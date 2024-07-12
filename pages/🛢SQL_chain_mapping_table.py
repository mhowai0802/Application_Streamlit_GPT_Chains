import utils
import sqlite3
import streamlit as st
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy import create_engine
import pymysql

pymysql.install_as_MySQLdb()
import MySQLdb
from langchain_community.callbacks import StreamlitCallbackHandler
from testing.Ollama_sql_chain_mapping import *
from deep_translator import GoogleTranslator
from sqlalchemy import text

st.set_page_config(page_title="ChatSQL", page_icon="🛢")
st.header('Chat with SQL database')
st.write('Enable the chatbot to interact with a SQL database through simple, conversational commands.')
st.write(
    '[![view source code ](https://img.shields.io/badge/view_source_code-gray?logo=github)](https://github.com/shashankdeshpande/langchain-chatbot/blob/master/pages/5_%F0%9F%9B%A2_chat_with_sql_db.py)')


class SqlChatbot:
    def __init__(self):
        self.openai_model = utils.configure_openai()
    @utils.enable_chat_history
    def main(self):
        ollama_chain_obj = translation_chain()
        user_query = st.chat_input(placeholder="Ask me anything!")
        engine = create_engine('mysql://root:joniwhfe@localhost/Text2SQL_english')
        if user_query:
            st.session_state.messages.append({"role": "user", "content": user_query})
            st.chat_message("user").write(user_query)
            with st.chat_message("assistant"):
                st_cb = StreamlitCallbackHandler(st.container())
                chain = ollama_chain_obj.run('mysql://root:joniwhfe@localhost/Text2SQL_english')
                translated = chain.invoke({"question": user_query})
                # response = translated.split("\n")[0].replace("`", "").replace("'", "")
                st.session_state.messages.append({"role": "assistant", "content": translated})
                st.write(translated)


if __name__ == "__main__":
    obj = SqlChatbot()
    obj.main()
