import streamlit as st
import requests
from langchain.prompts import PromptTemplate
from langchain_community.document_loaders import TextLoader
from langchain.chains.llm import LLMChain
from langchain_openai import ChatOpenAI
import openai
from langchain.chains.summarize import load_summarize_chain
from dotenv import dotenv_values

def main():
    st.title("Context for ChatGPT model")

    # widget for uploading files
    files = st.file_uploader("Select files", type=["txt", "md"], accept_multiple_files=True)

    if files:
        if st.button("Send files"):
            send_files(files)
            
def processing(f, content):
    #openai key
    openai_api_key = str(dotenv_values("../.env")['OPENAI_API_KEY'])
    
    # prompt template definition
    prompt_template = f"""Write a concise summary and analysis of the following text:
    "{content}"
    SUMMARY:"""
    prompt = PromptTemplate.from_template(prompt_template)
    
    # loading the model
    llm = ChatOpenAI(openai_api_key=openai_api_key, model="gpt-3.5-turbo")
    summary = llm.invoke(prompt_template)
        
    # saving the summary
    with open(f'../summaries/summary_{f.name}.txt', 'w') as summarized:
        summarized.write(summary.content)
    
    st.markdown("# Analysis over the docs")
    st.markdown(f"## {f.name}")
    st.markdown(str(summary.content))
            
def send_files(files):
    # api where the files should be sent
    api = "http://localhost:8000/api/upload-file/"
    
    # create a tuple for each file. It can be used list comprehension or append method.
    files_tuple = []
    for f in files:
        files_tuple.append(("file", (f.name, f)))
        print(f.name)
        content = open(f'../files/{f.name}')
        processing(f, content)
    
    # saving the response
    response = requests.post(api, files=files_tuple)
    
    # verify the answer
    if response.status_code == 201:
        st.success("Files sucessfully sent to the server.")
    else:
        st.error(f"Error! Messages have not been processed. {response.status_code} - {response.text}")

if __name__ == "__main__":
    main()