# Prerequisites

Before running the labs, make sure your environment meets the following requirements. This guide walks you through each dependency and how to verify it is correctly installed. Tested under Ubuntu-24.04 (WSL). 

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

## 5. shai CLI (optional — AI terminal assistant)

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

## Quick validation script

Run these commands to verify everything is in place:

```bash
# Check Python version
python3 --version

# Check pip is available
pip3 --version

# Check the OpenStack CLI is installed
openstack --version

```