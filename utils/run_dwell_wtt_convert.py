#!/usr/bin/python3

import pyperclip

def multiline_input():
    print("Enter/Paste your content. Ctrl-D or Ctrl-Z ( windows ) to save it.")
    contents = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        contents.append(line)
    print("====================")
    return contents

if __name__ == "__main__":
    while True:
        pyperclip.copy('\n'.join('\t'.join([word.strip() for word in line.strip().split('-')]) for line in multiline_input() if line.strip()))
        pyperclip.copy('\n'.join(line.strip() for line in multiline_input() if line.isnumeric()))
