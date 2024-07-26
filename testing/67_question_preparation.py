import pandas as pd
import csv

classificaiton_txt = '數據查詢 數據查詢 數據查詢 數據查詢 領域概念 數據分析 數據分析 歸納摘要 數據查詢 數據查詢 數據查詢 數據查詢 數據查詢 數據查詢 歸納摘要 數據查詢 數據查詢 數據查詢 數據查詢 數據查詢 數據查詢 數據查詢 數據查詢 數據查詢 數據查詢 數據查詢 數據查詢 數據查詢 歸納摘要 數據查詢 歸納摘要 數據查詢 數據查詢 歸納摘要 歸納摘要 歸納摘要 歸納摘要 數據查詢 數據查詢 數據查詢 數據查詢 歸納摘要 歸納摘要 歸納摘要'
list_of_questions = []
with open('data_source/source_text_67_questions.txt', 'r') as f:
    for line in f.readlines():
        question = line.strip()
        list_of_questions.append(question)
classificaiton_list = classificaiton_txt.split(' ')

print(list_of_questions,len(classificaiton_list))

dict = {'question': list_of_questions, 'classification': classificaiton_list}
df = pd.DataFrame(dict)

df.to_csv('data_source/output.csv')