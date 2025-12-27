"""
Verify Intel HEX file format and checksums
"""

def verify_intel_hex_checksum(line):
    """Verify checksum of an Intel HEX record"""
    if not line.startswith(':'):
        return False, "Missing colon"
    
    # Remove colon and convert hex pairs to bytes
    hex_str = line[1:].strip()
    if len(hex_str) % 2 != 0:
        return False, "Odd number of hex digits"
    
    bytes_data = [int(hex_str[i:i+2], 16) for i in range(0, len(hex_str), 2)]
    
    # Calculate checksum (sum of all bytes including checksum should be 0 mod 256)
    total = sum(bytes_data)
    if (total & 0xFF) == 0:
        return True, f"Checksum OK: {bytes_data[-1]:02X}"
    else:
        expected = (-sum(bytes_data[:-1])) & 0xFF
        return False, f"Checksum FAIL: got {bytes_data[-1]:02X}, expected {expected:02X}"

def decode_intel_hex_record(line):
    """Decode an Intel HEX record"""
    hex_str = line[1:].strip()
    bytes_data = [int(hex_str[i:i+2], 16) for i in range(0, len(hex_str), 2)]
    
    byte_count = bytes_data[0]
    address = (bytes_data[1] << 8) | bytes_data[2]
    record_type = bytes_data[3]
    data = bytes_data[4:4+byte_count]
    checksum = bytes_data[4+byte_count]
    
    type_names = {
        0x00: "Data",
        0x01: "EOF",
        0x02: "Extended Segment Address",
        0x03: "Start Segment Address",
        0x04: "Extended Linear Address",
        0x05: "Start Linear Address"
    }
    
    print(f"  Byte Count: {byte_count}")
    print(f"  Address: 0x{address:04X}")
    print(f"  Type: 0x{record_type:02X} ({type_names.get(record_type, 'Unknown')})")
    if data:
        print(f"  Data: {' '.join(f'{b:02X}' for b in data)}")
    print(f"  Checksum: 0x{checksum:02X}")

# Test the expected output
expected_lines = [
    ":020000040800F2",
    ":08000000123456789ABCDEF0C0",
    ":00000001FF"
]

print("Expected Intel HEX format:")
print("=" * 60)
for i, line in enumerate(expected_lines, 1):
    print(f"\nLine {i}: {line}")
    valid, msg = verify_intel_hex_checksum(line)
    print(f"  Validation: {msg}")
    if valid:
        decode_intel_hex_record(line)

# Now verify actual file
print("\n" + "=" * 60)
print("Actual file content:")
print("=" * 60)

try:
    with open(r".\output\assembly_build\test_intel_hex.hex", 'r') as f:
        lines = [line.strip() for line in f if line.strip()]
    
    for i, line in enumerate(lines, 1):
        print(f"\nLine {i}: {line}")
        valid, msg = verify_intel_hex_checksum(line)
        print(f"  Validation: {msg}")
        if valid:
            decode_intel_hex_record(line)
        
        if i <= len(expected_lines):
            if line == expected_lines[i-1]:
                print(f"  [OK] Matches expected")
            else:
                print(f"  [FAIL] MISMATCH! Expected: {expected_lines[i-1]}")
except FileNotFoundError:
    print("File not found!")
