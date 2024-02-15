#!/bin/bash

# Determine the directory where this script is located,
# which is assumed to be the root of the Git repository
REPO_DIR=$(dirname "$0")

# Change to the repository directory
cd "$REPO_DIR"

# Check if the 'local' file exists in the repository
if [ -f "local" ]; then
    echo "Local file found. Aborting script to prevent unintended changes."
    exit 1
fi

# Reset the working directory to the last commit
git reset --hard HEAD

# Pull the latest changes from the remote repository
git pull

echo "Repository has been updated to the latest commit."
