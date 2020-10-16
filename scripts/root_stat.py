#!/usr/bin/env python3

from root_pandas import read_root
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Show signal fraction of a root file')
    parser.add_argument('filename', type=str)
    args = parser.parse_args()

    df = read_root(args.filename, 'lambda')

    print('Number of candidates:', len(df))
    print('Matched:', len(df.query('isSignal == 1')))
    print('Unmatched:', len(df.query('isSignal == 0')))
    print('Fraction of matched candidates:', df.isSignal.mean())