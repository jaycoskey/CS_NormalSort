#!/usr/bin/env python

import argparse
from functools import reduce
from numpy.random import multinomial
import operator
import pickle
import sys
import time

from normalsort import normalsort


def benchmark(max_power=5):
    def ord_count_to_total(ordinals):
        start_idx = 1
        total = sum([(k + start_idx) * int(x) for k, x in enumerate(ordinals)])
        return total

    sizess = [[k * 10**p for k in range(1, 10)] for p in range(2, max_power + 1)]
    sizes = reduce(operator.add, sizess, [])
    times = {}
    for size in sizes:
        # Add up $size rolls of 1000d1000
        raw = multinomial(1000, [1/1000] * 1000, size)
        totals = list(map(ord_count_to_total, raw))

        t_begin = time.time()
        normalsorted = normalsort(totals) 
        t_end = time.time()
        t_diff = t_end - t_begin

        assert(sorted(normalsorted) == normalsorted)
        print(f'size={size}: t_diff={t_diff}')
        times[size] = t_diff
    return times


def print_times(times):
    for count, t in times.items():
        print(f'{count}:\t{t}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='normalsort', add_help=True)
    parser.add_argument('-i', '--ifile', help='File to load benchmark data from')
    parser.add_argument('-o', '--ofile', help='File to store benchmark data to')
    parser.add_argument('--magnitude', help='The largest number of zeros in the sizes of the sets sorted')
    args = parser.parse_args()
    if args.ifile and args.ofile:
        print('ERROR: Either -i/--ifile or -o/--ofile can be specified, but not both.')

    if args.ifile:
        with open(args.ifile, 'rb') as f:
            times = pickle.load(f)
            print_times(times)
        sys.exit(0)

    if args.magnitude:
        times = benchmark(int(args.magnitude))
    else:
        times = benchmark()

    print_times(times)

    if args.ofile:
        with open(args.ofile, 'wb') as f:
            times = pickle.dump(times, f)
 
