#!/usr/bin/python3
import sys

# emoji = {}
# import os
# import json

# with open(os.path.dirname(__file__) + '/emoji.json') as f:
# 	j = json.load(f)
# 	for i in j:
# 		emoji[i['emoji']] = '\\' + i['aliases'][0]

def replace(text: str) -> str:
	# for i in emoji:
	# 	text = text.replace(i, emoji[i])
	# return text
	return text.replace('✅', '').replace('❌', '')

# read from stdin and write to stdout
def main():
    # Leggi l'input da stdin
    input_text = sys.stdin.read()

    # Sostituisci le emoji
    output_text = replace(input_text)

    # Scrivi l'output su stdout in ASCII
    print(output_text)

if __name__ == '__main__':
	main()