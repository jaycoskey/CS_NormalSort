#!/usr/bin/env python

from collections import defaultdict
from math import ceil, floor, sqrt
from numpy.random import multinomial
import scipy.stats 


def normalsort(nums, bin_count=None, default_exp=None, default_stdev=None, verbose=False):
    """Phase 1: Approximate sort, assuming normal dist; Phase 2: Complete w/ insertion sort."""

    if verbose:
        print(f'normalsort input:\n\t{nums}')
    """Phase 1: Roughly sort the data into bins, assuming the data is normally distributed"""
    DEFAULT_EXP = 0.5
    DEFAULT_STDEV = 0.1
    EPSILON = 10e-6
    bins = defaultdict(list)
    if bin_count is None:
        default_exp = default_exp if default_exp else DEFAULT_EXP
        bin_count = ceil(len(nums) ** default_exp)
    total = 0
    total2 = 0
    for k, n in enumerate(nums):
        
        total += n
        total2 += n**2
        mean = total / (k + 1)

        # print(f'k:{type(k)}')
        # print(f'num:{type(n)}')
        # print(f'total:{type(total)}')

        stdev = sqrt(total2 / (k + 1) - mean**2)
        if abs(stdev) < EPSILON:
            stdev = default_stdev if default_stdev else DEFAULT_STDEV

        cum_density = scipy.stats.norm.cdf(n, loc=mean, scale=stdev)
        bin_num = floor(bin_count * cum_density)
        bins[bin_num].append(n)

    if verbose:
        print(f'normalsort bins:')
        for bin_key in sorted(bins.keys()):
            print(f'\tbin #{bin_key}: {bins[bin_key]}')
 
    """Phase 2: Concatenate the contents of the different bins"""
    result = [num for bin_num in range(bin_count) for num in bins[bin_num]]

    """Phase 3: Insertion sort FTW, which performs well on nearly-sorted data"""
    for count in range(len(result)):
        idx = count
        num = result[idx]
        # Put this in the leftmost position where it's larger than those it follows.
        while idx > 0 and num < result[idx - 1]:
            result[idx] = result[idx - 1]
            idx -= 1
        result[idx] = num

    return result

 
def main():
    # 20d6, sampled 30 times
    dice_roll_info = multinomial(20, [1/6] * 6, 30)
    rolls = [sum([(k+1) * row[k] for k in range(len(row))]) for row in dice_roll_info]
    normalsorted = normalsort(rolls, bin_count=10, verbose=True)
    print(f'normalsort output:\n\t{normalsorted}')


if __name__ == '__main__':
    main()

