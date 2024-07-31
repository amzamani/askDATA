# Import necessary libraries and modules
import streamlit as st
import pandas as pd
# from pandasai import PandasAI

# new code
from pandasai import SmartDataframe
# from pandasai.llm import OpenAI
# from pandasai.llm import BambooLLM
from pandasai.llm import GooglePalm
from pandasai.responses.response_parser import ResponseParser

# new code
# from pandasai.llm.openai import OpenAI
# import openai

# Get API key
# OPENAI_API_KEY = st.secrets['OPENAI_API_KEY']
API_KEY = st.secrets['API_KEY'] 
class PandasDataFrame(ResponseParser):
    def __init__(self, context) -> None:
        super().__init__(context)

    def format_dataframe(self, result):
        # Returns Pandas Dataframe instead of SmartDataFrame
        return result["value"]

# Set OpenAI API key
# openai.api_key = OPENAI_API_KEY

# Set page configuration and title for Streamlit
st.set_page_config(page_title="askDATA", page_icon="📄", layout="wide")

# Add header with title and description
st.markdown(
    '<p style="display:inline-block;font-size:40px;font-weight:bold;">📊askDATA <br><br></p>'
    ' <p style="display:inline-block;font-size:16px;">askDATA is tool that uses AI-powered '
    'natural language processing to analyze and provide insights on CSV data. Users can '
    'upload CSV files, view the data, and have interactive conversations with the AI model '
    'to obtain valuable information and answers related to the uploaded data <br><br></p>',
    unsafe_allow_html=True
)

def chat_with_csv(df, prompt):
    # llm = OpenAI(api_token=OPENAI_API_KEY)
    # pandas_ai = PandasAI(llm)
    # result = pandas_ai.run(df, prompt=prompt)
    # llm = BambooLLM(api_key=API_KEY)
    llm = GooglePalm(api_key=API_KEY)

 
    sdf = SmartDataframe(df, config={"llm": llm, "response_parser": PandasDataFrame,"enable_cache": False,"save_logs": False})
    response = sdf.chat(prompt)
    result = response
    print(result)
    return result

input_csv = st.file_uploader("Upload your CSV file", type=['csv'])

if input_csv is not None:
    col1, col2 = st.columns([1, 1])

    with col1:
        st.info("CSV Uploaded Successfully")
        data = pd.read_csv(input_csv)
        st.dataframe(data, use_container_width=True)

    with col2:
        st.info("Chat Below")
        input_text = st.text_area("Enter your query")

        if input_text is not None:
            if st.button("Chat"):
                st.info("Your Query: " + input_text)
                result = chat_with_csv(data, input_text)
                st.success(result)

# Hide Streamlit header, footer, and menu
hide_st_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
"""

# Apply CSS code to hide header, footer, and menu
st.markdown(hide_st_style, unsafe_allow_html=True)
