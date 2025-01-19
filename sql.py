import pandas as pd
import sqlite3


# define function to execute queries on the created database and return a pd.DataFrame
def sql_query(sql_query_string: str,
              db_name: str = "verbatim.db"):
    # connect to SQL db
    con = sqlite3.connect(db_name)

    # execute query
    cursor = con.execute(sql_query_string)

    # get data and column names
    result_data = cursor.fetchall()
    # description attribute returns a 7-tuple for which the last 6 items are None
    # index to get the first row which is the column
    cols = [description[0] for description in cursor.description]

    # close connection
    con.close()

    # return the result as a dataframe
    return pd.DataFrame(result_data, columns=cols)

# define function to execute queries on the created database and return a pd.DataFrame
def sql_insert(row_data: list,
               db_name: str = "verbatim.db"):
    # connect to SQL db
    con = sqlite3.connect(db_name)
    cursor = con.cursor()

    # compile insert query
    insert_query = "INSERT INTO logging (filename, process_step, time_stamp) VALUES (?, ?, ?)"

    # convert data to tuple
    data_tuple = tuple(row_data)

    # execute the insert query
    cursor.execute(insert_query, data_tuple)
    con.commit()

    # close connection
    con.close()