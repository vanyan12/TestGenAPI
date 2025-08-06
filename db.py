import pyodbc

def connect_to_db():
    return pyodbc.connect(
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=localhost;"
    "Database=TestGen;"
    "Trusted_Connection=yes;"
)

# def connect_to_db():
#     return pyodbc.connect(
#         "Driver={ODBC Driver 18 for SQL Server};"
#         "Server=34.30.127.124;"
#         "Database=TestGen;"
#         "Uid=sqlserver;"
#         "Pwd=van203;"
#         "Encrypt=yes;"
#         "TrustServerCertificate=yes;"
#     )




