#!/usr/bin/env python3
"""
ConfigureMacKeys - A simple CLI tool for managing environment variables on macOS
"""

import os
import sys
import argparse
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple, Optional


class MacEnvManager:
    def __init__(self):
        self.shell_config_files = [
            Path.home() / '.zshrc',
            Path.home() / '.bash_profile',
            Path.home() / '.bashrc'
        ]
        self.primary_config = Path.home() / '.zshrc'  # Primary for macOS with zsh

    def get_current_env_vars(self) -> Dict[str, str]:
        """Get all current environment variables"""
        return dict(os.environ)

    def list_env_vars(self, filter_pattern: Optional[str] = None) -> None:
        """List environment variables, optionally filtered by pattern"""
        env_vars = self.get_current_env_vars()
        
        if filter_pattern:
            filtered_vars = {k: v for k, v in env_vars.items() 
                           if filter_pattern.lower() in k.lower()}
        else:
            filtered_vars = env_vars

        if not filtered_vars:
            print("No environment variables found" + 
                  (f" matching '{filter_pattern}'" if filter_pattern else ""))
            return

        print(f"\nFound {len(filtered_vars)} environment variable(s):")
        print("-" * 50)
        
        # Sort by key name for better readability
        for key in sorted(filtered_vars.keys()):
            value = filtered_vars[key]
            # Truncate very long values for readability
            display_value = value if len(value) <= 100 else value[:97] + "..."
            print(f"{key}={display_value}")

    def get_shell_config_content(self) -> Tuple[List[str], Path]:
        """Read the primary shell configuration file"""
        config_file = self.primary_config
        
        if not config_file.exists():
            return [], config_file
        
        try:
            with open(config_file, 'r') as f:
                lines = f.readlines()
            return lines, config_file
        except Exception as e:
            print(f"Error reading {config_file}: {e}")
            return [], config_file

    def backup_config_file(self, config_file: Path) -> bool:
        """Create a backup of the configuration file"""
        backup_file = config_file.with_suffix(config_file.suffix + '.backup')
        try:
            if config_file.exists():
                subprocess.run(['cp', str(config_file), str(backup_file)], check=True)
                print(f"✓ Backup created: {backup_file}")
            return True
        except Exception as e:
            print(f"Error creating backup: {e}")
            return False

    def set_env_var(self, name: str, value: str, permanent: bool = True) -> bool:
        """Set an environment variable"""
        if not name:
            print("Error: Variable name cannot be empty")
            return False

        if not permanent:
            # For temporary variables, we can only provide the export command
            print(f"To set {name} in your current session, run:")
            print(f"  export {name}={value}")
            print("\nOr use this command with eval:")
            print(f"  eval $(configkeys export {name} {value})")
            return True

        # Make it permanent by adding to shell config
        lines, config_file = self.get_shell_config_content()
        
        # Create backup
        if not self.backup_config_file(config_file):
            print("Warning: Could not create backup, proceeding anyway...")

        # Check if variable already exists in the file
        export_line = f"export {name}={value}\n"
        pattern = f"export {name}="
        
        # Remove existing entries
        lines = [line for line in lines if not line.strip().startswith(pattern)]
        
        # Add the new export statement with comment (only if not already present)
        comment_line = "# Added by ConfigureMacKeys\n"
        if not any("# Added by ConfigureMacKeys" in line for line in lines):
            lines.append(f"\n{comment_line}")
        lines.append(export_line)
        
        try:
            # Ensure directory exists
            config_file.parent.mkdir(exist_ok=True)
            
            # Write the updated content
            with open(config_file, 'w') as f:
                f.writelines(lines)
            
            print(f"✓ Added {name} to {config_file}")
            print(f"✓ Variable will be available in new shell sessions")
            print("\nTo use in current session, run:")
            print(f"  source {config_file}")
            print("Or start a new terminal session")
            
            return True
            
        except Exception as e:
            print(f"Error writing to {config_file}: {e}")
            return False

    def remove_env_var(self, name: str) -> bool:
        """Remove an environment variable from shell config"""
        lines, config_file = self.get_shell_config_content()
        
        if not lines:
            print(f"No configuration file found at {config_file}")
            return False

        # Create backup
        if not self.backup_config_file(config_file):
            print("Warning: Could not create backup, proceeding anyway...")

        pattern = f"export {name}="
        original_count = len(lines)
        
        # Remove lines containing the export statement
        lines = [line for line in lines if not line.strip().startswith(pattern)]
        
        if len(lines) == original_count:
            print(f"Variable '{name}' not found in {config_file}")
            return False

        try:
            with open(config_file, 'w') as f:
                f.writelines(lines)
                
            print(f"✓ Removed {name} from {config_file}")
            print("Variable will be removed from new shell sessions")
            
            # Remove from current session
            if name in os.environ:
                del os.environ[name]
                print(f"✓ Removed {name} from current session")
            
            return True
            
        except Exception as e:
            print(f"Error writing to {config_file}: {e}")
            return False

    def show_config_location(self) -> None:
        """Show where the configuration file is located"""
        print(f"Primary configuration file: {self.primary_config}")
        print(f"Exists: {'Yes' if self.primary_config.exists() else 'No'}")
        
        if self.primary_config.exists():
            try:
                stat = self.primary_config.stat()
                print(f"Size: {stat.st_size} bytes")
                print(f"Last modified: {stat.st_mtime}")
            except Exception:
                pass


def main():
    parser = argparse.ArgumentParser(
        description="ConfigureMacKeys - Simple environment variable management for macOS",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  configkeys list                    # List all environment variables
  configkeys list PATH              # List variables containing 'PATH'
  configkeys set GEMINI_API_KEY mykey123  # Set a new variable
  configkeys remove OLD_VAR         # Remove a variable
  configkeys info                   # Show config file location
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List environment variables')
    list_parser.add_argument('filter', nargs='?', help='Filter variables by name pattern')
    
    # Set command  
    set_parser = subparsers.add_parser('set', help='Set an environment variable')
    set_parser.add_argument('name', help='Variable name')
    set_parser.add_argument('value', help='Variable value')
    set_parser.add_argument('--temp', action='store_true', 
                           help='Set only for current session (not permanent)')
    
    # Remove command
    remove_parser = subparsers.add_parser('remove', help='Remove an environment variable')
    remove_parser.add_argument('name', help='Variable name to remove')
    
    # Info command
    info_parser = subparsers.add_parser('info', help='Show configuration file information')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    manager = MacEnvManager()
    
    if args.command == 'list':
        manager.list_env_vars(args.filter)
    elif args.command == 'set':
        manager.set_env_var(args.name, args.value, permanent=not args.temp)
    elif args.command == 'remove':
        manager.remove_env_var(args.name)
    elif args.command == 'info':
        manager.show_config_location()


if __name__ == '__main__':
    main() 