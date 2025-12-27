"""
Comprehensive Logging System Tests

Tests for the TASM logging functionality including log entry formatting,
statistics tracking, JSON export, and all log levels.
"""

import pytest
import tempfile
import json
from pathlib import Path
import sys

# Add src to path for testing
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from logger import (
    CompilerLogger, LogLevel, LogEntry, initialize_logger,
    log_info, log_error, log_warning, log_debug, log_abort, log_fatal,
    export_build_summary_json
)


class TestLogEntry:
    """Test LogEntry formatting and creation"""
    
    def test_log_entry_basic_formatting(self):
        """Test basic log entry without location"""
        entry = LogEntry(LogLevel.ERROR, "Test error message")
        formatted = entry.format_entry()
        assert "error: Test error message" in formatted
    
    def test_log_entry_with_location(self):
        """Test log entry with file location"""
        entry = LogEntry(LogLevel.WARNING, "Test warning", file_path="test.py", line_number=42, column=15, error_code="WARN001")
        formatted = entry.format_entry()
        assert "warning: Test warning" in formatted
        assert "WARN001" in formatted
        assert "test.py" in formatted
    
    def test_log_entry_with_file_and_line(self):
        """Test log entry with file and line only"""
        entry = LogEntry(LogLevel.INFO, "Test info", file_path="main.py", line_number=10)
        formatted = entry.format_entry()
        assert "info: Test info" in formatted
    
    def test_log_entry_with_error_code(self):
        """Test log entry with error code"""
        entry = LogEntry(LogLevel.ERROR, "Syntax error", file_path="test.asm", line_number=25, column=10, error_code="SYNTAX_ERROR")
        formatted = entry.format_entry()
        assert "error:" in formatted
        assert "Syntax error" in formatted
        assert "SYNTAX_ERROR" in formatted


class TestCompilerLogger:
    """Test CompilerLogger functionality"""
    
    def test_logger_initialization(self):
        """Test logger can be initialized"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.log') as f:
            log_file = Path(f.name)
        
        try:
            logger = CompilerLogger(log_file, console_output=False)
            assert logger is not None
            assert log_file.exists()
        finally:
            if log_file.exists():
                log_file.unlink()
    
    def test_all_log_levels(self):
        """Test logging all severity levels"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.log') as f:
            log_file = Path(f.name)
        
        try:
            logger = CompilerLogger(log_file, console_output=False)
            
            # Test all log levels
            logger.error("Test error")
            logger.warning("Test warning")
            logger.info("Test info")
            logger.debug("Test debug")
            logger.abort("Test abort")
            logger.fatal("Test fatal")
            
            # Verify statistics
            assert logger.stats[LogLevel.ERROR] == 1
            assert logger.stats[LogLevel.WARNING] == 1
            assert logger.stats[LogLevel.INFO] == 1
            assert logger.stats[LogLevel.DEBUG] == 1
            assert logger.stats[LogLevel.ABORT] == 1
            assert logger.stats[LogLevel.FATAL] == 1
            
            # Verify entries were logged
            assert len(logger.entries) == 6
            
            # Verify log file content
            content = log_file.read_text(encoding='utf-8')
            assert "Test error" in content
            assert "Test warning" in content
            assert "Test info" in content
            
        finally:
            if log_file.exists():
                log_file.unlink()
    
    def test_log_with_location_info(self):
        """Test logging with file location information"""
        logger = CompilerLogger(console_output=False)
        
        logger.error("Syntax error", "test.asm", 42, 15, "SYNTAX_ERROR")
        logger.warning("Unused variable", "main.c", 67, 12, "UNUSED_VAR")
        
        # Check entries contain location info
        assert len(logger.entries) == 2
        assert logger.entries[0].file_path == "test.asm"
        assert logger.entries[0].line_number == 42
        assert logger.entries[0].column == 15
        assert logger.entries[1].file_path == "main.c"
    
    def test_statistics_tracking(self):
        """Test that logger tracks statistics correctly"""
        logger = CompilerLogger(console_output=False)
        
        # Add multiple messages
        for i in range(5):
            logger.error(f"Error {i}")
        for i in range(3):
            logger.warning(f"Warning {i}")
        logger.info("Info message")
        
        # Verify counts
        assert logger.stats[LogLevel.ERROR] == 5
        assert logger.stats[LogLevel.WARNING] == 3
        assert logger.stats[LogLevel.INFO] == 1
        assert logger.stats[LogLevel.DEBUG] == 0
        
        # Verify total
        total = sum(logger.stats.values())
        assert total == 9


class TestJSONExport:
    """Test JSON summary export functionality"""
    
    def test_json_export_basic(self):
        """Test basic JSON export"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            json_file = Path(f.name)
        
        try:
            logger = CompilerLogger(console_output=False)
            
            # Add test entries
            logger.error("Test error", "test.py", 10, error_code="ERR001")
            logger.warning("Test warning", "main.py", 20, error_code="WARN001")
            logger.info("Test info")
            
            # Export JSON
            logger.export_json_summary(json_file)
            
            # Verify file exists and is valid JSON
            assert json_file.exists()
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Check structure
            assert "build_info" in data
            assert "statistics" in data
            assert "entries" in data
            
            # Check statistics (keys are plural forms)
            assert data["statistics"]["errors"] == 1
            assert data["statistics"]["warnings"] == 1
            assert data["statistics"]["info"] == 1
            
        finally:
            if json_file.exists():
                json_file.unlink()
    
    def test_json_export_with_multiple_errors(self):
        """Test JSON export with multiple log entries"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            json_file = Path(f.name)
        
        try:
            logger = CompilerLogger(console_output=False)
            
            # Add multiple entries
            for i in range(10):
                logger.error(f"Error {i}", f"file{i}.asm", i+1)
            for i in range(5):
                logger.warning(f"Warning {i}")
            
            logger.export_json_summary(json_file)
            
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Verify counts
            assert data["statistics"]["errors"] == 10
            assert data["statistics"]["warnings"] == 5
            assert len(data["entries"]) == 15
            
        finally:
            if json_file.exists():
                json_file.unlink()


class TestGlobalLoggerFunctions:
    """Test global logger convenience functions"""
    
    def setup_method(self):
        """Setup test logger"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.log') as f:
            self.log_file = Path(f.name)
        initialize_logger(self.log_file, console_output=False)
    
    def teardown_method(self):
        """Cleanup test files"""
        if self.log_file.exists():
            self.log_file.unlink()
    
    def test_global_log_functions(self):
        """Test global log_* functions"""
        log_error("Global error test")
        log_warning("Global warning test")
        log_info("Global info test")
        log_debug("Global debug test")
        log_abort("Global abort test")
        log_fatal("Global fatal test")
        
        # Verify messages were logged
        content = self.log_file.read_text(encoding='utf-8')
        assert "Global error test" in content
        assert "Global warning test" in content
        assert "Global info test" in content
    
    def test_global_log_with_location(self):
        """Test global log functions with location info"""
        log_error("Error with location", "test.asm", 42, 15, "ERR_CODE")
        log_warning("Warning with location", "main.asm", 67, error_code="WARN_CODE")
        
        content = self.log_file.read_text(encoding='utf-8')
        assert "test.asm" in content
        assert "ERR_CODE" in content
        assert "main.asm" in content


class TestComprehensiveLogging:
    """Comprehensive logging system validation"""
    
    def test_mixed_message_types(self):
        """Test system with mixed message types"""
        logger = CompilerLogger(console_output=False)
        
        # Test basic logging without location
        logger.info("System initialization started")
        logger.debug("Debug mode enabled")
        logger.warning("Low memory warning", error_code="LOW_MEMORY")
        logger.error("Configuration error", error_code="CONFIG_ERROR")
        
        # Test logging with file locations
        logger.error("Syntax error", "parser.py", 142, 25, "SYNTAX_ERROR")
        logger.warning("Unused variable", "utils.py", 67, 12, "UNUSED_VAR")
        logger.info("Function compiled", "data.py", 89)
        
        # Verify statistics
        assert logger.stats[LogLevel.INFO] == 2
        assert logger.stats[LogLevel.DEBUG] == 1
        assert logger.stats[LogLevel.WARNING] == 2
        assert logger.stats[LogLevel.ERROR] == 2
    
    def test_multiple_errors_same_type(self):
        """Test handling of multiple errors of same type"""
        logger = CompilerLogger(console_output=False)
        
        # Multiple errors
        for i in range(10):
            logger.error(f"Validation error #{i+1}", f"file{i+1}.txt", i*10+1, error_code=f"VALID_ERR_{i+1}")
        
        # Multiple warnings
        for i in range(5):
            logger.warning(f"Performance warning #{i+1}", f"module{i+1}.py", (i+1)*20, error_code=f"PERF_WARN_{i+1}")
        
        # Verify counts
        assert logger.stats[LogLevel.ERROR] == 10
        assert logger.stats[LogLevel.WARNING] == 5
        assert len(logger.entries) == 15
    
    def test_edge_cases(self):
        """Test edge cases in logging"""
        logger = CompilerLogger(console_output=False)
        
        # Empty message
        logger.info("")
        assert logger.stats[LogLevel.INFO] == 1
        
        # Very long message
        long_msg = "x" * 1000
        logger.error(long_msg)
        assert logger.stats[LogLevel.ERROR] == 1
        
        # Special characters
        logger.warning("Message with special chars: <>&\"'")
        assert logger.stats[LogLevel.WARNING] == 1
    
    def test_statistics_calculation(self):
        """Test statistics are calculated correctly"""
        logger = CompilerLogger(console_output=False)
        
        # Add various log entries
        logger.error("Error 1")
        logger.error("Error 2")
        logger.warning("Warning 1")
        logger.warning("Warning 2")
        logger.warning("Warning 3")
        logger.info("Info 1")
        logger.debug("Debug 1")
        logger.abort("Abort 1")
        logger.fatal("Fatal 1")
        
        # Check individual stats
        assert logger.stats[LogLevel.ERROR] == 2
        assert logger.stats[LogLevel.WARNING] == 3
        assert logger.stats[LogLevel.INFO] == 1
        assert logger.stats[LogLevel.DEBUG] == 1
        assert logger.stats[LogLevel.ABORT] == 1
        assert logger.stats[LogLevel.FATAL] == 1
        
        # Check total
        total = sum(logger.stats.values())
        assert total == 9
        assert len(logger.entries) == 9


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
