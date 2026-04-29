# Prerequisites

Before running the labs, make sure your environment meets the following requirements. This guide walks you through each dependency and how to verify it is correctly installed.

## 1. Python 3.9+

The lab framework and all exercises are written in Python. You need Python **3.9 or later** (3.11 recommended).

```bash
# Check your Python version
python3 --version
# Expected output: Python 3.11.x (or any 3.9+)
```

If Python is not installed, download it from [python.org](https://www.python.org/downloads/) or use your system package manager:

```bash
# Debian / Ubuntu
sudo apt update && sudo apt install -y python3 python3-pip python3-venv

# macOS (Homebrew)
brew install python@3.11
```

## 2. pip (Python package manager)

`pip` is used to install the Python dependencies required by the labs (openstacksdk, PyYAML, pytest, etc.).

```bash
# Verify pip is available
pip3 --version
# Expected output: pip 2x.x from … (python 3.x)
```

If pip is missing, install it with:
```bash
sudo apt install -y python3-pip
```

## 3. OpenStack CLI client

All exercises use the `openstack` command-line client. Install it via pip:

```bash
# Install the OpenStack CLI client
pip3 install python-openstackclient

# Verify the installation
openstack --version
# Expected output: openstack 7.x.x (or later)
```

## 4. OpenStack SDK & Python dependencies (optional)

If you also want to run the automated assessment engine, install the following Python packages (defined in `labs/base/requirements.txt`):

- **openstacksdk 4.6.0** — official Python SDK for OpenStack APIs
- **PyYAML 6.0.2** — YAML configuration parsing
- **pytest 8.3.4** — test runner used by the assessment engine
- **hypothesis 6.112.5** — property-based testing library

Install them in a virtual environment:

```bash
# Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate   # Linux / macOS
# .venv\Scripts\activate    # Windows

# Install dependencies
pip install -r labs/base/requirements.txt
```

## 5. Docker (optional — for containerised labs)

The labs can run inside a Docker container that bundles all dependencies. If you prefer this approach, install Docker:

```bash
# Check Docker is installed
docker --version
# Expected output: Docker version 2x.x.x
```

Install Docker from [docs.docker.com](https://docs.docker.com/get-docker/).

### Installing Docker on Ubuntu (if not present)

If Docker is not installed on your Ubuntu machine, follow the steps below to install it from the official Docker repository:

```bash
# Remove any existing broken configs
sudo rm -f /etc/apt/sources.list.d/docker.list
sudo rm -f /etc/apt/sources.list.d/docker.sources

# Add the Docker repository with the noble codename
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  noble stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Make sure the GPG key exists
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

# Update and install Docker
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

## 6. shai CLI (optional — AI terminal assistant)

[shai](https://github.com/ovh/shai) is an interactive coding agent that lives in your terminal. It can help you write code, fix bugs, and answer questions while working through the labs.

```bash
# Check if shai is installed
shai --version
```

If shai is not installed, run the following command:

```bash
# Install the latest stable release
curl -fsSL https://raw.githubusercontent.com/ovh/shai/main/install.sh | sh
```

The binary will be installed in `$HOME/.local/bin`. Make sure this directory is in your `PATH`:

```bash
# Add to your PATH if needed
export PATH="$HOME/.local/bin:$PATH"
```

### Installing VS Code on Windows

If you don't have VS Code installed yet, follow these steps:

1. Download the installer from [code.visualstudio.com](https://code.visualstudio.com/download).
2. Run the `.exe` installer and follow the wizard.
3. Make sure to check **"Add to PATH"** during installation so you can use the `code` command from a terminal.

You can also install it via `winget` from a PowerShell terminal:

```bash
winget install -e --id Microsoft.VisualStudioCode
```

Verify the installation:

```bash
code --version
```

### shai-dev — VS Code Extension (alternative)

If you prefer using shai directly inside VS Code rather than in the terminal, you can install the [shai-dev](https://marketplace.visualstudio.com/items?itemName=shai-dev.shai-vscode) extension. It brings shai's capabilities (code assistance, fixes, questions) right into your editor.

To install it:

1. Open VS Code, go to the Extensions tab (`Ctrl+Shift+X`), search for **shai-dev** and click *Install*.
2. Or install it from the command line:

```bash
code --install-extension shai-dev.shai-vscode
```

## 7. OpenStack credentials

The lab runner needs valid OpenStack credentials. You can provide them via **environment variables** or a **credentials file**.

### Option A — Environment variables (Application Credentials)

```bash
export OS_AUTH_URL="https://auth.cloud.ovh.net/v3"
export OS_AUTH_TYPE="v3applicationcredential"
export OS_APPLICATION_CREDENTIAL_ID="your-credential-id"
export OS_APPLICATION_CREDENTIAL_SECRET="your-credential-secret"
```

### Option A — Environment variables (User / Password)

```bash
export OS_AUTH_URL="https://auth.cloud.ovh.net/v3"
export OS_USERNAME="your-username"
export OS_PASSWORD="your-password"
export OS_PROJECT_NAME="your-project"
export OS_DOMAIN_NAME="Default"
```

### Option B — Credentials file

Create `~/.openstack/credentials.yaml`:

```yaml
auth_url: https://auth.cloud.ovh.net/v3
username: your-username
password: your-password
project_name: your-project
domain_name: Default
```

## 8. Basic terminal knowledge

You should be comfortable running commands in a terminal (bash, zsh, or PowerShell). All exercises are launched from the command line.

## Quick validation script

Run these commands to verify everything is in place:

```bash
# Check Python version
python3 --version

# Check pip is available
pip3 --version

# Check the OpenStack CLI is installed
openstack --version

# Test authentication
openstack token issue
```