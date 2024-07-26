import re
from sqlalchemy import create_engine
import pymysql
import sqlalchemy as sa
from sqlalchemy import MetaData
pymysql.install_as_MySQLdb()
from langchain_community.utilities import SQLDatabase

engine = sa.create_engine('mysql://root:joniwhfe@localhost/Text2SQL_english')
db = SQLDatabase(engine=engine, metadata=MetaData(schema='Text2SQL_english'))
schema = db.get_table_info()
print(schema)
print("================================================================")
pattern = re.compile(r'\((.*?)\)', re.DOTALL)

# Search for the pattern
match = pattern.search(schema)

if match:
    # Extract the string inside parentheses
    content_inside_parentheses = match.group(1)

    # Regular expression to find all column names
    column_pattern = re.compile(r'`?([\w/()]+)`?\s+\w+')

    # Find all matches
    columns = column_pattern.findall(content_inside_parentheses)

    # Print the list of column names
    print(columns)