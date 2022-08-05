import sys
import collections
import pandas as pd
import numpy as np
import math


def find_max_prime_divisor(number: int):
    while number % 2 == 0:
        max_prime = 2
        number /= 1
    for i in range(3, int(math.sqrt(number)) + 1, 2):
        while number % i == 0:
            max_prime = i
            number = number / i
    if number > 2:
        max_prime = number
    return int(max_prime)


def check_headers_are_same(file1: pd.DataFrame, file2: pd.DataFrame):
    file1_col_names = list(file1)
    file2_col_names = list(file2)

    if collections.Counter(file1_col_names) != collections.Counter(file2_col_names):
        not_matching = list(set(file1_col_names) ^ set(file2_col_names))

        for i in range(len(not_matching)):
            if not_matching[i] in file1:
                print(f"Dropping {not_matching[i]} from file1.")
                file1.drop(columns=not_matching[i], inplace=True)
            else:
                print(f"Dropping {not_matching[i]} from file2.")
                file2.drop(columns=not_matching[i], inplace=True)


def write_chunk_differences_to_df(file1_df_chunks: pd.DataFrame, file2_df_chunks: pd.DataFrame):
    if len(file1_df_chunks) != len(file2_df_chunks):
        print("Dataframe chunks are of different lengths. Something has gone wrong.")
        return

    comparison_truth_table_chunks = []

    for i in range(len(file1_df_chunks)):
        comparison_truth_table_chunks.append(
            file1_df_chunks[i] == file2_df_chunks[i])

    file1_differences = pd.DataFrame()
    file2_differences = pd.DataFrame()
    difference_indexes = []

    for i in range(len(comparison_truth_table_chunks)):
        for index, row in comparison_truth_table_chunks[i].iterrows():
            for f_index, f_row in file1_df_chunks[i].iterrows():
                # TODO
                print()


def compare_csvs(file1_filepath: str, file2_filepath: str):
    file1_df = pd.read_csv(file1_filepath, encoding='cp1252')
    file2_df = pd.read_csv(file2_filepath, encoding='cp1252')

    # Filling empty cells with - because empty cells will always return false when doing the comparison
    file1_df.fillna('-', inplace=True)
    file2_df.fillna('-', inplace=True)

    print("Checking file headers for differences and attemping to make them similar for comparison.")
    file1_df, file2_df = check_headers_are_same(file1_df, file2_df)

    print("Chunking up dataframes.")
    file1_df_chunks = np.split(file1_df, find_max_prime_divisor(len(file1_df)))
    file2_df_chunks = np.split(file2_df, find_max_prime_divisor(len(file2_df)))


def main():
    compare_csvs(sys.argv[1], sys.argv[2])


if __name__ == '__main__':
    main()
