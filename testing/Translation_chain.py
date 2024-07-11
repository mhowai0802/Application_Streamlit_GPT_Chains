from langchain_community.llms import Ollama
from sqlalchemy import create_engine
import pymysql

pymysql.install_as_MySQLdb()
import MySQLdb
from langchain_core.output_parsers import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from langchain_community.utilities import SQLDatabase
from langchain_core.prompts import ChatPromptTemplate
import sqlalchemy as sa
from sqlalchemy import MetaData
from langchain_community.chat_models import ChatOllama
import json
import pandas as pd
import itertools
from deep_translator import GoogleTranslator
from sqlalchemy import text


def get_cell_value():
    engine = sa.create_engine('mysql://root:joniwhfe@localhost/Text2SQL_english')
    db = SQLDatabase(engine=engine, metadata=MetaData(schema='Text2SQL_english'))
    with engine.connect() as conn, conn.begin():
        df = pd.read_sql_query('Select * from Sensetime_financial_data;', conn)
        merged = list(itertools.chain(*df[['company', 'Auditor\'s_opinion']].values.tolist()))
        merged_deduplicated = list(set(merged))
        for english in merged_deduplicated:
            chinese = GoogleTranslator(source='auto', target='zh-TW').translate(text=english)
            mySql_insert_query = f'INSERT INTO translations (source_name, translation_name) VALUES ("{chinese}", "{english}");'
            conn.execute(text(mySql_insert_query))

class translation_chain():
    # ==================================================================================================================================
    def run(self, db_link):
        llm = ChatOllama(model="mistral")
        engine = sa.create_engine(db_link)
        db = SQLDatabase(engine=engine, metadata=MetaData(schema='Text2SQL_english'))

        # ==================================================================================================================================
        def get_schema(_):
            with engine.connect() as conn, conn.begin():
                source_name = pd.read_sql_query('Select source_name from translations;', conn)
                target_name = pd.read_sql_query('Select translation_name from translations;', conn)
                return {'chinese': sum(source_name.values.tolist(), []),
                        'english': sum(target_name.values.tolist(), [])
                        }
        # ==================================================================================================================================
        template = """

        ### system prompt ###
        你是一個翻釋專家, 不要編作資料。

        ### rule ###
        跟據{question}, 將中文問題變成英文問題, 不要作其他回應, 數字不用理會。
        
        ### translation library ###
        {schema}  
        """
        prompt = ChatPromptTemplate.from_template(template)

        # ==================================================================================================================================
        trans_chain = (
                RunnablePassthrough.assign(schema=get_schema)
                | prompt
                | llm
                | StrOutputParser()
        )
        # ==================================================================================================================================
        return trans_chain

object = translation_chain()
chain = object.run('mysql://root:joniwhfe@localhost/Text2SQL_english')
print("Starting translation...................")
question = "商湯科技集團有限公司2023年的毛利？"
print(question)
print(chain.invoke({"question": question}))
