# Parsing PA Voter Rolls

### Downloading voter rolls
Fill out the form [here](https://www.pavoterservices.pa.gov/pages/purchasepafullvoterexport.aspx) to purchase voter rolls.
As for 2021, they cost $20 and you can get data from every county in PA.


### Parse rolls and write simplified CSV
Note that not all fields are parsed by this script.
As of now, the output fields are "voter_id", "last_name", "first_name", "middle_name", "title", "sex", "dob", "registration_date", "status", "date_last_status_change", "party", and "address".

Point the `parse_rolls.py` script at the directory of the unzipped voter rolls downloaded in the step above.
A first pass at the data is written to `rolls_out.csv` and file which can optionally be used to get associate records with their geocoded locations is written to `to_geocode.csv`.
```bash
python parse_rolls.py --src voter_rolls
```


### Geocode to_geocode.csv (optional)
To use the census tract batch geocoder, we need to create batches of at most 10,000 records.
The unix command (sorry Windows users...) `split` can be used here:
```bash
split --verbose -a 3 -l 10000 to_geocode.csv geocode_batches/
```

> -a tells it how many digits of suffix to use for addressing batches
> -l tells it how many lines per file


### Parallel geocoding
The batch size limit on the census geocoder is 10,000.
We will skirt this restriction by submitting, in parallel, each of the files produced in the step above as separate batches.
The data we get back can then be stored in a csv/lookup table and used to associate voter records with their registered locations (very roughly - the geocoder is far from perfect).


