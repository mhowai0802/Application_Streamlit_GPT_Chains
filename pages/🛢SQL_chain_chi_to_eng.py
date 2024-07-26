import utils
import streamlit as st
import pymysql
pymysql.install_as_MySQLdb()
from langchain_community.callbacks import StreamlitCallbackHandler
from deep_translator import GoogleTranslator
from sqlalchemy import text
from chains.Ollama_sql_chain_add_translation import *

########################################################################################################
database = {
    'host': "localhost",
    'user': "root",
    'password': "joniwhfe",
    'database': "Text2SQL_english"
}
table = 'Sensetime_financial_data'
model = 'deepseek-coder-v2'
embedding = 'BAAI/bge-base-en-v1.5'
k = 5
########################################################################################################
st.set_page_config(page_title="ChatSQL", page_icon="🛢")
st.header('Chat with SQL database')
st.write(f'Database link: {database}')

class SqlChatbot:
    def __init__(self):
        self.openai_model = utils.configure_openai()
        self.translation_chain_obj = ollama_sql_chain(database, table, model, embedding, k)
    @utils.enable_chat_history
    def main(self):
        user_query = st.chat_input(placeholder="Ask me anything!")
        if user_query:
            st.session_state.messages.append({"role": "user", "content": user_query})
            st.chat_message("user").write(user_query)
            with st.chat_message("assistant"):
                st_cb = StreamlitCallbackHandler(st.container())
                translated = GoogleTranslator(source='auto', target='en').translate(text=user_query)
                st.session_state.messages.append({"role": "assistant", "content": translated})
                st.write(translated)
########################################################################################################
                chain = self.translation_chain_obj.chain_generation(translated)
                result = chain.invoke(translated)
########################################################################################################
                result = result.replace('"', "").replace("[", "").replace("]", "").replace("'", "")
                st.session_state.messages.append({"role": "assistant", "content": result})
                st.write(result)
########################################################################################################
                try:
                    cursor = self.translation_chain_obj.conn.cursor()
                    cursor.execute(result)
                    sql_result = cursor.fetchall()
                    st.session_state.messages.append({"role": "assistant", "content": sql_result})
                    st.write(f"Result: {sql_result}")
                except:
                    st.session_state.messages.append({"role": "assistant", "content": "Query not valid"})
                    st.write("Result: Query not valid")
########################################################################################################
if __name__ == "__main__":
    obj = SqlChatbot()
    obj.main()
