import pyodbc


try:
    # Replace with your actual connection details
    conn_str = (
    r"DRIVER={ODBC Driver 17 for SQL Server};"
    r"SERVER=APB-JBS02-113L\\SQLEXPRESS;"
    r"DATABASE=blog;"
    r"UID=APB-JBS02-113L\\JBS LAB;"
    r"PWD=Malvapudding78*;"
)

    conn = pyodbc.connect(conn_str)
    # Execute a query
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM User")

    # Fetch and print results
    for row in cursor:
        print(row)

except pyodbc.Error as e:
    print("Error:", e)

finally:
    if conn:
        conn.close()