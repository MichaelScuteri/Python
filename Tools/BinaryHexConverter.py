import sys

def convert_to_bin(input_string):
    return ' '.join(format(ord(char), '08b') for char in input_string)

def convert_to_hex(input_string):
    return ' '.join(format(ord(char), '02x') for char in input_string)

def decode_from_bin(input_string):
    binary_values = input_string.split()
    return ''.join(chr(int(bv, 2)) for bv in binary_values)

def decode_from_hex(input_string):
    hex_values = input_string.split()
    return ''.join(chr(int(hv, 16)) for hv in hex_values)

def main():
    if len(sys.argv) != 4:
        print("Usage: script.py [-e|-d] [-b|-h] string")
        sys.exit(1)

    input_string = sys.argv[1]
    operation = sys.argv[2]
    format_type = sys.argv[3]

    if operation == "-e":
        if format_type == "-b":
            output = convert_to_bin(input_string)
            print(output)
        elif format_type == "-h":
            output = convert_to_hex(input_string)
            print(output)
        else:
            print("Invalid format. Specify either -b for binary or -h for hex.")
            sys.exit(1)
    elif operation == "-d":
        if format_type == "-b":
            output = decode_from_bin(input_string)
            print(output)
        elif format_type == "-h":
            output = decode_from_hex(input_string)
            print(output)
        else:
            print("Invalid format. Specify either -b for binary or -h for hex.")
            sys.exit(1)
    else:
        print("Invalid operation. Specify either -e for encode or -d for decode.")
        sys.exit(1)

if __name__ == "__main__":
    main()
