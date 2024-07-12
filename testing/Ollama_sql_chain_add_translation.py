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


class ollama_sql_chain():
    # ==================================================================================================================================
    def run(self, db_link):
        llm = ChatOllama(model="deepseek-coder")
        engine = sa.create_engine(db_link)
        db = SQLDatabase(engine=engine, metadata=MetaData(schema='Text2SQL_english'))

        # ==================================================================================================================================
        def get_schema(_):
            schema = db.get_table_info()
            print(schema.split('\n')[-5].replace('	', ' ').split(' '))
            return {'table_name': schema.split('\n')[1].split(' ')[2].split('.')[1].strip('`'),
                    'column_names': schema.split('\n')[-5].replace('	', ' ').split(' ')
                    }

        # ==================================================================================================================================
        template = """
        
        ### system prompt ###
        你是一個自然語言 to SQL 專家
        
        ### table name ###
        {schema}的table
        
        ### column name ###
        {schema}的column name
        
        ### rule ###
        只能根据下面問題,编写一个SQL回答：
        问题：{question}
        生成前先檢查query的有效性
        SQL查询     
        """
        prompt = ChatPromptTemplate.from_template(template)

        # ==================================================================================================================================
        sql_chain = (
                RunnablePassthrough.assign(schema=get_schema)
                | prompt
                | llm
                | StrOutputParser()
        )
        # ==================================================================================================================================
        return sql_chain
