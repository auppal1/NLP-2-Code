import pandasql as ps
from openai import OpenAI

OPEN_AI_KEY = ""  
client = OpenAI(api_key=OPEN_AI_KEY)


def generate_sql_query_from_nl(dataframe_description: str, query: str) -> str:
    """
    Generates an SQL query from a natural language query using OpenAI API.

    Args:
    - dataframe_description (str): A textual description of the DataFrame structure.
    - query (str): The user's natural language query.

    Returns:
    - str: The generated SQL query string.
    """
    prompt = f"""
        - Role: You are a SQL programmer who can write SQL queries for pandas DataFrames.
        - You are provided with the following DataFrame structure and sample data:
          {dataframe_description}
        - Generate an SQL query to fulfill the user's request.
        - Do not create sample data, explain logic, or provide comments.
        - Provide only the SQL query.
    """

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": query},
        ]
    )

    # Extract the SQL query from the response
    sql_query = response.choices[0].message.content.strip()
    return sql_query


def execute_sql_code(dataframe, sql_query: str):
    """
    Executes the provided SQL query on the given DataFrame using pandasql.

    Args:
    - dataframe (pd.DataFrame): The pandas DataFrame to operate on.
    - sql_query (str): The SQL query to execute.

    Returns:
    - pd.DataFrame: Result of the SQL execution.
    """
    try:
        return ps.sqldf(sql_query, locals())
    except Exception as e:
        raise ValueError(f"Error in executing SQL: {e}")
