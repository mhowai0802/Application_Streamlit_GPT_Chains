from langchain_community.llms import Ollama
from sqlalchemy import create_engine
import pymysql

pymysql.install_as_MySQLdb()
import MySQLdb
from langchain_core.output_parsers import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from langchain_openai import ChatOpenAI
from langchain_community.utilities import SQLDatabase
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_sql_query_chain
import sqlalchemy as sa
from sqlalchemy import MetaData
from langchain_community.agent_toolkits import create_sql_agent
from langchain_community.chat_models import ChatOllama
import json
import re
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.utils.math import cosine_similarity
import numpy as np

database = {
    'host': "localhost",
    'user': "root",
    'password': "joniwhfe",
    'database': "Text2SQL_english"
}

conn = pymysql.connect(
    host=database['host'],
    user=database['user'],
    password=database['password'],
    database=database['database']
)
cursor = conn.cursor()
query = """
SELECT
	COLUMN_NAME
FROM
	INFORMATION_SCHEMA.COLUMNS
WHERE
	TABLE_NAME = N'Sensetime_financial_data';
"""
cursor.execute(query)
column_name = cursor.fetchall()
cursor.close()

column_list = [item[0] for item in column_name]

k = 3
query = 'sensetime 2022 gross profit?'
embed_model = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")
query_vector = embed_model.embed_query(query)
example_query_vector = embed_model.embed_documents(column_list)
similiarity = cosine_similarity([query_vector], example_query_vector)[0]
sorted_similarity_i = np.argsort(similiarity)[::-1]
best_match = [column_list[i] for i in sorted_similarity_i[0:k]]
print(best_match)