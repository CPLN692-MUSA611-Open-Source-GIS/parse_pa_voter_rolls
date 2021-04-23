#!/usr/bin/env python

import csv
import os
from datetime import datetime

import click

def files_for_county(all_files, county):
    relevant_files = [f for f in all_files if f.startswith(county)]
    return {
        'election_map': next(f for f  in relevant_files if "Election Map" in f),
        'fve': next(f for f  in relevant_files if "FVE" in f),
        'zone_types': next(f for f  in relevant_files if "Types" in f),
        'zone_codes': next(f for f  in relevant_files if "Codes" in f),
    }

def record_from_row(row):
    entries = [entry.strip().strip('"').strip() for entry in row.split('\t')]

    return {
        "voter_id": entries[0],
        "last_name": entries[2],
        "first_name": entries[3],
        "middle_name": entries[4] or None,
        "title": entries[5] or None,
        "sex": entries[6],
        "dob": read_date(entries[7]),
        "registration_date": read_date(entries[8]),
        "status": entries[9],
        "date_last_status_change": read_date(entries[10]),
        "party": entries[11],
        "address": f"{entries[12]} {entries[13]}{entries[14]} {entries[15]} {entries[16]} {entries[17].rstrip()}, {entries[18]} {entries[19]}",
        "to_geocode": [entries[0], f"{entries[12]} {entries[13]}{entries[14]} {entries[15]} {entries[16]}".rstrip(), entries[17], entries[18], entries[19]]
    }

def read_date(date_string):
    try:
        date = datetime.strptime(date_string , '%m/%d/%Y')
    except ValueError: 
        date = None
    return date


@click.command()
@click.option('--src', '-s', help='Directory with voter rolls.', required=True)
def main(src):
    all_files = [f for f in os.listdir(src) if os.path.isfile(os.path.join(src, f))]

    counties = list(set([f.split(' ')[0] for f in all_files]))

    county_files = [files_for_county(all_files, county) for county in counties]

    fve_files = [cf['fve'] for cf in county_files]

    with open("rolls_out.csv", 'w') as out_file, open("to_geocode.csv", 'w') as out_geocode:
        record_fieldnames = ["voter_id", "last_name", "first_name", "middle_name", "title", "sex", "dob", "registration_date", "status", "date_last_status_change", "party", "address"]
        record_writer = csv.DictWriter(out_file, fieldnames=record_fieldnames)
        record_writer.writeheader()

        geocode_writer = csv.writer(out_geocode)

        for fve_file in fve_files:
            click.echo(f"Begin processing {fve_file}...")
            with open(os.path.join(src, fve_file), 'r') as fve:
                for line in fve:
                    record = record_from_row(line)
                    geocode_writer.writerow(record['to_geocode'])
                    del record['to_geocode']
                    record_writer.writerow(record)

            click.echo(f"Finish processing {fve_file}...")

if __name__ == '__main__':
    main()