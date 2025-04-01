import os
import pyodbc

# Access environment variables set in Azure
db_username = os.getenv("DB_USERNAME")
db_password = os.getenv("DB_PASSWORD")

# Now you can use db_username and db_password to connect to your Azure SQL Database
