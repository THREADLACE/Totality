#!/bin/bash

# Update Homebrew and install dependencies
echo "Updating Homebrew..."
brew update

# Install GitHub CLI
echo "Installing GitHub CLI..."
brew install gh

# Install Docker
echo "Installing Docker..."
brew install --cask docker

# Install Google Cloud CLI
echo "Installing Google Cloud CLI..."
brew install --cask google-cloud-sdk

# Install Python 3
echo "Installing Python 3..."
brew install python

# Verify installations
echo "Verifying installations..."

# Verify GitHub CLI installation
if command -v gh &>/dev/null; then
  echo "GitHub CLI installed successfully."
else
  echo "Error: GitHub CLI installation failed."
fi

# Verify Docker installation
if command -v docker &>/dev/null; then
  echo "Docker installed successfully."
else
  echo "Error: Docker installation failed."
fi

# Verify Google Cloud CLI installation
if command -v gcloud &>/dev/null; then
  echo "Google Cloud CLI installed successfully."
else
  echo "Error: Google Cloud CLI installation failed."
fi

# Verify Python installation
if command -v python3 &>/dev/null; then
  echo "Python 3 installed successfully."
else
  echo "Error: Python 3 installation failed."
fi

echo "Installation script complete!"

