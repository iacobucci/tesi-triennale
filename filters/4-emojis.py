#!/usr/bin/python3
import sys

def replace(text: str) -> str:
    return text.replace('✅', 'Sì').replace('❌', 'No')

# read from stdin and write to stdout
if __name__ == '__main__':
    # Leggi l'input da stdin
    input_text = sys.stdin.read()

    # Sostituisci le emoji
    output_text = replace(input_text)

    # Scrivi l'output su stdout in ASCII
    print(output_text)