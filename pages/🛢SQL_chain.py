import utils
import sqlite3
import streamlit as st
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy import create_engine
import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb
import sqlalchemy as sa
from langchain_community.callbacks import StreamlitCallbackHandler
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.llms import Ollama
from langchain.chains import create_sql_query_chain
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate
from langchain_community.agent_toolkits import create_sql_agent
from testing.Ollama_sql_chain import *

st.set_page_config(page_title="ChatSQL", page_icon="🛢")
st.header('Chat with SQL database')
st.write('Enable the chatbot to interact with a SQL database through simple, conversational commands.')
st.write('[![view source code ](https://img.shields.io/badge/view_source_code-gray?logo=github)](https://github.com/shashankdeshpande/langchain-chatbot/blob/master/pages/5_%F0%9F%9B%A2_chat_with_sql_db.py)')

class SqlChatbot:
    def __init__(self):
        self.openai_model = utils.configure_openai()
    def setup_db(_self, db_uri):
        engine = sa.create_engine(db_uri)
        db = SQLDatabase(engine)
        with st.sidebar.expander('Database tables', expanded=True):
            st.info('\n- ' + '\n- '.join(db.get_usable_table_names()))
        return db

    @utils.enable_chat_history
    def main(self):
        ollama_chain_obj = ollama_sql_chain()
        user_query = st.chat_input(placeholder="Ask me anything!")
        if user_query:
            st.session_state.messages.append({"role": "user", "content": user_query})
            st.chat_message("user").write(user_query)
            with st.chat_message("assistant"):
                st_cb = StreamlitCallbackHandler(st.container())
                chain = ollama_chain_obj.run('mysql://root:joniwhfe@localhost/Testing')
                result = chain.invoke({"question": user_query})
                response = result.split("\n")[0].replace("`", "").replace("'","")
                print("================================================")
                print(f"Result: {response}")
                print("================================================")
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.write(response)


if __name__ == "__main__":
    obj = SqlChatbot()
    obj.main()


