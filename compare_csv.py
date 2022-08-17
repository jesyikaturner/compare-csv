import collections
import sys

import numpy as np
import pandas as pd

from utilities import find_max_prime_divisor, write_to_file

# These options make sure the full dataframe is printed instead of shortened version.
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', None)


def make_headers_same(file1: pd.DataFrame, file2: pd.DataFrame):
    """
    Takes two file dataframes - file1 and file2 and checks if the headers
    are the same, otherwise remove and note down removed the columns. This will
    make the two dataframes ready for comparison.

    Parameters: 
        file1: pd.DataFrame -- dataframe of file1 to compare headers
        file2: pd.DataFrame -- dataframe of file2 to compare headers

    Returns:
        file1: pd.DataFrame -- modified file1 dataframe with removed headers
        fil2: pd.Dataframe -- modified file2 dataframe with removed headers
    """
    file1_col_names = list(file1)
    file2_col_names = list(file2)

    if collections.Counter(file1_col_names) != collections.Counter(file2_col_names):
        not_matching = list(set(file1_col_names) ^ set(file2_col_names))

        for i in range(len(not_matching)):
            if not_matching[i] in file1:
                write_to_file(
                    f"Dropping {not_matching[i]} from file1.")
                file1.drop(columns=not_matching[i], inplace=True)
            else:
                write_to_file(
                    f"Dropping {not_matching[i]} from file2.")
                file2.drop(columns=not_matching[i], inplace=True)

    return file1, file2


def write_chunk_differences_to_df(file1_df_chunks: list, file2_df_chunks: list):
    """
    Run through each of the df chunks from file1 and file2 and compare the differences
    between them then return a DataFrame 

    Parameters:
        file1_df_chunks: pd.DataFrame -- chunks of file1 dataframe to compare
        file2_df_chunks: pd.DataFrame -- chunks of file2 dataframe to compare

    Returns:
        file1_differences: pd.DataFrame -- 
        file2_differences: pd.DataFrame --
    """
    if len(file1_df_chunks) != len(file2_df_chunks):
        write_to_file(
            "Dataframe chunks are of different lengths. Something has gone wrong.")
        return

    comparison_truth_table_chunks = []

    for i in range(len(file1_df_chunks)):
        comparison_truth_table_chunks.append(
            file1_df_chunks[i] == file2_df_chunks[i])

    file1_differences = pd.DataFrame()
    file2_differences = pd.DataFrame()

    for i in range(len(comparison_truth_table_chunks)):
        for index, row in comparison_truth_table_chunks[i].iterrows():
            for f1_index, f1_row in file1_df_chunks[i].iterrows():
                if index == f1_index and row.all() == False:
                    file1_differences = file1_differences.append(f1_row)
            for f2_index, f2_row in file2_df_chunks[i].iterrows():
                if index == f2_index and row.all() == False:
                    file2_differences = file2_differences.append(f2_row)
        # Printing this to terminal to show that the program is doing something and
        # not just hanging. It doesn't really matter with small CSVs but big ones
        # can take ages.
        print(f"\nNumber of rows that are different: {len(file1_differences)}")

    return file1_differences, file2_differences


def compare_csvs(file1_filepath: str, file2_filepath: str):
    """
    TODO: write description
    Parameters:
        file1_filepath: str --
        file2_filepath: str --

    Return:
        output_df: pd.DataFrame -- 
    """
    file1_df = pd.read_csv(file1_filepath, encoding='cp1252')
    file2_df = pd.read_csv(file2_filepath, encoding='cp1252')

    # Filling empty cells with - because empty cells will always return false when doing the comparison
    file1_df.fillna('-', inplace=True)
    file2_df.fillna('-', inplace=True)

    # TODO: Add index column to both dataframes if none exists

    write_to_file(
        "Checking file headers for differences and attempting to make them similar for comparison.")
    file1_df, file2_df = make_headers_same(
        file1_df, file2_df)

    write_to_file("Chunking up dataframes.")
    file1_df_chunks = np.split(file1_df, find_max_prime_divisor(len(file1_df)))
    file2_df_chunks = np.split(file2_df, find_max_prime_divisor(len(file2_df)))

    write_to_file("Getting differences in chunks")
    file1_differences, file2_differences = write_chunk_differences_to_df(
        file1_df_chunks, file2_df_chunks)

    # TODO: Guard statement to exit program if either file1_difference or file2_differences are empty
    # if file1_differences == None or file2_differences == None:
    #     write_to_file(
    #         "ERROR: Cannot continue with comparisons - exiting program.")
    #     return

    difference_truth_table = file1_differences == file2_differences

    write_to_file(
        f"Creating output dataframe with columns: Affected Index, Affected Column, {file1_filepath}_data, and {file2_filepath}_data")
    output_df = pd.DataFrame(columns=[
                             "Affected Index", "Affected Column", f"{file1_filepath}_data", f"{file2_filepath}_data"])

    new_rows = []

    for i in range(len(file1_differences)):
        write_to_file("--------start")
        write_to_file(f"{file1_filepath}:")
        write_to_file(file1_differences.iloc[[i]].values)

        write_to_file("")

        write_to_file(f"{file2_filepath}:")
        write_to_file(file2_differences.iloc[[i]].values)
        write_to_file("--------end")
        write_to_file("")

        file1_data = file1_differences.iloc[[i]].values.tolist()
        file2_data = file2_differences.iloc[[i]].values.tolist()

        truth_row = difference_truth_table.iloc[[i]].values.tolist()

        index_difference = file1_data

        file1_difference = None
        file2_difference = None
        col_difference = None

        for col in range(len(difference_truth_table.columns)):
            if truth_row[0][col] == False:
                file1_difference = file1_data[0][col]
                file2_difference = file2_data[0][col]
                col_difference = difference_truth_table.columns[col]
        new_row = {
            "Affected Index": index_difference[0][0],
            "Affected Column": col_difference,
            f"{file1_filepath}_data": file1_difference,
            f"{file2_filepath}_data": file2_difference
        }

        new_rows.append(pd.DataFrame(new_row, index=[0], columns=[
            "Affected Index", "Affected Column", f"{file1_filepath}_data", f"{file2_filepath}_data"]))

    return pd.concat(new_rows, ignore_index=False)


def main():
    df = compare_csvs(sys.argv[1], sys.argv[2])
    df.to_excel('output/results.xlsx')


if __name__ == '__main__':
    main()
