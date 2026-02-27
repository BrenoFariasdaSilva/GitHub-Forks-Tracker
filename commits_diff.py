"""
================================================================================
GitHub Forks Tracker - commits_diff.py
================================================================================
Author      : Breno Farias da Silva
Created     : 2026-02-27
Description :
    Utilities to compute divergent commits between an original repository and
    its forks, and to export divergent commits to CSV files.

Usage:
    Import `build_original_sha_set`, `find_divergent_commits`, `export_commits_csv`,
    and `process_single_fork` from this module.

Outputs:
    CSV files written to the provided outputs directory when divergent commits
    are present.

Dependencies:
    - csv
    - colorama

Assumptions & Notes:
    - CSV header is exactly: ["Commit Number", "Commit Hash", "Commit Date", "Commit Owner", "Commit Message"].
    - No CSV file is created when there are zero divergent commits.
"""


import atexit  # For playing a sound when the program finishes
import csv  # Local import for CSV writing
import datetime  # For getting the current date and time
import os  # For running a command in the terminal
import platform  # For getting the operating system name
import sys  # For system-specific parameters and functions
import typing  # For type hints
from colorama import Style  # For coloring the terminal
from github_api import GitHubAPI  # Imported for type checking only to avoid runtime import cycles
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


def build_original_sha_set(original_commits: "list") -> "set[str]":
    """
    Build a set of SHA hashes from original commits.

    :param original_commits: List of commit dictionaries from original repository
    :return: Set of commit SHA strings
    """

    original_shas: set = set()  # Initialize SHA set
    
    for commit in original_commits:  # Iterate commits
        sha = commit.get("sha")  # Extract SHA
        
        if isinstance(sha, str):  # Ensure string
            original_shas.add(sha)  # Add SHA to set
            
    return original_shas  # Return SHA set


def find_divergent_commits(original_shas: "set[str]", fork_commits: "list") -> "list":
    """
    Return commits present in `fork_commits` but not in `original_shas` preserving chronological order.

    :param original_shas: Set of original commit SHAs
    :param fork_commits: List of commits from fork (newest first)
    :return: List of divergent commits ordered oldest -> newest
    """

    divergent = [c for c in fork_commits if c.get("sha") not in original_shas]  # Filter by SHA
    divergent.reverse()  # Oldest -> newest
    
    return divergent  # Return filtered list


def build_commit_url(
    api: typing.Optional["GitHubAPI"], fork_owner: str, fork_name: str, sha: str
) -> str:
    """
    Build a commit URL using the API helper method.

    :param api: Optional GitHubAPI client instance
    :param fork_owner: Owner login of the fork
    :param fork_name: Repository name of the fork
    :param sha: Commit SHA hash
    :return: URL string to the commit on GitHub, or empty string on failure
    """

    commit_url: str = ""  # Initialize URL
    if api and fork_owner and fork_name and sha:  # Ensure all required info exists
        try:  # Attempt to build URL using API helper
            base: str = api.build_repo_url(fork_owner, fork_name)  # Build base URL
            commit_url = f"{base}/commit/{sha}"  # Construct full commit URL
        except Exception:  # Silently ignore failures
            commit_url = ""  # Return empty string if construction fails

    return commit_url  # Return commit URL


def build_commit_csv_row(
    commit: dict,
    commit_number: int,
    api: typing.Optional["GitHubAPI"] = None,
    fork_owner: typing.Optional[str] = None,
    fork_name: typing.Optional[str] = None,
) -> typing.List[typing.Any]:
    """
    Build a CSV row from a commit dictionary.

    :param commit: Commit dictionary returned from GitHub API
    :param commit_number: Sequential commit number (oldest->newest)
    :param api: Optional GitHubAPI client for URL construction
    :param fork_owner: Optional fork owner login
    :param fork_name: Optional fork repository name
    :return: List representing a CSV row
    """

    commit_obj: dict = commit.get("commit", {})  # Commit details
    author_obj: dict = commit_obj.get("author") or {}  # Author info
    sha: str = commit.get("sha", "")  # Commit SHA
    date: str = author_obj.get("date", "")  # Commit ISO date
    owner_name: str = author_obj.get("name") or "Unknown"  # Commit author name
    message: str = commit_obj.get("message", "")  # Commit message
    commit_url: str = build_commit_url(api, fork_owner or "", fork_name or "", sha)  # Build URL

    return [commit_number, sha, date, owner_name, message, commit_url]  # CSV row


def export_commits_csv(
    api: GitHubAPI,
    fork_name: str,
    fork_owner: str,
    commits: typing.List[dict],
    outputs_dir: str,
) -> str:
    """
    Export commits to CSV and return the output path.

    :param fork_name: Repository name of the fork
    :param fork_owner: Owner login of the fork
    :param commits: List of commit dicts ordered oldest->newest
    :param outputs_dir: Directory to write CSV into
    :return: Path to the written CSV file
    """

    if not commits:  # No commits, nothing to write
        return ""  # Return empty

    Path(outputs_dir).mkdir(parents=True, exist_ok=True)  # Ensure outputs dir exists
    count = len(commits)  # Number of divergent commits
    safe_name = f"{fork_name}-{fork_owner}-{count}.csv"  # File name using fork name and owner
    output_path = os.path.join(outputs_dir, safe_name)  # Full path

    header = [
        "Commit Number",
        "Commit Hash",
        "Commit Date",
        "Commit Owner",
        "Commit Message",
        "Commit URL",
    ]  # CSV header with URL

    with open(output_path, "w", newline="", encoding="utf-8") as fh:  # Open file
        writer = csv.writer(fh, quoting=csv.QUOTE_MINIMAL)  # CSV writer
        writer.writerow(header)  # Write header

        for idx, commit in enumerate(commits, start=1):  # Iterate commits
            row = build_commit_csv_row(commit, idx, api=api, fork_owner=fork_owner, fork_name=fork_name)  # Build row with URL
            writer.writerow(row)  # Write CSV row

    return output_path  # Return path


def process_single_fork(api: GitHubAPI, fork: dict, original_shas: typing.Set[str], outputs_dir: str) -> None:
    """
    Process a single fork: fetch commits, compute divergence and export CSV.

    :param api: GitHubAPI client instance
    :param fork: Fork metadata dictionary
    :param original_shas: Set of original repository SHAs
    :param outputs_dir: Directory to write CSV outputs
    :return: None
    """

    fork_owner = (fork.get("owner") or {}).get("login") or ""  # Fork owner
    fork_name = fork.get("name") or ""  # Fork repo name
    
    if not fork_owner or not fork_name:  # Skip malformed entries
        return  # Nothing to do

    try:  # Fetch fork commits
        fork_commits = api.list_commits(fork_owner, fork_name)  # All commits newest->oldest
    except Exception as exc:  # Handle inaccessible or deleted fork
        print(f"\t- {BackgroundColors.YELLOW}Skipping fork {BackgroundColors.CYAN}{fork_owner}{BackgroundColors.YELLOW}/{BackgroundColors.CYAN}{fork_name}{BackgroundColors.YELLOW}, error: {exc}{Style.RESET_ALL}")  # Log
        return  # Skip

    divergent = find_divergent_commits(original_shas, fork_commits)  # Compute divergent commits
    
    if not divergent:  # No divergent commits
        verbose_output(f"\t- {BackgroundColors.YELLOW}No divergent commits for {BackgroundColors.CYAN}{fork_owner}{BackgroundColors.YELLOW}/{BackgroundColors.CYAN}{fork_name}{Style.RESET_ALL}")  # Log
        return  # Nothing to export

    outpath = export_commits_csv(api, fork_name, fork_owner, divergent, outputs_dir)  # Write CSV
    verbose_output(f"\t- {BackgroundColors.GREEN}Exported {BackgroundColors.CYAN}{len(divergent)}{BackgroundColors.GREEN} divergent commits to {BackgroundColors.CYAN}{outpath}{Style.RESET_ALL}")  # Log


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
        f"{BackgroundColors.CLEAR_TERMINAL}{BackgroundColors.BOLD}{BackgroundColors.GREEN}Welcome to the {BackgroundColors.CYAN}GitHub Forks Tracker - commits_diff.py{BackgroundColors.GREEN}!{Style.RESET_ALL}",
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
