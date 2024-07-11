from langchain_community.llms import Ollama
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool, StructuredTool, tool
from typing import Optional, Type
from langchain.agents import initialize_agent, AgentType, create_structured_chat_agent, create_tool_calling_agent
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain import hub
from langchain_core.prompts import PromptTemplate
from langchain_experimental.llms.ollama_functions import OllamaFunctions
import json
class Company_annual_performance(BaseModel):
    """Get the company name and financial year"""
    company_name: str = Field(description="company_name")
    financial_year: str = Field(description="financial_year")

def SQL_Company_annual_performance(compnay, financial_year):
    return f"SELECT * from annual report where company_name = {compnay} and financial_year = {financial_year}"

tools = [Company_annual_performance]
llm = OllamaFunctions(model="llama2")
llm_with_tools = llm.bind_tools(tools)
result = llm_with_tools.invoke("Tencent financial performace?")
print(json.loads(result.json())['tool_calls'][0]['name'])
print(json.loads(result.json())['tool_calls'][0]['args'])

match(json.loads(result.json())['tool_calls'][0]['name']):
    case 'Company_annual_performance':
        company = json.loads(result.json())['tool_calls'][0]['args']['company_name']
        financial_year = json.loads(result.json())['tool_calls'][0]['args']['financial_year']
        print(SQL_Company_annual_performance(company,financial_year))
