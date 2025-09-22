# File Integrity Checker with Jira Integration

This project is a Python-based file integrity monitoring tool that periodically checks a directory for changes (creations, modifications, and deletions) and automatically raises tickets in Jira for any detected integrity violations.

## Features

- **File Hashing**: Uses SHA256 to generate a unique hash for each file.
- **Baseline Comparison**: Stores a baseline of file hashes and compares it against the current state of the files.
- **Integrity Verification**:
  - Detects when a file's content has been modified.
  - Detects when a new, untracked file is added.
  - Detects when a monitored file is deleted.
- **Automated Jira Ticketing**:
  - Creates a "Medium" priority ticket for new files.
  - Creates a "High" priority ticket for modified files.
  - Creates a "High" priority ticket for deleted files.
- **Configurable**: Easily configure Jira credentials and project details using an environment file.

## How It Works

1.  **Baseline Creation**: The `update_baseline.py` script is run once to scan the `important_files/` directory. It calculates the SHA256 hash for every file and saves it in `checksums.json`. This file acts as the trusted baseline.

2.  **Integrity Monitoring**: The `main.py` script runs in a loop, performing the following checks at a set interval:
    - It recalculates the hashes of all current files in the `important_files/` directory.
    - It compares the new hashes against the hashes stored in `checksums.json`.
    - **For Modified Files**: If a file's hash has changed, it raises a "File Integrity Alert" ticket in Jira.
    - **For Deleted Files**: If a file from the baseline is missing, it raises a "File Deletion Detected" ticket.
    - **For New Files**: If a new, untracked file is found, it raises a "New File Detected" ticket and adds the new file's hash to the baseline to monitor it going forward.

3.  **Jira Integration**: The `jira.py` module contains all the logic for communicating with the Jira API. It formats the ticket details (summary, description, priority) and sends the request to create the ticket.

## Setup and Installation

### Prerequisites

- Python 3.x
- A Jira account with API token credentials.

### Steps

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/SH4RWIN/auto-file-integrity-ticketer-Jira.git
    cd auto-file-integrity-ticketer-Jira
    ```

2.  **Install Dependencies**
    It's recommended to use a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```
    Then, install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Environment Variables**
    Copy the example environment file and fill in your Jira credentials:
    ```bash
    cp .env.example .env
    ```
    Now, edit the `.env` file with your actual credentials:
    ```env
    JIRA_URL="https://your-domain.atlassian.net"
    JIRA_EMAIL="your-email@example.com"
    JIRA_API_TOKEN="your-api-token"
    PROJECT_KEY="YOUR_PROJECT_KEY"
    ```

## Usage

1.  **Create the Initial Baseline**
    Before running the monitor for the first time, you need to create the baseline of your important files.
    ```bash
    python update_baseline.py
    ```
    This will generate the `checksums.json` file.

2.  **Run the Integrity Checker**
    To start monitoring the `important_files/` directory, run the main script:
    ```bash
    python main.py
    ```
    The script will run continuously and check for file changes every 15 seconds (by default). You can stop it by pressing `Ctrl+C`.

## Project Structure

```
.
├── important_files/      # The directory with files to be monitored.
├── .env.example          # Example environment variables.
├── .gitignore            # Specifies files to be ignored by Git.
├── checksums.json        # The baseline hashes of all monitored files.
├── crypto.py             # Handles SHA256 hash generation.
├── jira.py               # Manages Jira API communication and ticket creation.
├── main.py               # The main script that runs the integrity checks.
├── update_baseline.py    # Script to create or update the baseline.
├── requirements.txt      # Project dependencies.
└── README.md             # This file.
```

## Known Issues

- If an integrity issue is not resolved before the next check, the script will raise a duplicate Jira ticket for the same problem. A mechanism to track open tickets and prevent duplicates is needed.
