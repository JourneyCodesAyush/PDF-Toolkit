# Entry point script to initialize and run the PDF Toolkit CLI application

"""
Entry point script to initialize and run the PDF Toolkit CLI application.

This script imports and invokes the main CLI handler, serving as the
executable entry point when running the application from the command line.
"""

from cli.__main__ import main

if __name__ == "__main__":
    main()
