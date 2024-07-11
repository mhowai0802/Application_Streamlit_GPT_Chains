import utils
import streamlit as st
import pymysql
pymysql.install_as_MySQLdb()
import sqlalchemy as sa
from langchain_community.callbacks import StreamlitCallbackHandler
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.llms import Ollama
from langchain.tools import BaseTool, StructuredTool, Tool, tool
from langchain.agents import initialize_agent,AgentType
from langchain_experimental.llms.ollama_functions import OllamaFunctions
from langchain.pydantic_v1 import BaseModel, Field
import json

st.set_page_config(page_title="ChatSQL", page_icon="🛢")
st.header('Chat with SQL database (seperate Input)')
st.write('Choosing input in Sentence.')
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
        llm = OllamaFunctions(model="llama2")
        class Company_annual_performance(BaseModel):
            """Get the company name and financial year"""
            company_name: str = Field(description="company_name")
            financial_year: str = Field(description="financial_year")
        tools = [Company_annual_performance]
        llm_with_tools = llm.bind_tools(tools)
        user_query = st.chat_input(placeholder="Ask me anything!")
        if user_query:
            st.session_state.messages.append({"role": "user", "content": user_query})
            st.chat_message("user").write(user_query)
            with st.chat_message("assistant"):
                st_cb = StreamlitCallbackHandler(st.container())
                result = llm_with_tools.invoke(user_query)
                result = json.loads(result.json())
                tool_name = result['tool_calls'][0]['name']
                args = result['tool_calls'][0]['args']
                match tool_name:
                    case 'Company_annual_performance':
                        SQL_statement = f"SELECT * from annual report where company_name = {args['company_name']} and financial_year = {args['financial_year']}"
                st.session_state.messages.append({"role": "assistant", "content": tool_name})
                st.write(tool_name)
                st.session_state.messages.append({"role": "assistant", "content": args})
                st.write(args)
                st.session_state.messages.append({"role": "assistant", "content": SQL_statement})
                st.write(SQL_statement)

if __name__ == "__main__":
    obj = SqlChatbot()
    obj.main()