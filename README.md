# Compare CSVs

A small python program that compares two CSVs and finds the differences between them. The differences are output into an excel spreadsheet, listing the affected index, column and the data from each CSV.

## Pre-requisites 

- Python 3.8.10
- OpenPyxl
- Pandas
- Numpy

## Setup

1. Install python3

2. Install OpenPyxl:
```bash
    python3 -m pip install openpyxl
```

## Run

- Run Program:

```bash
    python3 compare_csv.py ./data/actual.csv ./data/expected.csv
```

- Run Tests:

```bash
    python3 test_compare_csv.py
```

