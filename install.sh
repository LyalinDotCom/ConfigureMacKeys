#!/bin/bash

# ConfigureMacKeys Installation Script
# This script installs the configkeys command globally

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="/usr/local/bin"
SCRIPT_NAME="configkeys"
SOURCE_SCRIPT="$SCRIPT_DIR/configkeys.py"

echo "🔧 Installing ConfigureMacKeys..."

# Check if the source script exists
if [ ! -f "$SOURCE_SCRIPT" ]; then
    echo "❌ Error: configkeys.py not found in $SCRIPT_DIR"
    exit 1
fi

# Check if we have write permission to /usr/local/bin
if [ ! -w "$INSTALL_DIR" ]; then
    echo "📋 Need sudo permissions to install to $INSTALL_DIR"
    sudo ln -sf "$SOURCE_SCRIPT" "$INSTALL_DIR/$SCRIPT_NAME"
else
    ln -sf "$SOURCE_SCRIPT" "$INSTALL_DIR/$SCRIPT_NAME"
fi

# Make sure the script is executable
chmod +x "$SOURCE_SCRIPT"

echo "✅ ConfigureMacKeys installed successfully!"
echo ""
echo "You can now use the 'configkeys' command from anywhere:"
echo "  configkeys list              # List all environment variables"
echo "  configkeys set KEY value     # Set an environment variable"
echo "  configkeys remove KEY        # Remove an environment variable"
echo "  configkeys info              # Show config file location"
echo ""
echo "Run 'configkeys --help' for more information." 