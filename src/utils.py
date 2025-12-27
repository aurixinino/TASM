"""
Utility functions and helpers

This module contains common utility functions that can be used
across the application.
"""

import logging
from datetime import datetime
from pathlib import Path
from config_loader import get_config

def setup_logging(log_level=logging.INFO, log_file=None):
    """
    Set up logging configuration.
    
    Args:
        log_level: Logging level (default: INFO)
        log_file: Optional log file path
    """
    format_str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    if log_file:
        logging.basicConfig(
            level=log_level,
            format=format_str,
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
    else:
        logging.basicConfig(level=log_level, format=format_str)

def get_project_root() -> Path:
    """Get the project root directory."""
    return Path(__file__).parent.parent

def create_output_dir(name: str = None, override_path: str = None) -> Path:
    """
    Create an output directory with fixed name (no timestamp).
    
    Args:
        name: Base name for the directory (optional, uses config default if None)
        override_path: Override path from command-line (absolute or relative to project root)
        
    Returns:
        Path to the created directory
    """
    if override_path:
        # Command-line override takes precedence
        output_path = Path(override_path)
        if not output_path.is_absolute():
            output_dir = get_project_root() / output_path
        else:
            output_dir = output_path
    elif name:
        # Use specified name with legacy "output" directory
        output_dir = get_project_root() / "output" / name
    else:
        # Use configured default output directory
        config = get_config()
        config_path = config.output_dir_path
        output_dir = get_project_root() / config_path
    
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir

def create_output_dir_with_timestamp(name: str = None, override_path: str = None) -> Path:
    """
    Create an output directory with timestamp (legacy function).
    
    Args:
        name: Base name for the directory (optional, uses config default if None)
        override_path: Override path from command-line (will append timestamp)
        
    Returns:
        Path to the created directory
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    if override_path:
        # Command-line override with timestamp
        base_path = Path(override_path)
        if not base_path.is_absolute():
            output_dir = get_project_root() / f"{base_path}_{timestamp}"
        else:
            output_dir = Path(f"{base_path}_{timestamp}")
    elif name:
        # Use specified name with legacy "output" directory
        output_dir = get_project_root() / "output" / f"{name}_{timestamp}"
    else:
        # Use configured default with timestamp
        config = get_config()
        config_path = config.output_dir_path
        output_dir = get_project_root() / f"{config_path}_{timestamp}"
    
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir

def load_data_file(filename: str) -> Path:
    """
    Get path to a data file.
    
    Args:
        filename: Name of the data file
        
    Returns:
        Path to the data file
    """
    data_path = get_project_root() / "data" / filename
    if not data_path.exists():
        raise FileNotFoundError(f"Data file not found: {data_path}")
    return data_path