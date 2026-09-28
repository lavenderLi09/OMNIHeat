#!/usr/bin/env python3
"""Generic heating-budget checks and metrics for pre-aligned observation pairs."""

import argparse
import csv
import json
import math
from pathlib import Path
import statistics


def validate_budget(data):
    """Check nonnegative component powers and optional exhaustive radial partitions."""
    global_power = data['global_power_erg_s']
    components = set(global_power) - {'Htotal'}
    if not components or 'Htotal' not in global_power:
        raise ValueError('provide components and Htotal')
    bands = data.get('radial_band_power_erg_s', {})
    for record in [global_power, *bands.values()]:
        if set(record) != components | {'Htotal'}:
            raise ValueError('all records must have the same component names')
        if any(type(v) not in (int, float) or not math.isfinite(v) or v < 0
               for v in record.values()):
            raise ValueError('heating powers must be finite nonnegative numbers')
        if not math.isclose(record['Htotal'], math.fsum(record[k] for k in components),
                            rel_tol=1e-9, abs_tol=0.):
            raise ValueError('Htotal differs from the sum of its components')
    if bands:
        for key, value in global_power.items():
            if not math.isclose(value, math.fsum(b[key] for b in bands.values()),
                                rel_tol=1e-9, abs_tol=0.):
                raise ValueError('radial partitions do not reproduce the global powers')
    return {'valid': True, 'total_power_erg_s': global_power['Htotal'],
            'bands_checked': len(bands)}


def compare_pairs(pairs):
    """Equal-weight metrics; model minus observation. No alignment or fill filtering."""
    pairs = list(pairs)
    if not pairs or any(not math.isfinite(v) for pair in pairs for v in pair):
        raise ValueError('provide at least one finite model/observation pair')
    errors = [model - observed for model, observed in pairs]
    result = {'count': len(errors), 'bias': statistics.fmean(errors),
              'mae': statistics.fmean(abs(e) for e in errors),
              'rmse': math.hypot(*errors) / math.sqrt(len(errors))}
    if any(not math.isfinite(v) for v in result.values()):
        raise ValueError('metric overflow; rescale the input units')
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['budget', 'compare'])
    parser.add_argument('input', type=Path)
    args = parser.parse_args()
    try:
        with args.input.open(encoding='utf-8', newline='') as stream:
            if args.command == 'budget':
                result = validate_budget(json.load(stream))
            else:
                rows = csv.DictReader(stream)
                result = compare_pairs((float(r['model']), float(r['observed'])) for r in rows)
    except (OSError, ValueError, KeyError, TypeError, AttributeError, OverflowError) as error:
        parser.exit(2, f'Invalid input: {error}\n')
    print(json.dumps(result, indent=2, allow_nan=False))


if __name__ == '__main__':
    main()
