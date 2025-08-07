#!/usr/bin/env python3
"""
Prospect Research Platform - Main Entry Point

This is the primary entry point for the AI agent orchestration platform.
Use this to start the development server or run specific tasks.
"""

import sys
import argparse
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src"))

def start_api_server():
    """Start the FastAPI development server."""
    from prospect_research.api.main import app
    import uvicorn
    from prospect_research.config.settings import settings
    
    print("Starting Prospect Research Platform API Server")
    print(f"Server: http://{settings.api_host}:{settings.api_port}")
    print(f"API Docs: http://{settings.api_host}:{settings.api_port}/docs")
    print("Press Ctrl+C to stop")
    
    uvicorn.run(
        "prospect_research.api.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.environment == "development"
    )

def run_tests():
    """Run the test suite."""
    import pytest
    sys.exit(pytest.main(["-v", "tests/"]))

def main():
    """Main CLI interface."""
    parser = argparse.ArgumentParser(
        description="Prospect Research Platform - AI Agent Orchestration"
    )
    parser.add_argument(
        "command",
        choices=["server", "test", "help"],
        help="Command to run"
    )
    
    args = parser.parse_args()
    
    if args.command == "server":
        start_api_server()
    elif args.command == "test":
        run_tests()
    elif args.command == "help":
        parser.print_help()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()