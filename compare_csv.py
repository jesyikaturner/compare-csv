import sys
import collections
import pandas as pd
import numpy as np

from utilities import write_to_file, find_max_prime_divisor


def check_headers_are_same(file1: pd.DataFrame, file2: pd.DataFrame, output_filepath: str):
    file1_col_names = list(file1)
    file2_col_names = list(file2)

    if collections.Counter(file1_col_names) != collections.Counter(file2_col_names):
        not_matching = list(set(file1_col_names) ^ set(file2_col_names))

        for i in range(len(not_matching)):
            if not_matching[i] in file1:
                write_to_file(
                    f"Dropping {not_matching[i]} from file1.", output_filepath)
                file1.drop(columns=not_matching[i], inplace=True)
            else:
                write_to_file(
                    f"Dropping {not_matching[i]} from file2.", output_filepath)
                file2.drop(columns=not_matching[i], inplace=True)

    return file1, file2


def write_chunk_differences_to_df(file1_df_chunks: pd.DataFrame, file2_df_chunks: pd.DataFrame):
    if len(file1_df_chunks) != len(file2_df_chunks):
        print(
            "Dataframe chunks are of different lengths. Something has gone wrong.")
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
            for f1_index, f1_row in file1_df_chunks[i].iterrows():
                if index == f1_index and row.all() == False:
                    difference_indexes.append(f1_index)
                    file1_differences = file1_differences.append(f1_row)
            for f2_index, f2_row in file2_df_chunks[i].iterrows():
                if index == f2_index and row.all() == False:
                    difference_indexes.append(f2_index)
                    file2_differences = file2_differences.append(f2_row)

    return file1_differences, file2_differences


def compare_csvs(file1_filepath: str, file2_filepath: str, output_filepath: str):
    file1_df = pd.read_csv(file1_filepath, encoding='cp1252')
    file2_df = pd.read_csv(file2_filepath, encoding='cp1252')

    # Filling empty cells with - because empty cells will always return false when doing the comparison
    file1_df.fillna('-', inplace=True)
    file2_df.fillna('-', inplace=True)

    write_to_file(
        "Checking file headers for differences and attemping to make them similar for comparison.", output_filepath)
    file1_df, file2_df = check_headers_are_same(
        file1_df, file2_df, output_filepath)

    write_to_file("Chunking up dataframes.", output_filepath)
    file1_df_chunks = np.split(file1_df, find_max_prime_divisor(len(file1_df)))
    file2_df_chunks = np.split(file2_df, find_max_prime_divisor(len(file2_df)))

    write_to_file("Getting differences in chunks", output_filepath)
    file1_differences, file2_differences = write_chunk_differences_to_df(
        file1_df_chunks, file2_df_chunks)

    difference_truth_table = file1_differences == file2_differences
    col_differences = []

    for i in range(len(file1_differences)):
        write_to_file(f"{file1_filepath}:", output_filepath)
        write_to_file(file1_differences.iloc[[i]], output_filepath)

        write_to_file(f"{file2_filepath}:", output_filepath)
        write_to_file(file2_differences.iloc[[i]], output_filepath)

        write_to_file("Columns that have differences:", output_filepath)

        line = difference_truth_table.iloc[[i]].values.tolist()
        print(line)

        for col in range(len(difference_truth_table.columns)):
            if line[0][col] == False:
                col_differences.append(difference_truth_table.columns[col])

        write_to_file(list(dict.fromkeys(col_differences)), output_filepath)
        write_to_file("", output_filepath)


def main():
    compare_csvs(sys.argv[1], sys.argv[2], sys.argv[3])


if __name__ == '__main__':
    main()
