#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
# Copyright © 2021 gnunez <gnunez@ubuntu.gnunez88>
# Distributed under terms of the MIT license.

"""
My own way of testing with "argparsed" python scripts
"""

import argparse
import pdb
import subprocess
import sys
from colorama import Fore, Style

# Run script
def run(command: str,
        verbose: False) -> object:

    result = subprocess.run(command,
                            shell=True,
                            capture_output=True,
                            text=True)
    return result

def results(passed: int,
            failed: int):
    message  = f'Results:\t{Fore.GREEN}{passed}{Style.RESET_ALL}'
    message += f' - {Fore.RED}{failed}{Style.RESET_ALL}'
    message += f'\t{Fore.BLUE}{passed/(passed+failed):3.2%}{Style.RESET_ALL}'
    print(message)

def show_info(func_name: str,
              command: str,
              result: str,
              expected: str,
              error=False) -> str:
    #colour = f'{Fore.RED if error else Style.RESET_ALL}'
    colour = f'{Fore.RED if error else Fore.GREEN}'
    execute = f'{colour}COMMAND: {command} {result.args}'
    stdout = f'{colour}STDOUT: \'{result.stdout}\''
    expected = f'{colour}EXPECT: \'{expected}\''
    stderr = f'{colour}STDERR: {result.stderr}'
    exitcode = f'{colour}EXIT CODE: {result.returncode}'
    print()
    print(execute)
    print(stdout)
    print(expected)
    print(stderr)
    print(exitcode)

def show_error(func_name: str,
               command: str,
               result: str,
               expected: str,
               error=False) -> str:
    show_info(func_name, command, result, expected, True)

class TestResultException(Exception):
    def __init__(self,
                 funcname: str,
                 result: str,
                 expected: str):
        sys.stderr.write(f'{funcname}: ')
        sys.stderr.write(f'{result} != {expected}\n')

# Tests
## Text to Morse
### 1 lowercase ASCII letter
def test_t2m_1lAletter(command, verbose=False):
    func_name = 'test_t2m_1lAletter'
    exit_status = True
    args = '-m a'
    execute = f'{command} {args}'
    expected = '.-'
    result = run(execute, verbose)
    if verbose:
        show_info(func_name, command, result, expected)
    if result.stdout != expected:
        show_error(func_name, command, result, expected)
        exit_status = False
    return exit_status

### 1 uppercase ASCII letter
def test_t2m_1uAletter(command, verbose=False):
    func_name = 'test_t2m_1uAletter'
    exit_status = True
    args = '-m A'
    execute = f'{command} {args}'
    expected = '.-'
    result = run(execute, verbose)
    if verbose:
        show_info(func_name, command, result, expected)
    if result.stdout != expected:
        show_error(func_name, command, result, expected)
        exit_status = False
    return exit_status

### 1 digit
def test_t2m_1digit(command, verbose=False):
    func_name = 'test_t2m_1digit'
    exit_status = True
    args = '-m 1'
    execute = f'{command} {args}'
    expected = '.----'
    result = run(execute, verbose)
    if verbose:
        show_info(func_name, command, result, expected)
    if result.stdout != expected:
        show_error(func_name, command, result, expected)
        exit_status = False
    return exit_status

### 1 lowercase ASCII word
def test_t2m_1lAword(command, verbose=False):
    func_name = 'test_t2m_1lAword'
    exit_status = True
    args = '-m hello'
    execute = f'{command} {args}'
    expected = '.... . .-.. .-.. ---'
    result = run(execute, verbose)
    if verbose:
        show_info(func_name, command, result, expected)
    if result.stdout != expected:
        show_error(func_name, command, result, expected)
        exit_status = False
    return exit_status

### 1 digit word
def test_t2m_1dword(command, verbose=False):
    func_name = 'test_t2m_1dword'
    exit_status = True
    args = '-m 1234567890'
    execute = f'{command} {args}'
    expected = '.---- ..--- ...-- ....- ..... -.... --... ---.. ----. -----'
    result = run(execute, verbose)
    if verbose:
        show_info(func_name, command, result, expected)
    if result.stdout != expected:
        show_error(func_name, command, result, expected)
        exit_status = False
    return exit_status

### 1 uppercase ASCII word
def test_t2m_1uAword(command, verbose=False):
    func_name = 'test_t2m_1uAword'
    exit_status = True
    args = '-m HELLO'
    execute = f'{command} {args}'
    expected = '.... . .-.. .-.. ---'
    result = run(execute, verbose)
    if verbose:
        show_info(func_name, command, result, expected)
    if result.stdout != expected:
        show_error(func_name, command, result, expected)
        exit_status = False
    return exit_status

### 1 lowercase ASCII line
def test_t2m_1lAline(command, verbose=False):
    func_name = 'test_t2m_1lAline'
    exit_status = True
    args = '-m "hello world"'
    execute = f'{command} {args}'
    expected = '.... . .-.. .-.. --- / .-- --- .-. .-.. -..'
    result = run(execute, verbose)
    if verbose:
        show_info(func_name, command, result, expected)
    if result.stdout != expected:
        show_error(func_name, command, result, expected)
        exit_status = False
    return exit_status

### 1 uppercase ASCII line
def test_t2m_1uAline(command, verbose=False):
    func_name = 'test_t2m_1uAline'
    exit_status = True
    args = '-m "HELLO WORLD"'
    execute = f'{command} {args}'
    expected = '.... . .-.. .-.. --- / .-- --- .-. .-.. -..'
    result = run(execute, verbose)
    if verbose:
        show_info(func_name, command, result, expected)
    if result.stdout != expected:
        show_error(func_name, command, result, expected)
        exit_status = False
    return exit_status

### 1 capitalised ASCII line
def test_t2m_1cAline(command, verbose=False):
    func_name = 'test_t2m_1cAline'
    exit_status = True
    args = '-m "Hello World"'
    execute = f'{command} {args}'
    expected = '.... . .-.. .-.. --- / .-- --- .-. .-.. -..'
    result = run(execute, verbose)
    if verbose:
        show_info(func_name, command, result, expected)
    if result.stdout != expected:
        show_error(func_name, command, result, expected)
        exit_status = False
    return exit_status

# Main
def main(args):
    command = '../morse/morse.py'
    counter_ok = 0  # Amount of test passed
    counter_ko = 0  # Amount of test failed
    # Basic test text to morse (t2m)
    if test_t2m_1lAletter(command, args.verbose):
        counter_ok += 1
    else:
        counter_ko += 1
    if test_t2m_1uAletter(command, args.verbose):
        counter_ok += 1
    else:
        counter_ko += 1
    if test_t2m_1digit(command, args.verbose):
        counter_ok += 1
    else:
        counter_ko += 1
    if test_t2m_1dword(command, args.verbose):
        counter_ok += 1
    else:
        counter_ko += 1
    if test_t2m_1lAword(command, args.verbose):
        counter_ok += 1
    else:
        counter_ko += 1
    if test_t2m_1uAword(command, args.verbose):
        counter_ok += 1
    else:
        counter_ko += 1
    if test_t2m_1lAline(command, args.verbose):
        counter_ok += 1
    else:
        counter_ko += 1
    if test_t2m_1uAline(command, args.verbose):
        counter_ok += 1
    else:
        counter_ko += 1
    if test_t2m_1cAline(command, args.verbose):
        counter_ok += 1
    else:
        counter_ko += 1
    #test_t2m_2uAline(command, args.verbose)

    results(counter_ok, counter_ko)

# Standalone checker
if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-v', '--verbose',
        help="Print more information (verbose mode).",
        action='store_true',
        required=False,
        default=False)
    parser.add_argument(
        '-d', '--debug',
        help="Activate debugging mode",
        action='store_true',
        required=False,
        default=False)
    args = parser.parse_args()

    main(args)
