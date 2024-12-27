import os
import pandas as pd


def read_csv_to_dataframe(file_name: str) -> pd.DataFrame:
    """
    Reads a CSV file into a pandas DataFrame.

    Args:
    - file_name (str): The name of the file to read.

    Returns:
    - pd.DataFrame: The DataFrame created from the CSV file.

    Raises:
    - FileNotFoundError: If the file does not exist.
    """
    if os.path.isfile(file_name):
        return pd.read_csv(file_name)
    else:
        raise FileNotFoundError(f"The file {file_name} does not exist.")


def describe_df(dataframe: pd.DataFrame) -> str:
    """
    Describes the DataFrame structure and sample data.

    Args:
    - dataframe (pd.DataFrame): The DataFrame to describe.

    Returns:
    - str: A description of the DataFrame.
    """
    description = "The DataFrame has the following columns:\n"
    for column in dataframe.columns:
        description += f" - {column} (type: {dataframe[column].dtype})\n"
    description += f"\nHere are the first few rows of the DataFrame:\n{dataframe.head().to_string(index=False)}"
    return description


def dataframe_info_to_string(dataframe: pd.DataFrame) -> str:
    """
    Converts DataFrame structure to a string for use in prompts.

    Args:
    - dataframe (pd.DataFrame): The DataFrame to convert.

    Returns:
    - str: A textual description of the DataFrame's columns and types.
    """
    column_info = ""
    for col in dataframe.columns:
        column_info += f"- Column '{col}': {dataframe[col].dtype}\n"
    return column_info
