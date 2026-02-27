<div align="center">
  
# [GitHub-Forks-Tracker.](https://github.com/BrenoFariasdaSilva/GitHub-Forks-Tracker) <img src="https://github.com/BrenoFariasdaSilva/GitHub-Forks-Tracker/blob/main/.assets/Images/Github.svg"  width="3%" height="3%">

</div>

<div align="center">
  
---

[GitHub-Forks-Tracker.](https://github.com/BrenoFariasdaSilva/GitHub-Forks-Tracker) is a small, reliable command-line utility that inspects a target GitHub repository and its forks to discover commits present in forks but missing from the original repository. The tool is split into three focused modules: the HTTP client (`github_api.py`), the diff/export engine (`commits_diff.py`) and the CLI/orchestration entrypoint (`main.py`). It is designed for forensics-style auditing (maintainers, security researchers, migration teams) and emphasizes reproducible CSV exports, robust API behaviour, and clear logging.

---

</div>

<div align="center">

![GitHub Code Size in Bytes](https://img.shields.io/github/languages/code-size/BrenoFariasdaSilva/GitHub-Forks-Tracker)
![GitHub Commits](https://img.shields.io/github/commit-activity/t/BrenoFariasDaSilva/GitHub-Forks-Tracker/main)
![GitHub Last Commit](https://img.shields.io/github/last-commit/BrenoFariasdaSilva/GitHub-Forks-Tracker)
![GitHub Forks](https://img.shields.io/github/forks/BrenoFariasDaSilva/GitHub-Forks-Tracker)
![GitHub Language Count](https://img.shields.io/github/languages/count/BrenoFariasDaSilva/GitHub-Forks-Tracker)
![GitHub License](https://img.shields.io/github/license/BrenoFariasdaSilva/GitHub-Forks-Tracker)
![GitHub Stars](https://img.shields.io/github/stars/BrenoFariasdaSilva/GitHub-Forks-Tracker)
![GitHub Contributors](https://img.shields.io/github/contributors/BrenoFariasdaSilva/GitHub-Forks-Tracker)
![GitHub Created At](https://img.shields.io/github/created-at/BrenoFariasdaSilva/GitHub-Forks-Tracker)
![wakatime](https://wakatime.com/badge/github/BrenoFariasdaSilva/GitHub-Forks-Tracker.svg)

</div>

<div align="center">
  
![RepoBeats Statistics](https://repobeats.axiom.co/api/embed/a22ecc5feb500a6640faf46ff140ad205ee29952.svg "Repobeats analytics image")

</div>

## Table of Contents
- [GitHub-Forks-Tracker. ](#github-forks-tracker-)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Requirements](#requirements)
  - [Setup](#setup)
    - [Clone the repository](#clone-the-repository)
    - [Python Installation](#python-installation)
    - [Dependencies](#dependencies)
  - [Usage](#usage)
  - [Results](#results)
    - [Output behaviour and CSV format](#output-behaviour-and-csv-format)
    - [Logging and CLI output](#logging-and-cli-output)
    - [API behaviour and robustness](#api-behaviour-and-robustness)
    - [Modular responsibilities](#modular-responsibilities)
  - [How to Cite?](#how-to-cite)
  - [Contributing](#contributing)
  - [Collaborators](#collaborators)
  - [License](#license)
    - [Apache License 2.0](#apache-license-20)

## Introduction

[GitHub-Forks-Tracker.](https://github.com/BrenoFariasdaSilva/GitHub-Forks-Tracker) is a compact, command-line Python utility that automates discovering and exporting commits present in forks but missing from an original GitHub repository. The project is organized into modular components: `github_api.py` implements a resilient REST client with paginated requests (using `per_page=100`), Link-header parsing, retry/backoff logic and rate-limit wait handling; `commits_diff.py` contains the core diff logic that builds a set of original SHAs, identifies divergent commits (preserving chronological order oldest→newest), and writes CSV reports with commit metadata and URLs; and `main.py` provides a friendly CLI entrypoint that loads configuration from `.env` (via python-dotenv), accepts overrides (`--repo-url` or `--original-owner` + `--repo`, `--token`, `--outputs`) and orchestrates the workflow. Output is written to the `Outputs` directory as CSV files (one per fork with divergences) and the project includes logging via the Logger helper and terminal-friendly coloring via colorama.

Under the hood the tool is designed for reliability and forensic clarity: API calls handle transient 5xx failures and wait for `X-RateLimit-Reset` when GitHub limits are reached, JSON responses are normalized into item streams, and CSV exports include a stable header and commit URL generation so results are immediately actionable. Typical use cases include repository maintainers auditing forks, security researchers tracking injected commits, or teams migrating or pruning forks; the codebase is intentionally small and extensible so you can add features like parallel fork processing, richer CSV fields, or integration with issue trackers. Dependencies are minimal (`requests`, `python-dotenv`, `colorama`) and the CLI is ready to run locally after setting `GITHUB_TOKEN` and providing the target repository.

## Requirements

- Python 3.8+ (tested on the environment used for development)
- A GitHub personal access token with repository read access (`GITHUB_TOKEN`)
- Dependencies listed in `requirements.txt` (colorama, python-dotenv, requests)

## Setup

### Clone the repository

1. Clone the repository with the following command:

   ```bash
   git clone https://github.com/BrenoFariasDaSilva/GitHub-Forks-Tracker.git
   cd GitHub-Forks-Tracker
   ```

### Python Installation

Ensure Python 3.6 or higher is installed on your system:

**Linux (Ubuntu/Debian):**
```bash
sudo apt update  # Update package lists
sudo apt install python3 python3-pip python3-venv -y  # Install Python 3, pip, and venv
```

**macOS:**
```bash
brew install python3  # Using Homebrew
```

**Windows:**
Download and install from [python.org](https://www.python.org/downloads/)

### Dependencies

1. Install the project dependencies with the following command:

**Option 1: Using Makefile (Recommended)**
```bash
make dependencies
```

**Option 2: Using pip directly**
Before running the command below, you need to created (if not already created) and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

The CLI is implemented in `main.py`. Configuration is read from a local `.env` file (loaded via `python-dotenv`) and may be overridden by command line arguments. Command-line options follow this precedence: explicit CLI arguments override values present in `.env`.

Primary CLI options:
- `--repo-url`: full GitHub repository URL (overrides `--original-owner` +
  `--repo` and `REPO_URL` in the environment)
- `--original-owner`: original repository owner (overrides `ORIGINAL_OWNER`)
- `--repo`: repository name (overrides `REPO`)
- `--token`: GitHub token (overrides `GITHUB_TOKEN`)
- `--outputs`: outputs directory (default: `./Outputs/`)

Examples:

```bash
# Use a full repo URL and a token from the environment or CLI
python main.py --repo-url https://github.com/originalOwner/repo --token "$GITHUB_TOKEN"

# Or specify owner and repo separately
python main.py --original-owner originalOwner --repo repo --outputs ./Outputs/
```

Notes:
- The `GITHUB_TOKEN` must be available via `.env` or `--token` for API access.
- If `--repo-url` is provided it takes precedence over `--original-owner` + `--repo`.

## Results

The tool produces CSV files in the specified output directory, one per fork that contains divergent commits. Each CSV file includes metadata about the divergent commits (SHA, date, author, message) and a URL pointing to the commit in the fork repository. The tool also logs progress and API interactions to both the terminal and log files under `./Logs/`.

### Output behaviour and CSV format

- Output directory: by default results are written to `./Outputs/` (created automatically when a CSV is written). The directory can be changed with `--outputs` or by setting `OUTPUTS` in the environment.
- CSV files are created only for forks that contain divergent commits (no file is produced when a fork has zero divergent commits).
- CSV filename format: `{fork_name}-{fork_owner}-{N}.csv` where `N` is the number of divergent commits exported for that fork (see `commits_diff.export_commits_csv`).
- CSV columns (header):

  `["Commit Number", "Commit Hash", "Commit Date", "Commit Owner", "Commit Message", "Commit URL"]`

  `Commit Number` is sequential (oldest → newest), `Commit Hash` is the SHA, `Commit Date` is the commit ISO date from the GitHub API, `Commit Owner` is the author name (or `Unknown` when absent), and `Commit URL` is a fully-qualified GitHub URL pointing to the commit in the fork repository.

### Logging and CLI output

- The project uses the bundled `Logger` helper to capture terminal output and persist it under `./Logs/` as `Logs/main.log`, `Logs/commits_diff.log`, and `Logs/github_api.log` (one per module). During execution, `stdout` and `stderr` are redirected to the logger so both console and file traces are available.
- Per-fork progress is printed to the terminal (and logged). The tool prints a colored progress line when it begins processing a fork and a line such as:

  `- Exported <N> divergent commits to <OutputsPath>`

  when a CSV is successfully written.

### API behaviour and robustness

- Pagination: API requests use `per_page=100` and the `Link` header is parsed to follow `next` pages until the full result set is retrieved.
- Rate-limits: the client reads `X-RateLimit-Remaining` and `X-RateLimit-Reset` from responses and detects a rate-limited response (403 with remaining == "0"). The client computes the seconds until reset and waits the required time before continuing.
- Retry/backoff: transient server errors (5xx) are retried with a backoff strategy (the client implements retry loops and delays for robustness).
- Requests are executed using a `requests.Session()` with a default timeout (20s) and the `Accept: application/vnd.github.v3+json` header.

### Modular responsibilities

- `github_api.py`: encapsulates HTTP behaviour (session management, header configuration, paginated fetches, `Link` header parsing, rate-limit wait computation, and 5xx retry/backoff logic). Use `GitHubAPI` to call `list_forks(owner, repo)` and `list_commits(owner, repo)`.
- `commits_diff.py`: contains the core diffing logic that builds a set of original repository SHAs (`build_original_sha_set`), identifies divergent commits while preserving chronological order (oldest → newest), and writes CSV exports (`export_commits_csv`). It also exposes `process_single_fork` used by the CLI orchestration.
- `main.py`: CLI entrypoint that loads `.env`, parses CLI args, derives effective configuration (CLI > .env precedence), instantiates `GitHubAPI`, fetches forks and original commits, and dispatches fork processing.

This README reflects the implemented CLI behaviour, logging, CSV exports, API pagination, and rate-limit handling present in the codebase.

## How to Cite?

If you use the GitHub-Forks-Tracker in your research, please cite it using the following BibTeX entry:

```
@misc{softwareGitHub-Forks-Tracker:2026,
  title = {GitHub-Forks-Tracker: A lightweight CLI framework to analyze GitHub forks, detect divergent commits, and export results to CSV via the GitHub REST API},
  author = {Breno Farias da Silva},
  year = {2026},
  howpublished = {https://github.com/BrenoFariasdaSilva/GitHub-Forks-Tracker},
  note = {Accessed on February 27, 2026}
}
```

Additionally, a `main.bib` file is available in the root directory of this repository, in which contains the BibTeX entry for this project.

If you find this repository valuable, please don't forget to give it a ⭐ to show your support! Contributions are highly encouraged, whether by creating issues for feedback or submitting pull requests (PRs) to improve the project. For details on how to contribute, please refer to the [Contributing](#contributing) section below.

Thank you for your support and for recognizing the contribution of this tool to your work!
