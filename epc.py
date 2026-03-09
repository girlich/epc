#!/usr/bin/python3

import json
import sys

def parse_epc_string(epc_data):
    # split lines
    lines = epc_data.strip().splitlines()
    
    # Mapping character set
    encoding_map = {
        "1": "UTF-8",
        "2": "ISO-8859-1 (Latin-1)",
        "3": "ISO-8859-2",
        "4": "ISO-8859-4",
        "5": "ISO-8859-5",
        "6": "ISO-8859-7",
        "7": "ISO-8859-10",
        "8": "ISO-8859-15"
    }

    # helper function to get an emtpy string in case the value is missing
    get_line = lambda i: lines[i] if i < len(lines) else ""

    raw_encoding = get_line(2)
    
    # Create structure
    parsed_data = {
        "technical_header": {
            "service_tag": get_line(0),      # expected: BCD
            "version": get_line(1),          # expected: 001 oder 002
            "identification": get_line(3),   # expected: SCT
            "encoding": {
                "raw": raw_encoding,
                "parsed": encoding_map.get(raw_encoding, "Unknown")
            }
        },
        "payment_details": {
            "bic": get_line(4),
            "recipient_name": get_line(5),
            "iban": get_line(6),
            "amount": get_line(7).replace("EUR", ""),
            "purpose_code": get_line(8),
            "remittance_reference": get_line(9), # Strukturiert (RF)
            "remittance_text": get_line(10),     # Unstrukturiert
            "information": get_line(11)          # Zusatzinfos
        }
    }

    return parsed_data

def main():
    raw = sys.stdin.read().strip()
    parsed_data = parse_epc_string(raw)
    print(json.dumps(parsed_data, indent=4, ensure_ascii=False))

if __name__ == "__main__":
    main()
