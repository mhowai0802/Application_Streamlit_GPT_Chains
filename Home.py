import streamlit as st

st.set_page_config(
    page_title="Langchain Chatbot",
    page_icon='💬',
    layout='wide'
)

st.header("Chatbot Implementations with Langchain")
st.write("""
[![view source code ](https://img.shields.io/badge/GitHub%20Repository-gray?logo=github)](https://github.com/shashankdeshpande/langchain-chatbot)
[![linkedin ](https://img.shields.io/badge/Shashank%20Deshpande-blue?logo=linkedin&color=gray)](https://www.linkedin.com/in/shashank-deshpande/)
![Visitors](https://api.visitorbadge.io/api/visitors?path=https%3A%2F%2Flangchain-chatbot.streamlit.app&label=Visitors&labelColor=%235d5d5d&countColor=%231e7ebf&style=flat)
""")
st.write("""
Langchain is a powerful framework designed to streamline the development of applications using Language Models (LLMs). It provides a comprehensive integration of various components, simplifying the process of assembling them to create robust applications.

- **SQL Chain**: Vertica database
- **VectorDB Chain**: Vector database
- **Website Chain**: Website database

To explore sample usage of each chatbot, please navigate to the corresponding chatbot section.
""")