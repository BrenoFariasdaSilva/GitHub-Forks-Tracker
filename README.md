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
