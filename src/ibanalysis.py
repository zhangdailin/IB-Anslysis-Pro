"""
Modern IB Analysis toolkit entry point.

This module provides backward compatibility with the original interface
while using the new modular architecture underneath.
"""

import sys
import warnings
from pathlib import Path

# Import new CLI
from ib_analysis.cli import cli_main
from ib_analysis.legacy import LegacyOperationManager, process_command, setup_argparse

def main():
    """
    Main entry point that provides backward compatibility.
    
    This function detects if the new CLI should be used or if we need
    to fall back to legacy compatibility mode.
    """
    
    # Check if we're being called with the new CLI syntax
    if len(sys.argv) > 1:
        first_arg = sys.argv[1]
        
        # If first argument is a known command from the new CLI, use new interface
        new_cli_commands = ['analyze', 'interactive', 'operations', 'version', '--help', '-h']
        if first_arg in new_cli_commands:
            cli_main()
            return
        
        # If it looks like the old format, show deprecation warning and use legacy
        if first_arg in ['-op', '--interactive'] or first_arg.startswith('-'):
            warnings.warn(
                "The legacy command-line interface is deprecated. "
                "Please use the new 'iba' command. Run 'iba --help' for usage information.",
                DeprecationWarning,
                stacklevel=2
            )
            
            # Use legacy argument parsing for backward compatibility
            try:
                from ib_analysis.legacy import setup_argparse
                arg_parser = setup_argparse()
                args = arg_parser.parse_args()
                
                if args.interactive:
                    # Use new interactive mode
                    from ib_analysis.core.interactive import InteractiveSession
                    from ib_analysis.config import get_config
                    from rich.console import Console
                    
                    config = get_config()
                    console = Console()
                    session = InteractiveSession(config, console)
                    session.run(
                        default_dir_a=Path(args.dir_a) if args.dir_a else None,
                        default_dir_b=Path(args.dir_b) if args.dir_b else None,
                    )
                else:
                    # Use legacy operation processing
                    exit_code = process_command(args)
                    sys.exit(exit_code)
                    
            except Exception as e:
                print(f"Error in legacy mode: {e}", file=sys.stderr)
                sys.exit(1)
        else:
            # Assume it's a directory path in the old format
            warnings.warn(
                "Positional directory arguments are deprecated. "
                "Use 'iba analyze <operation> <directory>' instead.",
                DeprecationWarning,
                stacklevel=2
            )
            
            # Try to parse as legacy format
            print("Legacy format detected. Use 'iba --help' for new syntax.")
            sys.exit(1)
    else:
        # No arguments provided, show help for new CLI
        cli_main()


if __name__ == "__main__":
    main()
