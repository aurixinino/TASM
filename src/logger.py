"""
Compiler-style logging system

This module provides structured logging capabilities that mimic compiler output
with categorized error/warning/info reporting and summary statistics.
"""

import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
import json

class LogLevel(Enum):
    """Log levels matching compiler-style output"""
    ERROR = "error"
    WARNING = "warning" 
    INFO = "info"
    DEBUG = "debug"
    ABORT = "abort"
    FATAL = "fatal"

@dataclass
class LogEntry:
    """Individual log entry with compiler-style formatting"""
    level: LogLevel
    message: str
    file_path: Optional[str] = None
    line_number: Optional[int] = None
    column: Optional[int] = None
    error_code: Optional[str] = None
    source_line: Optional[str] = None  # Copy of the source line where error occurred
    parsed_tokens: Optional[List[str]] = None  # Parsed tokens from the line
    error_token_index: Optional[int] = None  # Index of the token where error occurred
    timestamp: datetime = field(default_factory=datetime.now)
    
    def format_location(self) -> str:
        """Format file location like compiler output"""
        if not self.file_path:
            return ""
        
        location = self.file_path
        if self.line_number:
            location += f":{self.line_number}"
            if self.column:
                location += f":{self.column}"
        return location
    
    def format_entry(self) -> str:
        """Format entry like compiler output with enhanced context information"""
        # Build the main message: level: message [code]
        level_str = self.level.value
        message_parts = [f"{level_str}: {self.message}"]
        
        # Add error code if present
        if self.error_code:
            message_parts.append(f"[{self.error_code}]")
        
        main_message = " ".join(message_parts)
        
        # Add file location for errors/warnings with enhanced context
        show_location = (
            self.file_path and 
            (
                (self.level in [LogLevel.ERROR, LogLevel.WARNING, LogLevel.FATAL, LogLevel.ABORT] and self.line_number) or
                self.source_line or 
                self.parsed_tokens
            )
        )
        
        if show_location:
            location_parts = []
            if self.file_path:
                location_parts.append(f"file: {self.file_path}")
            if self.line_number:
                location_parts.append(f"line {self.line_number}")
                if self.column:
                    location_parts.append(f"col {self.column}")
            
            if location_parts:
                main_message += " - " + " - ".join(location_parts) + ":"
        
        base_message = main_message
        
        # Add enhanced context if available
        context_lines = []
        if self.source_line:
            context_lines.append(f"    Source: {self.source_line.strip()}")
        
        if self.parsed_tokens:
            tokens_str = " | ".join(self.parsed_tokens)
            context_lines.append(f"    Tokens: [{tokens_str}]")
            
            if self.error_token_index is not None and 0 <= self.error_token_index < len(self.parsed_tokens):
                error_token = self.parsed_tokens[self.error_token_index]
                context_lines.append(f"    Error at token #{self.error_token_index + 1}: '{error_token}'")
        
        if context_lines:
            return base_message + "\n" + "\n".join(context_lines)
        
        return base_message

class CompilerLogger:
    """Compiler-style logger with statistics tracking"""
    
    def __init__(self, output_file: Optional[Path] = None, console_output: bool = True, verbosity_level: str = "standard"):
        self.entries: List[LogEntry] = []
        self.output_file = output_file
        self.console_output = console_output
        self.verbosity_level = verbosity_level  # "standard", "info", "verbose", "debug"
        self.start_time = datetime.now()
        
        # Statistics counters
        self.stats = {
            LogLevel.ERROR: 0,
            LogLevel.WARNING: 0,
            LogLevel.INFO: 0,
            LogLevel.DEBUG: 0,
            LogLevel.ABORT: 0,
            LogLevel.FATAL: 0
        }
        
        # Setup file logging if specified and clear any existing log
        if self.output_file:
            self.output_file.parent.mkdir(parents=True, exist_ok=True)
            # Clear the log file at the start of each compilation
            with open(self.output_file, 'w', encoding='utf-8') as f:
                f.write(f"=== TASM Build Log - {self.start_time.strftime('%Y-%m-%d %H:%M:%S')} ===\n")
    
    def _should_show_in_console(self, level: LogLevel) -> bool:
        """Determine if a log entry should be shown in console based on verbosity level"""
        import os
        
        # Check for quiet mode environment variable (used by test_encoder_validation.py)
        if os.environ.get('TASM_QUIET_MODE') == '1':
            # In quiet mode, suppress all console output
            return False
        
        if self.verbosity_level == "verbose":
            # Verbose: show all messages except debug
            return level in [LogLevel.INFO, LogLevel.WARNING, LogLevel.ERROR, LogLevel.ABORT, LogLevel.FATAL]
        elif self.verbosity_level == "debug":
            # Debug: show all messages including debug
            return True
        elif self.verbosity_level == "info":
            # Info: show info + warnings + errors + aborts + fatal
            return level in [LogLevel.INFO, LogLevel.WARNING, LogLevel.ERROR, LogLevel.ABORT, LogLevel.FATAL]
        else:
            # Standard: show only errors and aborts (quiet console)
            return level in [LogLevel.ERROR, LogLevel.ABORT, LogLevel.FATAL]
    
    def log(self, level: LogLevel, message: str, file_path: Optional[str] = None, 
            line_number: Optional[int] = None, column: Optional[int] = None,
            error_code: Optional[str] = None, source_line: Optional[str] = None,
            parsed_tokens: Optional[List[str]] = None, error_token_index: Optional[int] = None) -> None:
        """Log an entry with compiler-style formatting and enhanced context"""
        
        entry = LogEntry(
            level=level,
            message=message,
            file_path=file_path,
            line_number=line_number,
            column=column,
            error_code=error_code,
            source_line=source_line,
            parsed_tokens=parsed_tokens,
            error_token_index=error_token_index
        )
        
        self.entries.append(entry)
        self.stats[level] += 1
        
        # Format and output
        formatted_entry = entry.format_entry()
        
        if self.console_output and self._should_show_in_console(level):
            # Color coding for different levels
            color_codes = {
                LogLevel.ERROR: '\033[91m',    # Red
                LogLevel.FATAL: '\033[91m',    # Red
                LogLevel.ABORT: '\033[91m',    # Red
                LogLevel.WARNING: '\033[93m',  # Yellow
                LogLevel.INFO: '\033[92m',     # Green
                LogLevel.DEBUG: '\033[94m'     # Blue
            }
            reset_code = '\033[0m'
            
            color = color_codes.get(level, '')
            print(f"{color}{formatted_entry}{reset_code}")
        
        if self.output_file:
            with open(self.output_file, 'a', encoding='utf-8') as f:
                f.write(f"{entry.timestamp.strftime('%Y-%m-%d %H:%M:%S')} - {formatted_entry}\n")
    
    def error(self, message: str, file_path: Optional[str] = None, 
              line_number: Optional[int] = None, column: Optional[int] = None,
              error_code: Optional[str] = None, source_line: Optional[str] = None,
              parsed_tokens: Optional[List[str]] = None, error_token_index: Optional[int] = None) -> None:
        """Log an error with enhanced context"""
        self.log(LogLevel.ERROR, message, file_path, line_number, column, error_code, 
                source_line, parsed_tokens, error_token_index)
    
    def warning(self, message: str, file_path: Optional[str] = None,
                line_number: Optional[int] = None, column: Optional[int] = None,
                error_code: Optional[str] = None) -> None:
        """Log a warning"""
        self.log(LogLevel.WARNING, message, file_path, line_number, column, error_code)
    
    def info(self, message: str, file_path: Optional[str] = None,
             line_number: Optional[int] = None, column: Optional[int] = None,
             error_code: Optional[str] = None) -> None:
        """Log an info message"""
        self.log(LogLevel.INFO, message, file_path, line_number, column, error_code)
    
    def debug(self, message: str, file_path: Optional[str] = None,
              line_number: Optional[int] = None, column: Optional[int] = None,
              error_code: Optional[str] = None) -> None:
        """Log a debug message"""
        self.log(LogLevel.DEBUG, message, file_path, line_number, column, error_code)
    
    def abort(self, message: str, file_path: Optional[str] = None,
              line_number: Optional[int] = None, column: Optional[int] = None,
              error_code: Optional[str] = None) -> None:
        """Log an abort message"""
        self.log(LogLevel.ABORT, message, file_path, line_number, column, error_code)
    
    def fatal(self, message: str, file_path: Optional[str] = None,
              line_number: Optional[int] = None, column: Optional[int] = None,
              error_code: Optional[str] = None) -> None:
        """Log a fatal error"""
        self.log(LogLevel.FATAL, message, file_path, line_number, column, error_code)
    
    def print_summary(self) -> None:
        """Print compiler-style summary"""
        end_time = datetime.now()
        duration = end_time - self.start_time
        
        # Calculate totals - don't count aborts as errors
        total_errors = self.stats[LogLevel.ERROR] + self.stats[LogLevel.FATAL]
        total_warnings = self.stats[LogLevel.WARNING]
        total_messages = sum(self.stats.values())
        
        print("\n" + "="*60)
        print("COMPILATION SUMMARY")
        print("="*60)
        print(f"Build started: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Build finished: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Duration: {duration.total_seconds():.2f} seconds")
        print()
        
        # Detailed statistics
        print("STATISTICS:")
        print(f"  Errors:   {self.stats[LogLevel.ERROR]:>6}")
        print(f"  Warnings: {self.stats[LogLevel.WARNING]:>6}")
        print(f"  Info:     {self.stats[LogLevel.INFO]:>6}")
        print(f"  Debug:    {self.stats[LogLevel.DEBUG]:>6}")
        print(f"  Aborts:   {self.stats[LogLevel.ABORT]:>6}")
        print(f"  Fatal:    {self.stats[LogLevel.FATAL]:>6}")
        print(f"  Total:    {total_messages:>6}")
        print()
        
        # Build result - consider both errors and aborts for failure
        total_failures = total_errors + self.stats[LogLevel.ABORT]
        if total_failures > 0:
            status = "FAILED"
            color = '\033[91m'  # Red
        elif total_warnings > 0:
            status = "SUCCEEDED WITH WARNINGS"
            color = '\033[93m'  # Yellow
        else:
            status = "SUCCEEDED"
            color = '\033[92m'  # Green
        
        reset_code = '\033[0m'
        print(f"BUILD {color}{status}{reset_code}")
        
        if total_errors > 0:
            print(f"{total_errors} error(s), {total_warnings} warning(s)")
        elif total_warnings > 0:
            print(f"0 error(s), {total_warnings} warning(s)")
        else:
            print("0 error(s), 0 warning(s)")
        
        print("="*60)
        
        # Write summary to file if specified
        if self.output_file:
            self.write_summary_to_file(duration, total_errors, total_warnings, total_messages)
    
    def write_summary_to_file(self, duration, total_errors: int, total_warnings: int, total_messages: int) -> None:
        """Write summary to log file"""
        with open(self.output_file, 'a', encoding='utf-8') as f:
            f.write(f"\n{'='*60}\n")
            f.write(f"COMPILATION SUMMARY\n")
            f.write(f"{'='*60}\n")
            f.write(f"Build started: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Build finished: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Duration: {duration.total_seconds():.2f} seconds\n\n")
            
            f.write(f"STATISTICS:\n")
            f.write(f"  Errors:   {self.stats[LogLevel.ERROR]:>6}\n")
            f.write(f"  Warnings: {self.stats[LogLevel.WARNING]:>6}\n")
            f.write(f"  Info:     {self.stats[LogLevel.INFO]:>6}\n")
            f.write(f"  Debug:    {self.stats[LogLevel.DEBUG]:>6}\n")
            f.write(f"  Aborts:   {self.stats[LogLevel.ABORT]:>6}\n")
            f.write(f"  Fatal:    {self.stats[LogLevel.FATAL]:>6}\n")
            f.write(f"  Total:    {total_messages:>6}\n\n")
            
            # Use same logic as print_summary for consistency
            total_failures = total_errors + self.stats[LogLevel.ABORT]
            if total_failures > 0:
                status = "FAILED"
            elif total_warnings > 0:
                status = "SUCCEEDED WITH WARNINGS"
            else:
                status = "SUCCEEDED"
            
            f.write(f"BUILD {status}\n")
            f.write(f"{total_errors} error(s), {total_warnings} warning(s)\n")
            f.write(f"{'='*60}\n")
    
    def export_json_summary(self, json_file: Path) -> None:
        """Export summary as JSON for programmatic access"""
        summary = {
            "build_info": {
                "start_time": self.start_time.isoformat(),
                "end_time": datetime.now().isoformat(),
                "duration_seconds": (datetime.now() - self.start_time).total_seconds()
            },
            "statistics": {
                "errors": self.stats[LogLevel.ERROR],
                "warnings": self.stats[LogLevel.WARNING],
                "info": self.stats[LogLevel.INFO],
                "debug": self.stats[LogLevel.DEBUG],
                "aborts": self.stats[LogLevel.ABORT],
                "fatal": self.stats[LogLevel.FATAL],
                "total": sum(self.stats.values())
            },
            "entries": [
                {
                    "level": entry.level.value,
                    "message": entry.message,
                    "file_path": entry.file_path,
                    "line_number": entry.line_number,
                    "column": entry.column,
                    "error_code": entry.error_code,
                    "timestamp": entry.timestamp.isoformat()
                }
                for entry in self.entries
            ]
        }
        
        json_file.parent.mkdir(parents=True, exist_ok=True)
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)

# Global logger instance
_global_logger: Optional[CompilerLogger] = None

def initialize_logger(output_file: Optional[Path] = None, console_output: bool = True, verbosity_level: str = "standard") -> CompilerLogger:
    """Initialize the global logger"""
    global _global_logger
    _global_logger = CompilerLogger(output_file, console_output, verbosity_level)
    return _global_logger

def get_logger() -> CompilerLogger:
    """Get the global logger instance"""
    global _global_logger
    if _global_logger is None:
        _global_logger = CompilerLogger()
    return _global_logger

# Convenience functions for global logger
def log_error(message: str, file_path: Optional[str] = None, 
              line_number: Optional[int] = None, column: Optional[int] = None,
              error_code: Optional[str] = None) -> None:
    """Log an error using global logger"""
    get_logger().error(message, file_path, line_number, column, error_code)

def log_warning(message: str, file_path: Optional[str] = None,
                line_number: Optional[int] = None, column: Optional[int] = None,
                error_code: Optional[str] = None) -> None:
    """Log a warning using global logger"""
    get_logger().warning(message, file_path, line_number, column, error_code)

def log_info(message: str, file_path: Optional[str] = None,
             line_number: Optional[int] = None, column: Optional[int] = None,
             error_code: Optional[str] = None) -> None:
    """Log an info message using global logger"""
    get_logger().info(message, file_path, line_number, column, error_code)

def log_debug(message: str, file_path: Optional[str] = None,
              line_number: Optional[int] = None, column: Optional[int] = None,
              error_code: Optional[str] = None) -> None:
    """Log a debug message using global logger"""
    get_logger().debug(message, file_path, line_number, column, error_code)

def log_abort(message: str, file_path: Optional[str] = None,
              line_number: Optional[int] = None, column: Optional[int] = None,
              error_code: Optional[str] = None) -> None:
    """Log an abort message using global logger"""
    get_logger().abort(message, file_path, line_number, column, error_code)

def log_fatal(message: str, file_path: Optional[str] = None,
              line_number: Optional[int] = None, column: Optional[int] = None,
              error_code: Optional[str] = None) -> None:
    """Log a fatal error using global logger"""
    get_logger().fatal(message, file_path, line_number, column, error_code)

def print_build_summary() -> None:
    """Print build summary using global logger"""
    get_logger().print_summary()

def export_build_summary_json(json_file: Path) -> None:
    """Export build summary as JSON using global logger"""
    get_logger().export_json_summary(json_file)