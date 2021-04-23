#!/usr/bin/env python

import csv
import multiprocessing as mp
import os

import censusgeocode as cg
from retrying import retry


def main():
    geocode_batches = [os.path.join("geocode_batches", f) for f in os.listdir("geocode_batches") if os.path.isfile(os.path.join("geocode_batches", f)) and f.startswith("batch")]

    pool = mp.Pool(mp.cpu_count())
    results = pool.map(process_batch, geocode_batches)
    pool.close()
    pool.join()
    with open("geocode_lookup.csv", 'w') as output_csv:
        fieldnames = ['voter_id', 'address', 'lat', 'lon', 'countyfp', 'tract', 'block', 'tigerlineid']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        for result in results:
            writer.writerows(result)


@retry(wait_exponential_multiplier=1000, wait_exponential_max=10000)
def process_batch(batch_path):
    print(f"Begin processing {batch_path}...")
    geocoded_results = cg.addressbatch(batch_path, timeout=1000)
    print(f"Finish processing {batch_path}...")
    return geocoded_results


if __name__ == "__main__":
    main()
