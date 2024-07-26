import utils
import streamlit as st
import pymysql
pymysql.install_as_MySQLdb()
from langchain_community.callbacks import StreamlitCallbackHandler
from langchain_experimental.llms.ollama_functions import OllamaFunctions
import json
from chains.Ollama_tool import Company_annual_performance, Calculate_sum, SQL_Company_annual_performance, switch_function


st.set_page_config(page_title="ChatSQL", page_icon="🛢")
st.header('Chat with Langchain Tools')
st.write(f'Tool names : Company_annual_performance, Calculate_sum')
st.write('[![view source code ](https://img.shields.io/badge/view_source_code-gray?logo=github)](https://github.com/shashankdeshpande/langchain-chatbot/blob/master/pages/5_%F0%9F%9B%A2_chat_with_sql_db.py)')

class SqlChatbot:
    def __init__(self):
        self.openai_model = utils.configure_openai()
        llm = OllamaFunctions(model="mistral")
        self.llm_with_tools = llm.bind_tools([Company_annual_performance, Calculate_sum])
    @utils.enable_chat_history
    def main(self):
        user_query = st.chat_input(placeholder="Ask me anything!")
        if user_query:
            st.session_state.messages.append({"role": "user", "content": user_query})
            st.chat_message("user").write(user_query)
            with st.chat_message("assistant"):
                st_cb = StreamlitCallbackHandler(st.container())
                result = self.llm_with_tools.invoke(user_query)
                ans = json.loads(result.json())['tool_calls'][0]
                chosen_tool = ans['name']
                tool_input = ans['args']
                st.session_state.messages.append({"role": "assistant", "content": f"Chosen Tool: {chosen_tool}"})
                st.write(f"Chosen Tool: {chosen_tool}")
                st.session_state.messages.append({"role": "assistant", "content": tool_input})
                st.write(tool_input)
                result = switch_function(ans)
                st.session_state.messages.append({"role": "assistant", "content": result})
                st.write(result)


if __name__ == "__main__":
    obj = SqlChatbot()
    obj.main()


