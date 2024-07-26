from langchain_community.llms import Ollama
from sqlalchemy import create_engine
import pymysql

pymysql.install_as_MySQLdb()
import MySQLdb
from langchain_core.output_parsers import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough, RunnableLambda
from langchain_community.agent_toolkits import create_sql_agent
from langchain_community.chat_models import ChatOllama
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.utils.math import cosine_similarity
from langchain_core.prompts import PromptTemplate
import numpy as np
from langchain_core.output_parsers import StrOutputParser


class ollama_sql_chain():
    def __init__(self, database, table, model, embedding, k):
        self.conn = pymysql.connect(
            host=database['host'],
            user=database['user'],
            password=database['password'],
            database=database['database']
        )
        self.k = k
        self.table = table
        self.llm = ChatOllama(model=model)
        self.schema = self.get_full_schema()
        self.embed_model = HuggingFaceEmbeddings(model_name=embedding)
        self.prompt = PromptTemplate.from_template("""
            ### system prompt ### 
            你是一個vertica專家。  
            
            ### rule ### 
            給定一個輸入問题,創建一個語法正確的mysql,只輸出SQL.
            
            ### table ### 
            {use_table_list}  
            
            ### column ###
            {use_column_list}  
            
            ### final step ### 
            檢查輸出SQL語法是否正確.不要加上double quotes.
            擷取column的時候，用實際在{use_column_list}拿到的名字.
            
            以上是有關資料，請不要輸出，僅輸出以下問题所需要的SQL 
            User input: {usr_question} 
            SQL query: 
        """)

# ==================================================================================================================================
    def get_full_schema(self):
        cursor = self.conn.cursor()
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
        return {
            'table': self.table,
            'column_names': column_list
        }

    def get_filter_schema(self, query, k=3):
        column_name = self.schema['column_names']
        query_vector = self.embed_model.embed_query(query)
        example_query_vector = self.embed_model.embed_documents(column_name)
        similiarity = cosine_similarity([query_vector], example_query_vector)[0]
        sorted_similarity_i = np.argsort(similiarity)[::-1]
        filtered_schema = [column_name[i] for i in sorted_similarity_i[0:self.k]]
        return filtered_schema

    def get_prompting_input(self, query):
        filtered_schema = self.get_filter_schema(query)
        input_dict = {
            'use_table_list': self.table,
            'use_column_list': filtered_schema,
            'usr_question': query
        }
        return input_dict

    def chain_generation(self, query):
        print("================================================")
        print(self.prompt.invoke(self.get_prompting_input(query)).text)
        print("================================================")
        final_chain = RunnableLambda(self.get_prompting_input) | self.prompt | self.llm.bind(
            stop=['\nSQLResult:']) | StrOutputParser()
        return final_chain
