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
  - [Installation:](#installation)
  - [Run Programing Language Code:](#run-programing-language-code)
    - [Dependencies](#dependencies)
    - [Dataset - Optional](#dataset---optional)
  - [Usage](#usage)
  - [Results - Optional](#results---optional)
  - [How to Cite?](#how-to-cite)
  - [Contributing](#contributing)
  - [Collaborators](#collaborators)
  - [License](#license)
    - [Apache License 2.0](#apache-license-20)
    - [Creative Commons Zero v1.0 Universal (CC0 1.0)](#creative-commons-zero-v10-universal-cc0-10)
    - [MIT License](#mit-license)

## Introduction

Detailed project description.

## Requirements

Bullet points of the requirements.

## Setup

### Clone the repository

1. Clone the repository with the following command:

   ```bash
   git clone https://github.com/BrenoFariasDaSilva/GitHub-Forks-Tracker.git
   cd GitHub-Forks-Tracker
   ```

## Installation:

* Programing Language:

  * Manually:
      ```bash
      # Programing Language:
      sudo apt install program-language -y
      ```

  * Using Makefile:
      ```bash
      make install
      ```

  * Using ShellScript:
      ```bash
      chmod +x install.sh
      sudo ./install.sh
      ```  

## Run Programing Language Code:

```bash
# Command here 
```

### Dependencies

1. Install the project dependencies with the following command:

   ```bash
   make dependencies
   ```

### Dataset - Optional

1. Download the dataset from [WEBSITE-HERE]() and place it in this project directory `(/GitHub-Forks-Tracker)` and run the following command:

   ```bash
   make dataset
   ```

## Usage

In order to run the project, run the following command:

```bash
make run
```

## Results - Optional

Discuss the results obtained in the project.

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

## Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**. If you have suggestions for improving the code, your insights will be highly welcome.
In order to contribute to this project, please follow the guidelines below or read the [CONTRIBUTING.md](CONTRIBUTING.md) file for more details on how to contribute to this project, as it contains information about the commit standards and the entire pull request process.
Please follow these guidelines to make your contributions smooth and effective:

1. **Set Up Your Environment**: Ensure you've followed the setup instructions in the [Setup](#setup) section to prepare your development environment.

2. **Make Your Changes**:
   - **Create a Branch**: `git checkout -b feature/YourFeatureName`
   - **Implement Your Changes**: Make sure to test your changes thoroughly.
   - **Commit Your Changes**: Use clear commit messages, for example:
     - For new features: `git commit -m "FEAT: Add some AmazingFeature"`
     - For bug fixes: `git commit -m "FIX: Resolve Issue #123"`
     - For documentation: `git commit -m "DOCS: Update README with new instructions"`
     - For refactorings: `git commit -m "REFACTOR: Enhance component for better aspect"`
     - For snapshots: `git commit -m "SNAPSHOT: Temporary commit to save the current state for later reference"`
   - See more about crafting commit messages in the [CONTRIBUTING.md](CONTRIBUTING.md) file.

3. **Submit Your Contribution**:
   - **Push Your Changes**: `git push origin feature/YourFeatureName`
   - **Open a Pull Request (PR)**: Navigate to the repository on GitHub and open a PR with a detailed description of your changes.

4. **Stay Engaged**: Respond to any feedback from the project maintainers and make necessary adjustments to your PR.

5. **Celebrate**: Once your PR is merged, celebrate your contribution to the project!

## Collaborators

We thank the following people who contributed to this project:

<table>
  <tr>
    <td align="center">
      <a href="#" title="defina o titulo do link">
        <img src="https://github.com/BrenoFariasdaSilva.png" width="100px;" alt="My Profile Picture"/><br>
        <sub>
          <b>Breno Farias da Silva</b>
        </sub>
      </a>
    </td>
    <td align="center">
      <a href="#" title="defina o titulo do link">
        <img src="https://github.com/BrenoFariasdaSilva.png" width="100px;" alt="My Profile Picture"/><br>
        <sub>
          <b>Breno Farias da Silva</b>
        </sub>
      </a>
    </td>
    <td align="center">
      <a href="#" title="defina o titulo do link">
        <img src="https://github.com/BrenoFariasdaSilva.png" width="100px;" alt="My Profile Picture"/><br>
        <sub>
          <b>Breno Farias da Silva</b>
        </sub>
      </a>
    </td>
  </tr>
</table>

## License

### Apache License 2.0

This project is licensed under the [Apache License 2.0](LICENSE). This license permits use, modification, distribution, and sublicense of the code for both private and commercial purposes, provided that the original copyright notice and a disclaimer of warranty are included in all copies or substantial portions of the software. It also requires a clear attribution back to the original author(s) of the repository. For more details, see the [LICENSE](LICENSE) file in this repository.

### Creative Commons Zero v1.0 Universal (CC0 1.0)

This project is licensed under the [Creative Commons Zero v1.0 Universal](LICENSE) (CC0 1.0) Public Domain Dedication. This means that the work is released into the public domain, allowing anyone to use, modify, distribute, and perform the work, even for commercial purposes, without asking permission and without attributing the original author(s). However, it's appreciated if you include a copy of the license or a link to it in any significant use or distribution. For more details, see the [LICENSE](LICENSE) file in this repository.

### MIT License

This project is licensed under the [MIT License](LICENSE). The MIT License is a permissive license that is short and to the point. It lets people do anything they want with your code as long as they provide attribution back to you and don’t hold you liable. This license allows for commercial use, modification, distribution, private use, and sublicensing. See the [LICENSE](LICENSE) file in this repository for more details.
