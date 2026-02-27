"""
================================================================================
GitHub Forks Tracker - github_api.py
================================================================================
Author      : Breno Farias da Silva
Created     : 2026-02-27
Description :
    HTTP client for the GitHub REST API used by the GitHub Forks Tracker.
    Provides robust pagination, retry/backoff and rate-limit handling.

Usage:
    Import `GitHubAPI` and call `list_forks(owner, repo)` and
    `list_commits(owner, repo)` to iterate repository data.

Outputs:
    None (library module).

Dependencies:
    - requests
    - colorama

Assumptions & Notes:
    - Uses `per_page=100` and parses the `Link` header for pagination.
    - Handles 5xx retries and waits on rate-limit resets using
      `X-RateLimit-Remaining` / `X-RateLimit-Reset` headers.
"""


import atexit  # For playing a sound when the program finishes
import datetime  # For getting the current date and time
import os  # For running a command in the terminal
import platform  # For getting the operating system name
import requests  # Local import to avoid modifying top-level template
import sys  # For system-specific parameters and functions
import time  # For sleeping between retries
import typing  # For type hints
from colorama import Style  # For coloring the terminal
from Logger import Logger  # For logging output to both terminal and file
from pathlib import Path  # For handling file paths


# Macros:
class BackgroundColors:  # Colors for the terminal
    CYAN = "\033[96m"  # Cyan
    GREEN = "\033[92m"  # Green
    YELLOW = "\033[93m"  # Yellow
    RED = "\033[91m"  # Red
    BOLD = "\033[1m"  # Bold
    UNDERLINE = "\033[4m"  # Underline
    CLEAR_TERMINAL = "\033[H\033[J"  # Clear the terminal


# Execution Constants:
VERBOSE = False  # Set to True to output verbose messages

# Logger Setup:
logger = Logger(f"./Logs/{Path(__file__).stem}.log", clean=True)  # Create a Logger instance
sys.stdout = logger  # Redirect stdout to the logger
sys.stderr = logger  # Redirect stderr to the logger

# Sound Constants:
SOUND_COMMANDS = {
    "Darwin": "afplay",
    "Linux": "aplay",
    "Windows": "start",
}  # The commands to play a sound for each operating system
SOUND_FILE = "./.assets/Sounds/NotificationSound.wav"  # The path to the sound file

# RUN_FUNCTIONS:
RUN_FUNCTIONS = {
    "Play Sound": True,  # Set to True to play a sound when the program finishes
}


# Classes Definitions:


class GitHubAPI:
    """
    Minimal GitHub REST API client with pagination and retry logic.

    :param token: Personal access token for GitHub API authentication
    :return: None
    """


    def __init__(self, token: str) -> None:
        """
        Initialize the GitHubAPI client with an optional token for authentication.
        
        :param token: Personal access token for GitHub API authentication
        :return: None
        """
        
        self.session = requests.Session()  # Create a requests session
        
        if token:  # If token provided
            self.session.headers.update({"Authorization": f"Bearer {token}"})  # Set auth header
        
        self.session.headers.update({"Accept": "application/vnd.github.v3+json"})  # Use REST v3


    def execute_single_request(self, method: str, url: str, params: typing.Optional[dict] = None) -> "requests.Response":
        """
        Execute a single HTTP request and return the response.

        :param method: HTTP method
        :param url: Full URL
        :param params: Query parameters
        :return: requests.Response
        """

        return self.session.request(method, url, params=params, timeout=20)  # Perform request


    def is_rate_limited(self, resp: "requests.Response") -> bool:
        """
        Verify if response indicates a rate limit has been reached.

        :param resp: Response object
        :return: True if rate limited
        """

        remaining = resp.headers.get("X-RateLimit-Remaining")  # Remaining calls
        reset = resp.headers.get("X-RateLimit-Reset")  # Reset epoch
        
        return resp.status_code == 403 and remaining == "0" and bool(reset)  # Rate limited verify


    def compute_rate_limit_wait(self, resp: "requests.Response", fallback: float) -> int:
        """
        Compute seconds to wait until rate limit reset, fallback on error.

        :param resp: Response object
        :param fallback: Fallback seconds
        :return: Seconds to wait
        """

        reset = resp.headers.get("X-RateLimit-Reset")  # Reset epoch
        
        if reset is None:  # Missing header
            return int(fallback)  # Fallback to backoff
        
        try:  # Attempt to parse reset time
            reset_int = int(reset)  # Convert reset to int
        except Exception:  # Parse error
            return int(fallback)  # Fallback to backoff on parse error
        
        return max(1, reset_int - int(time.time()))  # Compute wait seconds


    def is_server_error(self, resp: "requests.Response") -> bool:
        """
        Verify if response is a server-side error (5xx).

        :param resp: Response object
        :return: True if server error
        """

        return resp.status_code >= 500  # Server error verify


    def is_client_error(self, resp: "requests.Response") -> bool:
        """
        Verify if response is a client-side error (4xx).

        :param resp: Response object
        :return: True if client error
        """

        return resp.status_code >= 400  # Client error verify


    def extract_link_header(self, resp: "requests.Response") -> typing.Optional[str]:
        """
        Extract the Link header from a response if present.

        :param resp: Response object
        :return: Link header string or None
        """

        return resp.headers.get("Link")  # Return Link header


    def parse_next_url(self, link_header: str) -> typing.Optional[str]:
        """
        Parse a Link header and return the URL for rel="next" if available.

        :param link_header: The Link header string
        :return: Next page URL or None
        """

        parts = link_header.split(",")  # Split link parts
        
        for part in parts:  # Iterate parts
            if 'rel="next"' in part:  # Next link found
                return part.split(";")[0].strip()[1:-1]  # Extract and return URL
        
        return None  # No next link


    def yield_items_from_data(self, data: typing.Any) -> typing.Iterator[dict]:
        """
        Yield items from parsed JSON data (list or single object).

        :param data: Parsed JSON payload
        :return: Iterator of items
        """

        if isinstance(data, list):  # If list of items
            for item in data:  # Iterate list
                yield item  # Yield each
            return  # End generator
        
        yield data  # Yield single object


    def request(self, method: str, url: str, params: typing.Optional[dict] = None) -> "requests.Response":
        """
        Perform HTTP request with retries, backoff and rate-limit handling.

        :param method: HTTP method (GET, POST, etc.)
        :param url: Full URL to request
        :param params: Query parameters
        :return: requests.Response on success
        """

        backoff = 1.0  # Initial backoff seconds
        for attempt in range(8):  # Retry loop
            try:  # Attempt request
                resp = self.execute_single_request(method, url, params=params)  # Perform single request
            except Exception:  # Network error (requests.RequestException)
                time.sleep(backoff)  # Sleep before retry
                backoff *= 2  # Exponential backoff
                continue  # Retry

            if self.is_rate_limited(resp):  # Rate limited
                wait_seconds = self.compute_rate_limit_wait(resp, backoff)  # Compute wait
                time.sleep(wait_seconds + 1)  # Sleep until reset
                continue  # Retry after wait

            if self.is_server_error(resp):  # Server error
                time.sleep(backoff)  # Sleep then retry
                backoff *= 2  # Increase backoff
                continue  # Retry

            if self.is_client_error(resp):  # Client error
                raise RuntimeError(f"HTTP {resp.status_code} for {url}")  # Raise for 4xx

            return resp  # Return successful response

        raise RuntimeError("Max retries exceeded for URL: " + url)  # Give up after retries


    def get_all_pages(self, url: typing.Optional[str], params: typing.Optional[dict] = None) -> typing.Iterator[dict]:
        """
        Yield items from paginated GitHub endpoints using `per_page=100` and Link headers.

        :param url: Endpoint URL
        :param params: Query parameters
        :yield: Parsed JSON items one by one
        """

        params = dict(params or {})  # Copy params
        params["per_page"] = 100  # Force 100 per page

        while url:  # Walk pages
            resp = self.request("GET", url, params=params)  # Perform request with retries
            if resp.status_code == 404:  # Not found
                return  # Stop iteration on 404

            data = resp.json()  # Parse JSON body
            for item in self.yield_items_from_data(data):  # Yield parsed items
                yield item  # Yield each item

            link = self.extract_link_header(resp)  # Extract Link header
            next_url = self.parse_next_url(link) if link else None  # Determine next page
            url = next_url  # Advance to next page


    def list_forks(self, owner: str, repo: str) -> typing.List[dict]:
        """
        List forks for a repository using GET /repos/{owner}/{repo}/forks.

        :param owner: Original repository owner
        :param repo: Repository name
        :return: List of fork repository dicts
        """

        url = f"https://api.github.com/repos/{owner}/{repo}/forks"  # Forks endpoint
        items: typing.List[dict] = []  # Collect forks
        
        for item in self.get_all_pages(url):  # Iterate pages
            items.append(item)  # Append fork
        
        return items  # Return forks


    def list_commits(self, owner: str, repo: str) -> typing.List[dict]:
        """
        Retrieve all commits for a repository using GET /repos/{owner}/{repo}/commits.

        :param owner: Repository owner
        :param repo: Repository name
        :return: List of commits (newest first as returned by GitHub)
        """

        url = f"https://api.github.com/repos/{owner}/{repo}/commits"  # Commits endpoint
        commits: typing.List[dict] = []  # Collection
        
        for item in self.get_all_pages(url):  # Iterate items
            commits.append(item)  # Append commit
        
        return commits  # Return list


    def build_repo_url(self, owner: str, repo: str) -> str:
        """
        Build the canonical GitHub repository URL for a given owner and repo.

        :param owner: Repository owner/login
        :param repo: Repository name
        :return: Full https:// URL for the repository
        """

        return f"https://github.com/{owner}/{repo}"


# Functions Definitions:


def verbose_output(true_string="", false_string=""):
    """
    Outputs a message if the VERBOSE constant is set to True.

    :param true_string: The string to be outputted if the VERBOSE constant is set to True.
    :param false_string: The string to be outputted if the VERBOSE constant is set to False.
    :return: None
    """

    if VERBOSE and true_string != "":  # If VERBOSE is True and a true_string was provided
        print(true_string)  # Output the true statement string
    elif false_string != "":  # If a false_string was provided
        print(false_string)  # Output the false statement string


def verify_filepath_exists(filepath):
    """
    Verify if a file or folder exists at the specified path.

    :param filepath: Path to the file or folder
    :return: True if the file or folder exists, False otherwise
    """

    verbose_output(
        f"{BackgroundColors.GREEN}Verifying if the file or folder exists at the path: {BackgroundColors.CYAN}{filepath}{Style.RESET_ALL}"
    )  # Output the verbose message

    return os.path.exists(filepath)  # Return True if the file or folder exists, False otherwise


def to_seconds(obj):
    """
    Converts various time-like objects to seconds.
    
    :param obj: The object to convert (can be int, float, timedelta, datetime, etc.)
    :return: The equivalent time in seconds as a float, or None if conversion fails
    """
    
    if obj is None:  # None can't be converted
        return None  # Signal failure to convert
    if isinstance(obj, (int, float)):  # Already numeric (seconds or timestamp)
        return float(obj)  # Return as float seconds
    if hasattr(obj, "total_seconds"):  # Timedelta-like objects
        try:  # Attempt to call total_seconds()
            return float(obj.total_seconds())  # Use the total_seconds() method
        except Exception:
            pass  # Fallthrough on error
    if hasattr(obj, "timestamp"):  # Datetime-like objects
        try:  # Attempt to call timestamp()
            return float(obj.timestamp())  # Use timestamp() to get seconds since epoch
        except Exception:
            pass  # Fallthrough on error
    return None  # Couldn't convert


def calculate_execution_time(start_time, finish_time=None):
    """
    Calculates the execution time and returns a human-readable string.

    Accepts either:
    - Two datetimes/timedeltas: `calculate_execution_time(start, finish)`
    - A single timedelta or numeric seconds: `calculate_execution_time(delta)`
    - Two numeric timestamps (seconds): `calculate_execution_time(start_s, finish_s)`

    Returns a string like "1h 2m 3s".
    """

    if finish_time is None:  # Single-argument mode: start_time already represents duration or seconds
        total_seconds = to_seconds(start_time)  # Try to convert provided value to seconds
        if total_seconds is None:  # Conversion failed
            try:  # Attempt numeric coercion
                total_seconds = float(start_time)  # Attempt numeric coercion
            except Exception:
                total_seconds = 0.0  # Fallback to zero
    else:  # Two-argument mode: Compute difference finish_time - start_time
        st = to_seconds(start_time)  # Convert start to seconds if possible
        ft = to_seconds(finish_time)  # Convert finish to seconds if possible
        if st is not None and ft is not None:  # Both converted successfully
            total_seconds = ft - st  # Direct numeric subtraction
        else:  # Fallback to other methods
            try:  # Attempt to subtract (works for datetimes/timedeltas)
                delta = finish_time - start_time  # Try subtracting (works for datetimes/timedeltas)
                total_seconds = float(delta.total_seconds())  # Get seconds from the resulting timedelta
            except Exception:  # Subtraction failed
                try:  # Final attempt: Numeric coercion
                    total_seconds = float(finish_time) - float(start_time)  # Final numeric coercion attempt
                except Exception:  # Numeric coercion failed
                    total_seconds = 0.0  # Fallback to zero on failure

    if total_seconds is None:  # Ensure a numeric value
        total_seconds = 0.0  # Default to zero
    if total_seconds < 0:  # Normalize negative durations
        total_seconds = abs(total_seconds)  # Use absolute value

    days = int(total_seconds // 86400)  # Compute full days
    hours = int((total_seconds % 86400) // 3600)  # Compute remaining hours
    minutes = int((total_seconds % 3600) // 60)  # Compute remaining minutes
    seconds = int(total_seconds % 60)  # Compute remaining seconds

    if days > 0:  # Include days when present
        return f"{days}d {hours}h {minutes}m {seconds}s"  # Return formatted days+hours+minutes+seconds
    if hours > 0:  # Include hours when present
        return f"{hours}h {minutes}m {seconds}s"  # Return formatted hours+minutes+seconds
    if minutes > 0:  # Include minutes when present
        return f"{minutes}m {seconds}s"  # Return formatted minutes+seconds
    return f"{seconds}s"  # Fallback: only seconds


def play_sound():
    """
    Plays a sound when the program finishes and skips if the operating system is Windows.

    :param: None
    :return: None
    """

    current_os = platform.system()  # Get the current operating system
    if current_os == "Windows":  # If the current operating system is Windows
        return  # Do nothing

    if verify_filepath_exists(SOUND_FILE):  # If the sound file exists
        if current_os in SOUND_COMMANDS:  # If the platform.system() is in the SOUND_COMMANDS dictionary
            os.system(f"{SOUND_COMMANDS[current_os]} {SOUND_FILE}")  # Play the sound
        else:  # If the platform.system() is not in the SOUND_COMMANDS dictionary
            print(
                f"{BackgroundColors.RED}The {BackgroundColors.CYAN}{current_os}{BackgroundColors.RED} is not in the {BackgroundColors.CYAN}SOUND_COMMANDS dictionary{BackgroundColors.RED}. Please add it!{Style.RESET_ALL}"
            )
    else:  # If the sound file does not exist
        print(
            f"{BackgroundColors.RED}Sound file {BackgroundColors.CYAN}{SOUND_FILE}{BackgroundColors.RED} not found. Make sure the file exists.{Style.RESET_ALL}"
        )


def main():
    """
    Main function.

    :param: None
    :return: None
    """

    print(
        f"{BackgroundColors.CLEAR_TERMINAL}{BackgroundColors.BOLD}{BackgroundColors.GREEN}Welcome to the {BackgroundColors.CYAN}GitHub Forks Tracker - github_api.py{BackgroundColors.GREEN}!{Style.RESET_ALL}",
        end="\n\n",
    )  # Output the welcome message

    start_time = datetime.datetime.now()  # Get the start time of the program
    
    # Implement logic here

    finish_time = datetime.datetime.now()  # Get the finish time of the program
    
    print(
        f"{BackgroundColors.GREEN}Start time: {BackgroundColors.CYAN}{start_time.strftime('%d/%m/%Y - %H:%M:%S')}\n{BackgroundColors.GREEN}Finish time: {BackgroundColors.CYAN}{finish_time.strftime('%d/%m/%Y - %H:%M:%S')}\n{BackgroundColors.GREEN}Execution time: {BackgroundColors.CYAN}{calculate_execution_time(start_time, finish_time)}{Style.RESET_ALL}"
    )  # Output the start and finish times
    print(
        f"\n{BackgroundColors.BOLD}{BackgroundColors.GREEN}Program finished.{Style.RESET_ALL}"
    )  # Output the end of the program message
    (
        atexit.register(play_sound) if RUN_FUNCTIONS["Play Sound"] else None
    )  # Register the play_sound function to be called when the program finishes


if __name__ == "__main__":
    """
    This is the standard boilerplate that calls the main() function.

    :return: None
    """

    main()  # Call the main function
