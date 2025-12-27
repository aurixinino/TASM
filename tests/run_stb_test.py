#!/usr/bin/env python3
"""Run ST.B regression test with full error output."""

import sys
import os
import traceback

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from tests.test_stb_regression import main
    main()
except Exception as e:
    print(f"\n{'='*80}")
    print("FATAL ERROR IN TEST")
    print('='*80)
    print(f"Error: {e}")
    print("\nFull traceback:")
    traceback.print_exc()
    sys.exit(1)
