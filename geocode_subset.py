#!/usr/bin/env python

import csv
import multiprocessing as mp

import censusgeocode as cg
from retrying import retry


def main():
    geocode_batches = map(
        lambda x: "geocode_batches/batch-aa" + x,
        ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l"]
    )

    pool = mp.Pool(mp.cpu_count())
    results = pool.map(process_batch, geocode_batches)
    pool.close()
    pool.join()
    with open("geocode_lookup.csv", 'w') as output_csv:
        fieldnames = ['voter_id', 'address', 'lat', 'lon', 'countyfp', 'tract', 'block', 'tigerlineid']
        writer = csv.DictWriter(output_csv, fieldnames=fieldnames)
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
