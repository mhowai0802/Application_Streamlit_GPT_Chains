from sqlalchemy import create_engine
import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb
import sqlalchemy as sa
from langchain_community.utilities import SQLDatabase

engine = sa.create_engine('mysql://root:joniwhfe@localhost/Testing')
db = SQLDatabase(engine)
print(db.get_usable_table_names())