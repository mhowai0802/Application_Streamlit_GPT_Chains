import pandas as pd
from sqlalchemy import create_engine
import pymysql

pymysql.install_as_MySQLdb()
import MySQLdb
import sqlalchemy as sa
from langchain_community.utilities import SQLDatabase
from deep_translator import (GoogleTranslator)
# =================================================================
engine = sa.create_engine('mysql://root:joniwhfe@localhost/Testing')
db = SQLDatabase(engine)
schema = db.get_table_info()
dict = {'table_name': schema.split('\n')[1].split(' ')[2].split('.')[0].strip('`'),
        'column_names': schema.split('\n')[-5].replace('	', ' ').split(' ')
        }
cnx = engine.connect()
df = pd.read_sql_table('商表', cnx)
# =================================================================
translator = GoogleTranslator()
for element in dict['column_names']:
    translated = GoogleTranslator(source='auto', target='en').translate(text=element)
    print(element, translated)
    df.rename(columns={element: translated.replace(" ","_")}, inplace=True)
df.rename(columns={'Profit_margin_before_interest,_taxes,_depreciation_and_amortization': 'Profit_margin_before'}, inplace=True)
df.rename(columns={'Interests_in_associated_companies_and_jointly_controlled_companies': 'Interests_in_associated_companies'}, inplace=True)

# =================================================================

df['company'] = df['company'].apply(translator.translate, src='auto', dest='en')
df['Auditor\'s_opinion'] = df['Auditor\'s_opinion'].apply(translator.translate, src='auto', dest='en')
df['company'] = df['company'].apply(lambda x: x.replace(" ", "_"))

print(df.to_csv("data_source/Sensetime_financial_data.csv", index=False))