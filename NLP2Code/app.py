from sql_generator import generate_sql_query_from_nl, execute_sql_code
from data_operations import read_csv_to_dataframe, describe_df

if __name__ == "__main__":
    # Read the data
    file_name = "customers.csv"
    df = read_csv_to_dataframe(file_name)

    # Generate description
    df_description = describe_df(df)

    # Define the natural language query
    user_query = "Find customers whose first name starts with 'T'."

    # Generate the SQL query using OpenAI API
    sql_query = generate_sql_query_from_nl(df_description, user_query)
    print("Generated SQL Query:\n", sql_query)

    # Execute the SQL query
    try:
        result_df = execute_sql_code(df, sql_query)
        print("Query Result:\n", result_df)
    except ValueError as e:
        print("Error:", e)
