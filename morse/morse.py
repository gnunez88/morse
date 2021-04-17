#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Author: gnunez88
#
# Distributed under terms of the MIT license.

"""
Morse code translator
"""

import argparse as ap
import json
import os
import pdb
import re

class MorseCode:
    """
    Dumb class which only contains morse code read from a JSON file.
    """
    def __init__(self,
                 filename: str) -> None:
        with open(filename, 'r') as f:
            self._morse = json.load(f)

    def _reverse(self) -> None:
        self._revmorse = dict(zip(self._morse.values(), self._morse.keys()))

    def get(self,
            char: str) -> str:
        return self._morse[char.lower()]

    def getrev(self,
               code: str) -> str:
        # Check if self._revmorse exists
        try:
            char = self._revmorse[code]
        except AttributeError:
            self._reverse()
            char = self._revmorse[code]
        except KeyError:
            err_msg = f'The sequence "{code}" is not mapped'
            raise MorseCodeException(err_msg)

        return char

    def keys(self) -> list:
        return self._morse.keys()

    def values(self) -> list:
        return self._morse.values()

class MorseCodeException(Exception):
    """
    """

class Morse:
    """
    """
    def __init__(self,
                 dictionary: dict,
                 strict: False,
                 char_separator: ' ',
                 word_separator: '/',
                 line_separator: '\n'):
        self._dict = dictionary
        self._strict = strict
        self._char_separator = char_separator
        self._word_separator = word_separator
        self._line_separator = line_separator

    def get(self) -> str:
        return self._text

    def to_morse(self,
                 lines: list) -> str:
        """
        Convert text into Morse code
        """
        output = ''
        for l in range(len(lines)):
            if re.match('^\s*$', lines[l]):
                output += self._line_separator
            else:
                output += self._to_morse(lines[l].strip().lower(), self._strict)
                output += self._line_separator if l < len(lines) else ''

        return output.strip()

    def _to_morse(self,
                  text: str,
                  strict: False) -> str:
        """
        Convert one single line into Morse code
        """
        code = ''
        for char in text:
            if char == ' ':
                code += self._word_separator
                code += self._char_separator  # It's clearer
            elif char in self._dict.keys():
                code += self._dict.get(char)
                code += self._char_separator
            else:
                if not strict:
                    code += char  # A non-letter and non-digit character

        return code

    def to_text(self,
                lines: list) -> str:
        """
        Convert text from Morse code
        """
        output = ''
        for l in range(len(lines)):
            if re.match('^\s*$', lines[l]):
                output += '\n'
            else:
                output += self._to_text(lines[l].strip().lower(), self._strict)
                output += '\n' if l < len(lines) else ''

        return output.strip()

    def _to_text(self,
                 morse_code: str,
                 strict: False) -> str:
        """
        Convert one single line from Morse code
        """
        text = ''
        for code in morse_code.split(self._char_separator):
            is_format_right = re.match('^[.-]{1,5}$', code)
            if not is_format_right:
                symbol_and_separator = f'.{self._word_separator}'
                if code == self._word_separator:
                    text += ' '
                elif re.match(symbol_and_separator, code):
                    text += code[0]  # Get rid of the separator
                    text += ' '
                else:
                    if strict:
                        err_msg = f'"{code}" is not a valid morse code.'
                        raise MorseException(err_msg)
                    else:
                        text += code  # Which should be a symbol
            elif code == '':
                text += self._char_separator
            else:
                text += self._dict.getrev(code)

        return text

class MorseException(Exception):
    """
    """
    pass

# Functions
def main(args):

    if args.debug:
        pdb.set_trace()

    output = ''  # The result

    MORSE_SCRIPT = os.path.realpath(__file__)
    MORSE_CODE_FILE = os.path.dirname(MORSE_SCRIPT) + os.sep + 'morse.json'
    morse_code = MorseCode(MORSE_CODE_FILE)

    if args.file:
        with open(args.input, 'r') as f:
            lines = f.read().split(args.line_separator)
            if lines[-1] == '':  # Removing last entry if empty
                lines.pop()
    else:
        lines = args.input.split(args.line_separator)

    morse = Morse(morse_code,
                  args.strict,
                  args.char_separator,
                  args.word_separator,
                  args.line_separator)  # TODO: Merge with MorseCode

    if args.to_morse:
        output = morse.to_morse(lines)
    else:
        output = morse.to_text(lines)

    if args.upper_case:
        output = output.upper()

    if args.newline:
        output += '\n'

    if args.output:
        with open(args.output, 'w') as f:
            f.write(output)
    else:
        print(output, end='')

# Execution
if __name__ == '__main__':

    # Parsing arguments
    parser = ap.ArgumentParser()
    parser.add_argument(
        '-d', '--debug',
        help="Activate the debugging mode.",
        action='store_true',
        required=False,
        default=False)
    parser.add_argument(
        'input',
        help="Input text",
        type=str)
    parser.add_argument(
        '-m', '--to-morse',
        help="Convert to morse.",
        action='store_true',
        required=False,
        default=False)
    parser.add_argument(
        '-f', '--file',
        help="Input from file.",
        action='store_true',
        required=False,
        default=False)
    # Separators
    CHAR_SEPARATOR = ' '
    WORD_SEPARATOR = '/'
    LINE_SEPARATOR = '\n'
    parser.add_argument(
        '-c', '--char-separator',
        help=f"Character separator in the Morse code (default: {CHAR_SEPARATOR}).",
        type=str,
        required=False,
        default=CHAR_SEPARATOR)
    parser.add_argument(
        '-w', '--word-separator',
        help=f"Word separator in the Morse code (default: {WORD_SEPARATOR}).",
        type=str,
        required=False,
        default='/')
    parser.add_argument(
        '-l', '--line-separator',
        help=f"Line separator in the Morse code (default: {LINE_SEPARATOR}).",
        type=str,
        required=False,
        default='\n')
    parser.add_argument(
        '-s', '--strict',
        help="If set, it omits other symbols than letters and numbers.",
        action='store_true',
        required=False,
        default=False)
    parser.add_argument(
        '-u', '--upper-case',
        help="Output in uppercase (default is lowercase).",
        action='store_true',
        required=False,
        default=False)
    parser.add_argument(
        '-n', '--newline',
        help="Insert a line feed at the end.",
        action='store_true',
        required=False,
        default=False)
    parser.add_argument(
        '-o', '--output',
        help="File where to save the output (default STDOUT).",
        type=str,
        required=False)
    args = parser.parse_args()

    main(args)
