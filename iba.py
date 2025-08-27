#!/usr/bin/env python3
"""
Entry point for IB Analysis toolkit.

This script provides backward compatibility with the original interface
while directing users to the new CLI.
"""

import sys
import warnings
from src.ib_analysis.cli import cli_main

def main():
    """Main entry point with backward compatibility."""
    
    # Show deprecation warning for this entry point
    warnings.warn(
        "Using 'iba.py' is deprecated. Use 'iba' command directly or 'python -m ib_analysis'.",
        DeprecationWarning,
        stacklevel=2
    )
    
    # Use the new CLI
    cli_main()

if __name__ == '__main__':
    main()
