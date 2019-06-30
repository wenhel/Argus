"""Utils module

Can be used by any other module of the CLI
Determine if python is running in a virtual environment
"""
import sys

if __name__ == "__main__":
    if hasattr(sys, 'real_prefix'):
        sys.exit(0)
    else:
        sys.exit(1)
