import boto3
import json
import os
import botocore.config
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
import tiktoken
from pypdf import PdfReader

# loading environment variables
load_dotenv()
# configure Bedrock client
boto3.setup_default_session(profile_name=os.getenv("profile_name"))
config = botocore.config.Config(connect_timeout=120, read_timeout=120)
bedrock = boto3.client('bedrock-runtime', 'us-east-1', endpoint_url='https://bedrock-runtime.us-east-1.amazonaws.com',
                       config=config)

def summarizer(prompt_data) -> str:
    """
    This function creates the summary of each individual chunk as well as the final summary.
    :param prompt_data: This is the prompt along with the respective chunk of text, at the end it contains all summary chunks combined.
    :return: A summary of the respective chunk of data passed in or the final summary that is a summary of all summary chunks.
    """
    # setting the key parameters to invoke Amazon Bedrock
    body = json.dumps({"prompt": prompt_data,
                       "max_tokens_to_sample": 8191,
                       "temperature": 0,
                       "top_k": 250,
                       "top_p": 0.5,
                       "stop_sequences": []
                       })
    # the specific Amazon Bedrock model you are using
    modelId = 'anthropic.claude-v2'
    # type of data that should be expected upon invocation
    accept = 'application/json'
    contentType = 'application/json'
    # the invocation of bedrock, with all of the parameters you have configured
    response = bedrock.invoke_model(body=body,
                                    modelId=modelId,
                                    accept=accept,
                                    contentType=contentType)
    # gathering the response from bedrock, and parsing to get specifically the answer
    response_body = json.loads(response.get('body').read())
    answer = response_body.get('completion')
    # returning the final summary for that chunk of text
    return answer


def Chunk_and_Summarize(uploaded_file) -> str:
    """
    This function takes in the path to the file that was just uploaded through the streamlit app.
    :param uploaded_file: This is a file path, that should point to the newly uploaded file that is temporarily stored
    within the directory of this application.
    :return: This returns the final summary of the PDF document that was initially passed in by the user through the
    streamlit app.
    """
    # using PyPDF PdfReader to read in the PDF file as text
    reader = PdfReader(uploaded_file)
    # creating an empty string for us to append all the text extracted from the PDF
    text = ""
    # a simple for loop to iterate through all pages of the PDF we uploaded
    for page in reader.pages:
        # as we loop through each page, we extract the text from the page and append it to the "text" string
        text += page.extract_text() + "\n"
    # creating the text splitter, we are specifically using the the recursive text splitter from langchain:
    # https://python.langchain.com/docs/modules/data_connection/document_transformers/text_splitters/recursive_text_splitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=10000,
        chunk_overlap=100,
        length_function=len,
        add_start_index=True
    )
    # using the text splitter to split the entire string of text that contains all the text content of our PDF
    texts = text_splitter.create_documents([text])
    # Creating an empty summary string, as this is where we will append the summary of each chunk
    summary = ""
    # looping through each chunk of text we created, passing that into our prompt and generating a summary of that chunk
    for index, chunk in enumerate(texts):
        # gathering the text content of that specific chunk
        chunk_content = chunk.page_content
        # creating the prompt that will be passed into Bedrock with the text content of the chunk
        prompt = f"""\n\nHuman: Provide a detailed summary for the chunk of text provided to you:
        Text: {chunk_content}
        \n\nAssistant:"""
        # passing the prompt into the summarizer function to generate the summary of that chunk, and appending it to
        # the summary string
        summary += summarizer(prompt)
        # TODO: printing out the number of tokens contained in each chunk to provide a status update
        # print(f"\n\nNumber of tokens for Chunk {index + 1} with the prompt: {num_tokens_from_string(prompt)} tokens")
        # print("-------------------------------------------------------------------------------------------------------")
    # after we have generated the summaries of each chunk of text, and appended them to the single summary string,
    # we pass it into the final summary prompt
    final_summary_prompt = f"""\n\nHuman: You will be given a set of summaries from a document. Create a cohesive 
    summary from the provided individual summaries. The summary should very detailed and at least 2 pages. 
    Summaries: {summary}
            \n\nAssistant:"""
    # generating the final summary of all the summaries we have previously generated.
    return summarizer(final_summary_prompt)


def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens