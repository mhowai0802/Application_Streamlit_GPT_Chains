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
from langchain.agents import Tool

class Company_annual_performance(BaseModel):
    """Get the company name and financial year"""
    company_name: str = Field(description="company_name")
    financial_year: str = Field(description="financial_year")
class Calculate_sum(BaseModel):
    """Calculate the summation of two numbers"""
    first_num: str = Field(description="first_num")
    second_num: str = Field(description="second_num")

def SQL_Company_annual_performance(compnay, financial_year):
    return f"SELECT * from annual report where company_name = {compnay} and financial_year = {financial_year}"

def switch_function(tool_name_and_input):
    tool_name = tool_name_and_input['name']
    tool_input = tool_name_and_input['args']
    if tool_name == "Company_annual_performance":
        return SQL_Company_annual_performance(tool_input['company_name'],tool_input['financial_year'])
    elif tool_name == 'Calculate_sum':
        return tool_input
    else:
        return 0