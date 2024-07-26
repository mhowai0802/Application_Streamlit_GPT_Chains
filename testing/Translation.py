from deep_translator import GoogleTranslator
from langchain_community.document_transformers import DoctranTextTranslator


question = "商湯科技集團有限公司2023年的毛利？"
translated = GoogleTranslator(source='auto', target='en').translate(text=question)
print(translated)




