"""
Configuration loader for TASM assembler.
Loads and provides access to configuration settings from tasm_config.json.
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional


class TASMConfig:
    """Configuration manager for TASM assembler."""
    
    _instance: Optional['TASMConfig'] = None
    _config: Dict[str, Any] = {}
    _custom_config_path: Optional[Path] = None
    
    def __new__(cls):
        """Singleton pattern - ensure only one config instance exists."""
        if cls._instance is None:
            cls._instance = super(TASMConfig, cls).__new__(cls)
            cls._instance._load_config()
        return cls._instance
    
    def _load_config(self, custom_path: Optional[Path] = None) -> None:
        """
        Load configuration from JSON file.
        
        Args:
            custom_path: Optional custom path to config file. If None, uses default location.
        """
        # Use custom path if provided, otherwise use default
        if custom_path:
            config_path = Path(custom_path)
        elif self._custom_config_path:
            config_path = self._custom_config_path
        else:
            # Find config file - look in project root/config directory
            current_dir = Path(__file__).parent
            project_root = current_dir.parent
            config_path = project_root / "config" / "tasm_config.json"
        
        if not config_path.exists():
            raise FileNotFoundError(
                f"Configuration file not found: {config_path}\n"
                f"Please create config/tasm_config.json in the project root or specify a custom config file."
            )
        
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                self._config = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in configuration file: {e}")
    
    def get(self, *keys: str, default: Any = None) -> Any:
        """
        Get a configuration value using dot notation.
        
        Examples:
            config.get('architecture', 'endianness')  -> 'little'
            config.get('paths', 'pdf_manual')  -> 'C:\\...'
        
        Args:
            *keys: Path to the configuration value
            default: Default value if key not found
            
        Returns:
            Configuration value or default
        """
        value = self._config
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        return value
    
    # Convenience properties for commonly used settings
    
    @property
    def is_little_endian(self) -> bool:
        """Check if architecture is little-endian."""
        return self.get('architecture', 'endianness', default='little').lower() == 'little'
    
    @property
    def is_big_endian(self) -> bool:
        """Check if architecture is big-endian."""
        return not self.is_little_endian
    
    @property
    def word_size(self) -> int:
        """Get architecture word size (16 or 32 bits)."""
        return self.get('architecture', 'word_size', default=32)
    
    @property
    def pdf_manual_path(self) -> str:
        """Get path to PDF manual."""
        return self.get('paths', 'pdf_manual', default='')
    
    @property
    def instruction_set_path(self) -> str:
        """Get path to instruction set Excel file."""
        return self.get('paths', 'instruction_set', default='')
    
    @property
    def output_dir_path(self) -> str:
        """Get default output directory path (relative to project root)."""
        return self.get('paths', 'output_dir', default='output/assembly_build')
    
    @property
    def generate_lst(self) -> bool:
        """Check if LST file generation is enabled."""
        return self.get('output', 'generate_lst', default=True)
    
    @property
    def generate_bin(self) -> bool:
        """Check if BIN file generation is enabled."""
        return self.get('output', 'generate_bin', default=True)
    
    @property
    def generate_hex(self) -> bool:
        """Check if HEX file generation is enabled."""
        return self.get('output', 'generate_hex', default=True)
    
    @property
    def generate_map(self) -> bool:
        """Check if MAP file generation is enabled."""
        return self.get('output', 'generate_map', default=True)
    
    def reload(self, custom_path: Optional[Path] = None) -> None:
        """
        Reload configuration from file.
        
        Args:
            custom_path: Optional custom path to config file.
        """
        self._load_config(custom_path)
    
    @classmethod
    def set_custom_config_path(cls, config_path: Path) -> None:
        """
        Set a custom configuration file path before first instantiation.
        Must be called before get_config() for the first time.
        
        Args:
            config_path: Path to custom configuration file.
        """
        if cls._instance is not None:
            # Already instantiated, reload with new path
            cls._instance._custom_config_path = Path(config_path)
            cls._instance._load_config(Path(config_path))
        else:
            # Not yet instantiated, set for future use
            cls._custom_config_path = Path(config_path)


# Global configuration instance
def get_config() -> TASMConfig:
    """Get the global configuration instance."""
    return TASMConfig()


def set_config_path(config_path: str) -> None:
    """
    Set custom configuration file path.
    
    Args:
        config_path: Path to custom configuration file.
    """
    TASMConfig.set_custom_config_path(Path(config_path))
