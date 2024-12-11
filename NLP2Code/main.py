import pandas as pd
import os
from openai import OpenAI
import pandasql as ps

OPEN_AI_KEY = ""

client = OpenAI(api_key=OPEN_AI_KEY)


def read_csv_to_dataframe(file_name):
    # Check if the file exists
    if os.path.isfile(file_name):
        # Read the CSV file into a DataFrame
        df = pd.read_csv(file_name)
        return df
    else:
        raise FileNotFoundError(f"The file {file_name} does not exist.")


def describe_df(df: pd.DataFrame):
    description = "The dataframe has the follwoing columns: "
    for column in df.columns:
        description += f" - {column} (type: {df[column].dtype})\n"
    description += f"Here are first few rows pof teh dataftame : \n"
    description += df.head().to_string(index=False)
    return description


def generate_python_code_from_query(dataframe: pd.DataFrame, query: str) -> str:
    df_description = describe_df(dataframe)
    # Construct the prompt
    prompt = f"""
            - Role - You are a SQL programmer who can write code to extract specific information from a Pandas DataFrame based on a natural language query.
            - You are provided with the following Dataframe structure and sample data : {df_description}
            - Do not create sample dataframe
            - Do not expolain the logic.
            - Function name should be 'get_data_from_df'
            - The last line in the code after function definition should be 'output_df = get_data_from_df(df)'
            - Ask for clarification if required
           """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": query},
        ]
    )
    generated_code = response.choices[0].message.content.replace("```python\n", "").replace("```", "")
    return generated_code


def dataframe_info_to_string(dataframe: pd.DataFrame) -> str:
    """
    Converts the DataFrame structure to a string for use in a prompt.

    Args:
    - dataframe (pd.DataFrame): The DataFrame to convert.

    Returns:
    - str: A textual description of the DataFrame's columns and types.
    """
    # Extract column names and data types
    column_info = ""
    for col in dataframe.columns:
        column_info += f"- Column '{col}': {dataframe[col].dtype}\n"

    return column_info


def execute_sql_code(dataframe: pd.DataFrame, sql_code: str):
    """
    Executes the provided Python code on the given DataFrame.

    Args:
    - dataframe (pd.DataFrame): The pandas DataFrame to operate on.
    - python_code (str): A string containing Python code to execute.

    Returns:
    - Any: The result of the execution (could be any type).
    """
    # Local variables dictionary to store variables, including the dataframe

    try:
        # Execute the provided Python code within the context of local_vars
        return ps.sqldf(sql_code, locals())
    except Exception as e:
        return str(e)


# Example usage
if __name__ == "__main__":
    # Sample DataFrame
    file_name = 'customers.csv'
    df = read_csv_to_dataframe(file_name)

    # Query about the DataFrame
    user_query = "Find customers with first name starts with T?"

    # Generate Python code from query
    code = generate_python_code_from_query(df, user_query)
    print(execute_sql_code(df, code))

