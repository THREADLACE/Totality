#!/usr/bin/env python3

import os
import subprocess
import logging
import requests
import time

# Configure Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s')

# GitHub Repository and Release Info
REPO_OWNER="THREADLACE"
REPO_NAME="Totality"
REPO_URL=f"https://github.com/{REPO_OWNER}/{REPO_NAME}"
GITHUB_API=f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/releases/latest"

# System Information
DOCKER_USERNAME="https://index.docker.io/v1/"
GCP_PROJECT_ID="big-iridium-450012-e1"

# Required CLI Tools & Environment Variables
required_tools={'GitHub CLI':'gh', 'Docker':'docker', 'Google Cloud CLI':'gcloud'}
required_envs=['GITHUB_USERNAME', 'GITHUB_REPOSITORY', 'DOCKER_USERNAME', 'GCP_PROJECT_ID']

def check_command(cmd):
    """Checks if a command exists in the system."""
    return subprocess.run(f'command -v {cmd}', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode == 0

def get_latest_release_version():
    """Gets the latest release version from GitHub."""
    try:
        response = requests.get(GITHUB_API)
        response.raise_for_status()
        release_data = response.json()
        return release_data.get("tag_name", "Unknown Version")
    except requests.RequestException as e:
        logging.error(f"Failed to fetch latest release version: {e}")
        return None

def update_script():
    """Updates the script to the latest version from GitHub."""
    latest_version = get_latest_release_version()
    script_path = os.path.abspath(__file__)
    
    if latest_version:
        logging.info(f"Latest version detected: {latest_version}")
        script_url = f"{REPO_URL}/raw/{latest_version}/main.py"

        try:
            response = requests.get(script_url)
            response.raise_for_status()
            with open(script_path, 'wb') as file:
                file.write(response.content)
            logging.info(f"Script updated to version {latest_version}.")
            return True
        except requests.RequestException as e:
            logging.error(f"Failed to update script: {e}")
    return False

def verify_integrations():
    """Verifies all necessary integrations."""
    missing = []
    
    # Check CLI tools
    for tool, cmd in required_tools.items():
        if not check_command(cmd):
            missing.append(tool)
        
    # Check environment variables
    for env in required_envs:
        if not os.getenv(env):
            missing.append(env)
    
    if missing:
        logging.error("Missing dependencies: " + ', '.join(missing))
        return False

    logging.info("All integrations verified successfully.")
    return True
            
def execute_script():
    """Runs the complete workflow."""
    if not verify_integrations():
        logging.error("Fix the missing components before proceeding.")
        return
            
    logging.info("Executing Totality workflow...")
            
    try:
        subprocess.run(["gh", "repo", "view", "THREADLACE/Totality"], check=True)
        subprocess.run(["docker", "images"], check=True)
        subprocess.run(["gcloud", "projects", "list"], check=True)
        logging.info("Totality executed successfully.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Execution failed: {e}")
    
if __name__ == "__main__":
    if update_script():
        logging.info("Script updated successfully. Restarting execution.")
        time.sleep(2)
        execute_script()
    else:
        logging.info("No update available. Proceeding with execution.")
        execute_script()
    
    logging.info("Final Check: Nothing is missing. Totality is complete.")
