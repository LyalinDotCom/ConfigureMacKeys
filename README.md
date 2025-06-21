# ConfigureMacKeys

A simple CLI tool for managing environment variables on macOS. No more manually editing `~/.zshrc`!

## Features

- **List all environment variables** or filter by name
- **Set new or update existing environment variables** with automatic persistence
- **Remove environment variables** from your shell configuration
- **Automatic backups** before making changes
- **Works with zsh** (default macOS shell)

## Installation

1. Clone or download this repository
2. Run the installation script:
   ```bash
   ./install.sh
   ```

This will install the `configkeys` command globally so you can use it from anywhere.

## Usage

### List Environment Variables

```bash
# List all environment variables
configkeys list

# Filter variables by name (case-insensitive)
configkeys list PATH
configkeys list GEMINI
```

### Set Environment Variables

```bash
# Set a new environment variable (permanent)
configkeys set GEMINI_API_KEY your_api_key_here

# Set a variable only for the current session (temporary)
configkeys set DEBUG_MODE true --temp
```

### Remove Environment Variables

```bash
# Remove a variable from your shell configuration
configkeys remove OLD_VARIABLE
```

### Show Configuration Info

```bash
# Show where your shell configuration file is located
configkeys info
```

## Examples

Setting up your Gemini API key:
```bash
configkeys set GEMINI_API_KEY sk-your-api-key-here
```

Checking if it's set:
```bash
configkeys list GEMINI
```

Removing it later:
```bash
configkeys remove GEMINI_API_KEY
```

## How It Works

- **Configuration File**: Uses `~/.zshrc` as the primary shell configuration file
- **Backups**: Automatically creates backups (`.zshrc.backup`) before making changes
- **Current Session**: Changes are applied immediately to your current terminal session
- **Persistence**: New variables are added to your shell config for future sessions

## Safety Features

- Creates backups before modifying configuration files
- Validates variable names and values
- Shows clear feedback about what changes were made
- Handles errors gracefully

## Requirements

- macOS (tested on recent versions)
- Python 3 (comes pre-installed on macOS)
- zsh shell (default on modern macOS)

## Troubleshooting

If you encounter issues:

1. Check that Python 3 is available: `python3 --version`
2. Ensure the script is executable: `chmod +x configkeys.py`
3. Check your shell configuration: `configkeys info`

## Uninstall

To remove the tool:
```bash
sudo rm /usr/local/bin/configkeys
``` 