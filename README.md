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

## Limitations and Considerations

While `configkeys` aims to simplify environment variable management, there are some limitations and scenarios to be aware of:

*   **Shell Reload Required**: After setting or unsetting a variable that affects future terminal sessions (i.e., not using the `--temp` flag), you'll need to either:
    *   Restart your terminal.
    *   Source your shell configuration file (e.g., `source ~/.zshrc`) in any open terminal tabs/windows for the changes to take effect there.
    The tool will remind you of this.
*   **Temporary Variables**: While `configkeys set --temp` exists for session-specific variables, this utility primarily focuses on persistent environment variables. For complex temporary variable needs, direct shell commands like `export VAR="value"` might be more straightforward.
*   **Application-Specific Variables**: Some applications or development tools manage their own environment variables internally or through dedicated configuration files (e.g., `.env` files for Node.js projects, IDE-specific settings). `configkeys` manages shell-level environment variables and won't interfere with these.
*   **System-Wide Variables**: This tool operates at the user level, modifying user-specific shell configuration files. It does not manage system-wide environment variables that would typically require `sudo` privileges and modifications to files like `/etc/profile` or `/etc/environment`.
*   **GUI Applications**: GUI applications on macOS do not always inherit environment variables set in shell configuration files like `.zshrc`. If you need an environment variable to be available to a GUI application, you might need to use other methods, such as editing `environment.plist` or using `launchctl setenv`.
*   **Scope**: The tool is designed for managing variables in `~/.zshrc`. If you use a different shell or a more complex shell setup (e.g., sourcing multiple files, using frameworks like Oh My Zsh that have their own variable management), you might need to adjust your workflow or ensure `configkeys` targets the correct configuration file if it's not the default.

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