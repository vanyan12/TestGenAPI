import pyodbc

def connect_to_db():
    return pyodbc.connect(
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=localhost;"
    "Database=Project;"
    "Trusted_Connection=yes;"
)




