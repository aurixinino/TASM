"""
Macro Expander Module

This module handles macro definition parsing and expansion in assembly source code.
It processes #define directives and expands macro calls throughout the source.
"""

import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Set, Union
from dataclasses import dataclass

from logger import log_info, log_error, log_warning, log_debug, log_abort, get_logger

@dataclass
class Macro:
    """Represents a macro definition"""
    name: str
    parameters: List[str]
    body: str
    line_defined: int
    file_defined: str
    is_function_like: bool = False  # True if defined with (), even if no params

class MacroExpander:
    """Handles macro definitions and expansions"""
    
    def __init__(self):
        self.macros: Dict[str, Macro] = {}
        self.expansion_depth = 0
        self.max_expansion_depth = 10
        self.current_file = ""
        self.macro_counter = 0  # Counter for unique label generation
        
    def process_file(self, input_file: Path, output_file: Path) -> bool:
        """
        Process assembly file for macro definitions and expansions
        
        Args:
            input_file: Source assembly file
            output_file: Output file with macros expanded
            
        Returns:
            True if successful, False if errors occurred
        """
        self.current_file = str(input_file)
        log_info(f"Starting macro expansion for {input_file.name}", str(input_file))
        
        try:
            # Read source file
            if not input_file.exists():
                log_error(f"Source file not found: {input_file.name}", 
                         str(input_file), error_code="FILE_NOT_FOUND")
                return False
            
            with open(input_file, 'r', encoding='utf-8') as f:
                source_lines = f.readlines()
            
            log_info(f"Read {len(source_lines)} lines from source file", str(input_file))
            
            # First pass: collect macro definitions
            if not self._collect_macros(source_lines):
                return False
            
            # Second pass: expand macros
            expanded_lines = self._expand_macros(source_lines)
            if expanded_lines is None:
                return False
            
            # Write expanded output
            output_file.parent.mkdir(parents=True, exist_ok=True)
            with open(output_file, 'w', encoding='utf-8') as f:
                f.writelines(expanded_lines)
            
            log_info(f"Macro expansion completed successfully", str(output_file))
            log_info(f"Generated {len(expanded_lines)} lines of expanded code")
            
            return True
            
        except Exception as e:
            log_error(f"Unexpected error during macro expansion: {str(e)}", 
                     str(input_file), error_code="MACRO_EXPANSION_ERROR")
            return False
    
    def process_macro_file(self, macro_file: Path) -> bool:
        """
        Process a macro file to collect macro definitions only
        
        Args:
            macro_file: Path to macro file containing macro definitions
            
        Returns:
            True if successful, False otherwise
        """
        log_info(f"Processing macro file: {macro_file.name}", str(macro_file))
        
        try:
            # Check if macro file exists
            if not macro_file.exists():
                log_error(f"Macro file not found: {macro_file.name}", 
                         str(macro_file), error_code="MACRO_FILE_NOT_FOUND")
                return False
            
            # Read macro file
            with open(macro_file, 'r', encoding='utf-8') as f:
                macro_lines = f.readlines()
            
            log_debug(f"Read {len(macro_lines)} lines from macro file", str(macro_file))
            
            # Collect macro definitions from this file
            initial_macro_count = len(self.macros)
            
            if not self._collect_macros(macro_lines):
                log_abort(f"Failed to collect macros from: {macro_file.name}",
                         str(macro_file), error_code="MACRO_COLLECTION_FAILED")
                log_error(f"Check the macro definitions in {macro_file.name} for syntax errors")
                log_info(f"Macro file contains {len(macro_lines)} lines")
                
                # Show problematic lines for debugging
                for i, line in enumerate(macro_lines, 1):
                    if line.strip().startswith('#define'):
                        log_debug(f"Line {i}: {line.strip()}")
                
                return False
            
            new_macro_count = len(self.macros) - initial_macro_count
            log_info(f"Loaded {new_macro_count} macro definitions from {macro_file.name}")
            
            return True
            
        except Exception as e:
            log_error(f"Error processing macro file {macro_file.name}: {str(e)}", 
                     str(macro_file), error_code="MACRO_FILE_ERROR")
            return False
    
    def _collect_macros(self, source_lines: List[str]) -> bool:
        """Collect macro definitions from source"""
        log_debug("Collecting macro definitions")
        
        macro_count = 0
        
        for line_num, line in enumerate(source_lines, 1):
            line = line.strip()
            
            # Skip empty lines and comments
            if not line or line.startswith(';'):
                continue
            
            # Check for macro definition
            if line.startswith('#define'):
                if not self._parse_macro_definition(line, line_num):
                    return False
                macro_count += 1
        
        log_info(f"Found {macro_count} macro definitions")
        
        # Log macro details
        for macro_name, macro in self.macros.items():
            if macro.parameters:
                log_debug(f"Macro '{macro_name}({', '.join(macro.parameters)})' defined at line {macro.line_defined}")
            else:
                log_debug(f"Macro '{macro_name}' defined at line {macro.line_defined}")
        
        return True
    
    def _parse_macro_definition(self, line: str, line_num: int) -> bool:
        """Parse a macro definition line"""
        log_debug(f"Parsing macro definition at line {line_num}: {line.strip()}")
        # Pattern: #define MACRO_NAME(param1, param2) body
        # or: #define MACRO_NAME body
        
        parts = line[7:].strip()  # Remove '#define'
        
        if not parts:
            log_error("Empty macro definition", self.current_file, line_num, error_code="EMPTY_MACRO")
            return False
        
        # Check for parameterized macro
        is_function_like = False
        if '(' in parts:
            # Parameterized macro (function-like)
            is_function_like = True
            paren_pos = parts.find('(')
            macro_name = parts[:paren_pos].strip()
            
            if not macro_name:
                log_error("Missing macro name", self.current_file, line_num, error_code="MISSING_MACRO_NAME")
                return False
            
            # Extract parameters
            close_paren = parts.find(')', paren_pos)
            if close_paren == -1:
                log_error("Missing closing parenthesis in macro definition", 
                         self.current_file, line_num, error_code="MISSING_PAREN")
                return False
            
            param_str = parts[paren_pos+1:close_paren].strip()
            parameters = []
            
            if param_str:
                parameters = [p.strip() for p in param_str.split(',')]
                # Validate parameter names
                for param in parameters:
                    if not param.isidentifier():
                        log_error(f"Invalid parameter name: '{param}'", 
                                 self.current_file, line_num, error_code="INVALID_PARAM_NAME")
                        return False
            
            macro_body = parts[close_paren+1:].strip()
            
        else:
            # Simple macro (object-like)
            space_pos = parts.find(' ')
            if space_pos == -1:
                # Macro without body
                macro_name = parts
                macro_body = ""
            else:
                macro_name = parts[:space_pos]
                macro_body = parts[space_pos+1:]
            
            parameters = []
        
        # Validate macro name - allow more flexible naming for assembly macros
        # Assembly macro names can include brackets, dots, etc.
        if not macro_name or macro_name.isspace():
            log_error(f"Invalid or empty macro name: '{macro_name}'", 
                     self.current_file, line_num, error_code="INVALID_MACRO_NAME")
            return False
        
        # Check for obviously problematic characters that would break parsing
        invalid_chars = ['\n', '\r', '\t', '#']
        for char in invalid_chars:
            if char in macro_name:
                log_error(f"Invalid character '{repr(char)}' in macro name: '{macro_name}'", 
                         self.current_file, line_num, error_code="INVALID_MACRO_NAME")
                return False
        
        # Check for redefinition
        if macro_name in self.macros:
            log_warning(f"Macro '{macro_name}' redefined", 
                       self.current_file, line_num, error_code="MACRO_REDEFINITION")
            log_debug(f"Previous definition was at line {self.macros[macro_name].line_defined}")
        
        # Store macro
        self.macros[macro_name] = Macro(
            name=macro_name,
            parameters=parameters,
            body=macro_body,
            line_defined=line_num,
            file_defined=self.current_file,
            is_function_like=is_function_like
        )
        
        log_debug(f"Defined macro '{macro_name}' at line {line_num}")
        return True
    
    def _expand_macros(self, source_lines: List[str]) -> Optional[List[str]]:
        """Expand all macro calls in the source"""
        log_debug("Expanding macro calls")
        
        expanded_lines = []
        expansion_count = 0
        
        for line_num, line in enumerate(source_lines, 1):
            # Skip macro definitions in output
            if line.strip().startswith('#define'):
                log_debug(f"Skipping macro definition at line {line_num}")
                continue
            
            expanded_line = self._expand_line(line, line_num)
            if expanded_line is None:
                return None
            
            if expanded_line != line:
                expansion_count += 1
                log_debug(f"Expanded macro at line {line_num}")
                log_debug(f"Result: {repr(expanded_line[:100])}")  # Debug output
            
            # Split expanded line on pipe character for multi-statement macros
            if '|' in expanded_line:
                log_debug(f"Splitting line with pipes: {repr(expanded_line[:100])}")  # Debug
                # Preserve leading whitespace from original line
                leading_space = len(line) - len(line.lstrip())
                indent = line[:leading_space]
                
                parts = expanded_line.split('|')
                log_debug(f"Split into {len(parts)} parts")  # Debug
                for part in parts:
                    stripped = part.strip()
                    if stripped:  # Only add non-empty parts
                        # Ensure each part ends with newline
                        if not stripped.endswith('\n'):
                            stripped += '\n'
                        expanded_lines.append(indent + stripped)
            else:
                expanded_lines.append(expanded_line)
        
        log_info(f"Performed {expansion_count} macro expansions")
        return expanded_lines
    
    def _expand_line(self, line: str, line_num: int) -> Optional[str]:
        """Expand macros in a single line"""
        self.expansion_depth = 0
        return self._expand_line_recursive(line, line_num)
    
    def _expand_line_recursive(self, line: str, line_num: int) -> Optional[str]:
        """Recursively expand macros in a line"""
        self.expansion_depth += 1
        
        if self.expansion_depth > self.max_expansion_depth:
            log_error(f"Maximum macro expansion depth exceeded ({self.max_expansion_depth})", 
                     self.current_file, line_num, error_code="MACRO_RECURSION")
            return None
        
        original_line = line
        
        # Find macro calls in the line
        for macro_name, macro in self.macros.items():
            if macro.is_function_like:
                # Function-like macro call (with parentheses)
                pattern = rf'\b{re.escape(macro_name)}\s*\('
                matches = list(re.finditer(pattern, line))
                
                for match in reversed(matches):  # Process from right to left
                    start_pos = match.start()
                    
                    # Find matching closing parenthesis
                    paren_count = 0
                    pos = match.end() - 1  # Start at opening paren
                    end_pos = -1
                    
                    for i in range(pos, len(line)):
                        if line[i] == '(':
                            paren_count += 1
                        elif line[i] == ')':
                            paren_count -= 1
                            if paren_count == 0:
                                end_pos = i
                                break
                    
                    if end_pos == -1:
                        log_error(f"Missing closing parenthesis for macro call '{macro_name}'", 
                                 self.current_file, line_num, error_code="MISSING_MACRO_PAREN")
                        return None
                    
                    # Extract arguments
                    args_str = line[match.end():end_pos]
                    args = self._parse_macro_arguments(args_str, line_num)
                    if args is None:
                        return None
                    
                    if len(args) != len(macro.parameters):
                        log_error(f"Macro '{macro_name}' expects {len(macro.parameters)} arguments, got {len(args)}", 
                                 self.current_file, line_num, error_code="WRONG_MACRO_ARGS")
                        return None
                    
                    # Expand macro
                    expanded = self._substitute_macro_parameters(macro, args)
                    
                    # Increment counter for unique label generation
                    self.macro_counter += 1
                    
                    # Replace special tokens (__COUNTER__, __UNIQUE__)
                    expanded = self._replace_special_tokens(expanded)
                    
                    # Process token concatenation (##) AFTER all substitutions
                    expanded = self._process_token_concatenation(expanded)
                    
                    # Replace in line
                    line = line[:start_pos] + expanded + line[end_pos+1:]
            
            else:
                # Simple macro replacement
                pattern = rf'\b{re.escape(macro_name)}\b'
                line = re.sub(pattern, macro.body, line)
                
                # Also increment counter and replace special tokens for simple macros
                if '__COUNTER__' in macro.body or '__UNIQUE__' in macro.body:
                    self.macro_counter += 1
                    line = self._replace_special_tokens(line)
        
        # If line changed, try expanding again (for nested macros)
        if line != original_line:
            return self._expand_line_recursive(line, line_num)
        
        return line
    
    def _parse_macro_arguments(self, args_str: str, line_num: int) -> Optional[List[str]]:
        """Parse macro call arguments with support for quoted strings"""
        if not args_str.strip():
            return []
        
        args = []
        current_arg = ""
        paren_depth = 0
        in_single_quote = False
        in_double_quote = False
        
        for i, char in enumerate(args_str):
            # Handle quote toggles
            if char == "'" and not in_double_quote:
                in_single_quote = not in_single_quote
                # Don't include the quote in the argument
                continue
            elif char == '"' and not in_single_quote:
                in_double_quote = not in_double_quote
                # Don't include the quote in the argument
                continue
            
            # Only split on commas outside quotes and parentheses
            if char == ',' and paren_depth == 0 and not in_single_quote and not in_double_quote:
                args.append(current_arg.strip())
                current_arg = ""
            else:
                if char == '(' and not in_single_quote and not in_double_quote:
                    paren_depth += 1
                elif char == ')' and not in_single_quote and not in_double_quote:
                    paren_depth -= 1
                current_arg += char
        
        if current_arg.strip():
            args.append(current_arg.strip())
        
        return args
    
    def _substitute_macro_parameters(self, macro: Macro, args: List[str]) -> str:
        """Substitute parameters in macro body (without token concatenation)"""
        result = macro.body
        
        # Substitute parameters
        for param, arg in zip(macro.parameters, args):
            # Replace parameter with argument (whole word only)
            pattern = rf'\b{re.escape(param)}\b'
            result = re.sub(pattern, arg, result)
        
        return result
    
    def _process_token_concatenation(self, text: str) -> str:
        """Process ## token concatenation operator"""
        # Replace ## with direct concatenation (remove spaces around ##)
        # Pattern: token1 ## token2 -> token1token2
        before = text
        result = re.sub(r'\s*##\s*', '', text)
        if before != result:
            log_debug(f"Token concat: {repr(before[:50])} -> {repr(result[:50])}")
        return result
    
    def _replace_special_tokens(self, text: str) -> str:
        """Replace special macro tokens like __COUNTER__"""
        # Replace __COUNTER__ with current counter value
        text = text.replace('__COUNTER__', str(self.macro_counter))
        # Replace __UNIQUE__ with current counter value (alias)
        text = text.replace('__UNIQUE__', str(self.macro_counter))
        return text