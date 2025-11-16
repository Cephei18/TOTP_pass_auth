import sys
import re
from functools import reduce

def safe_parse_int(s):
    try:
        return int(s)
    except ValueError:
        return None

def process_one_test(lines, idx):
    return (None, idx) if idx >= len(lines) else (lambda x, i: (-1, i) if i >= len(lines) else (lambda tokens, ni: (lambda parsed: (-1, ni) if None in parsed or len(parsed) != x else (reduce(lambda acc, n: acc + n**4, list(filter(lambda n: n <= 0, parsed)), 0), ni))(list(map(safe_parse_int, tokens))))(list(filter(lambda t: t, re.split(r'\s+', lines[i].strip()))), i + 1))(int(lines[idx]), idx + 1)

def process_all_tests(lines, remaining_tests, current_idx, accumulated_results):
    return accumulated_results if remaining_tests == 0 else (lambda result, next_idx: process_all_tests(lines, remaining_tests - 1, next_idx, accumulated_results + [result]))(*process_one_test(lines, current_idx))

def main():
    (lambda lines: list(map(print, process_all_tests(lines, int(lines[0]), 1, []))))(list(filter(lambda line: line, map(str.strip, sys.stdin.readlines()))))

if __name__ == "__main__":
    main()