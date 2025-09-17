import os
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import json
# Load environment variables from a .env file
load_dotenv()

# Configuration
# This will read your credentials from the .env file.
JIRA_URL = os.getenv("JIRA_URL")
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")
PROJECT_KEY = os.getenv("PROJECT_KEY")

# ======= Master Ticker Creator =======

def create_jira_ticket(summary, description, priority, project_key=PROJECT_KEY, issue_type="Task"):
    # Check if all the Credentials are loaded, (Fail-Fast).
    if not all([JIRA_URL, JIRA_EMAIL, JIRA_API_TOKEN, PROJECT_KEY]):
        print("Credentials Missing: One or more Jira configuration variables are missing.")
        print("Please ensure JIRA_URL, JIRA_EMAIL, JIRA_API_TOKEN, and PROJECT_KEY are set in your .env file.")
        exit()
    
    url = f"{JIRA_URL}/rest/api/3/issue"
    auth = HTTPBasicAuth(JIRA_EMAIL, JIRA_API_TOKEN)
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    fields = {
            "project": {"key": project_key},
            "summary": summary,
            "description": {
                "type": "doc",
                "version": 1,
                "content": [{"type": "paragraph", "content": [{"type": "text", "text": description}]}]
            },
            "issuetype": {"name": issue_type},
            "priority": {"name": priority}
        }

    payload = {"fields": fields}
    try:
        response = requests.post(
           url,
           data=json.dumps(payload),
           headers=headers,
           auth=auth,
           timeout=30
        )

        response.raise_for_status() # If there is an error the exceptions will catch it.

        print("Ticket Raised Succesfully...")
        print(f"Success! Ticket '{response.json()['key']}' created.")
        return response.json()

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err} - {response.text}")
    except requests.exceptions.RequestException as req_err:
        print(f"A request error occurred: {req_err}")
    return None
    

# ======= custom tickets =======

def raise_ticket_new_file(file_path):
    """ Jira Ticket for a newly created file """
    summary = f"New File Detected: {os.path.basename(file_path)}"
    description = (
        f"An untracked file has been detected in the monitored directory.\n\n"
        f"File Path: {file_path}\n\n"
        f"Please investigate and add it to the baseline if it is an authorized file."
    )
    priority="Medium"
    issue_type="task"
    ticket = create_jira_ticket(summary=summary, description=description, priority=priority, issue_type=issue_type)
    return ticket

def raise_ticket_file_modification(file_path, expected_hash, current_hash):
    """Creates a high-priority Jira ticket for a file hash mismatch."""
    summary = f"File Integrity Alert: Modification Detected in {os.path.basename(file_path)}"
    description = (
        f"A file's hash does not match the baseline, indicating a modification.\n\n"
        f"File Path: {file_path}\n\n"
        f"Expected Hash (from baseline):\n{expected_hash}\n\n"
        f"Current Hash (actual):\n{current_hash}\n\n"
        f"Immediate investigation is required."
    )
    priority="High"
    issue_type="task"
    ticket = create_jira_ticket(summary=summary, description=description, priority=priority, issue_type=issue_type)
    return ticket

def raise_ticket_file_deleted(file_path, expected_hash):
    """Creates a Jira ticket for a file that has been deleted."""
    summary = f"File Deletion Detected: {os.path.basename(file_path)}"
    description = (
        f"A file that was part of the baseline has been deleted from the directory.\n\n"
        f"File Path: {file_path}\n\n"
        f"Last Known Hash:\n{expected_hash}\n\n"
        f"Please verify if this deletion was authorized."
    )
    priority="High"
    issue_type="task"
    ticket = create_jira_ticket(summary=summary, description=description, priority=priority, issue_type=issue_type)
    return ticket


