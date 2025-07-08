#!/usr/bin/env python3
"""
Run script for Airline Data Insights backend
"""
import uvicorn
import os
import sys
from pathlib import Path

# Add the app directory to Python path
sys.path.insert(0, str(Path(__file__).parent / "app"))

from config import settings

def main():
    """Main entry point for the application"""
    
    # Configure uvicorn settings
    uvicorn_config = {
        "app": "app.main:app",
        "host": settings.HOST,
        "port": settings.PORT,
        "reload": settings.DEBUG,
        "log_level": settings.LOG_LEVEL.lower(),
        "access_log": True,
    }
    
    # Additional development settings
    if settings.DEBUG:
        uvicorn_config.update({
            "reload_dirs": ["app"],
            "reload_includes": ["*.py"],
            "reload_excludes": ["*.pyc", "__pycache__"],
        })
    
    print(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    print(f"Environment: {'Development' if settings.DEBUG else 'Production'}")
    print(f"Server: http://{settings.HOST}:{settings.PORT}")
    print(f"API Documentation: http://{settings.HOST}:{settings.PORT}/docs")
    print(f"OpenAI API: {'Configured' if settings.OPENAI_API_KEY else 'Not configured (will use mock data)'}")
    
    # Start the server
    try:
        uvicorn.run(**uvicorn_config)
    except KeyboardInterrupt:
        print("\nShutting down server...")
    except Exception as e:
        print(f"Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 