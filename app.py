import streamlit as st
from pathlib import Path
import os
from image_to_text import image_to_text
from doc_comparer import doc_compare
from doc_summarizer import Chunk_and_Summarize
import time

# title of the streamlit app
st.title(f""":rainbow[Architecture Diagram with Amazon Bedrock]""")

# Insert containers separated into tabs:
tab1, tab2, tab3 = st.tabs(["Document Summarizer", "Documents Comparison", "Architecture Diagram"])

with tab1:
  # default container that houses the document upload field
    with st.container():
        st.header(f""":rainbow[PDF Document Summarization (Claude 2)]""")
        # header that is shown on the web UI
        st.subheader('PDF File Upload')
        # the file upload field, the specific ui element that allows you to upload the file
        File = st.file_uploader('Upload a file', type=["pdf"], key="doc_sum")
        # when a file is uploaded it saves the file to the directory, creates a path, and invokes the
        # Chunk_and_Summarize Function
        if File is not None:
            # determine the path to temporarily save the PDF file that was uploaded
            save_folder = os.getenv("save_folder")
            # create a posix path of save_folder and the file name
            save_path = Path(save_folder, File.name)
            # write the uploaded PDF to the save_folder you specified
            with open(save_path, mode='wb') as w:
                w.write(File.getvalue())
            # once the save path exists...
            if save_path.exists():
                # write a success message saying the file has been successfully saved
                st.success(f'File {File.name} is successfully saved!')
                # creates a timer to time the length of the summarization task and starts the timer
                start = time.time()
                # running the summarization task, and outputting the results to the front end
                st.write(Chunk_and_Summarize(save_path))
                # ending the timer
                end = time.time()
                # using the timer, we calculate the minutes and seconds it took to perform the summarization task
                seconds = int(((end - start) % 60))
                minutes = int((end - start) // 60)
                # string to highlight the amount of time taken to complete the summarization task
                total_time = f"""Time taken to generate a summary:
                Minutes: {minutes} Seconds: {round(seconds, 2)}"""
                # sidebar is created to display the total time taken to complete the summarization task
                with st.sidebar:
                    st.header(total_time)
                # removing the PDF that was temporarily saved to perform the summarization task
                os.remove(save_path)

with tab2:
    # default container that houses the document upload field
    with st.container():
        # header that is shown on the web UI
        st.header(f""":rainbow[PDF Document Comparison (Claude 2)]""")
        st.subheader('PDF File Upload')
        # the first file upload field, the specific ui element that allows you to upload file 1
        File1 = st.file_uploader('Upload File 1', type=["pdf"], key="doc_comp_1")
        # the second file upload field, the specific ui element that allows you to upload file 2
        File2 = st.file_uploader('Upload File 2', type=["pdf"], key="doc_comp_2")
        # when both files are uploaded it saves the files to the directory, creates a path, and invokes the
        # doc_compare Function
        if File1 and File2 is not None:
            # determine the path to temporarily save the PDF file that was uploaded
            save_folder = os.getenv('save_folder')
            # create a posix path of save_folder and the first file name
            save_path_1 = Path(save_folder, File1.name)
            # create a posix path of save_folder and the second file name
            save_path_2 = Path(save_folder, File2.name)
            # write the first uploaded PDF to the save_folder you specified
            with open(save_path_1, mode='wb') as w:
                w.write(File1.getvalue())
            # write the second uploaded PDF to the save_folder you specified
            with open(save_path_2, mode='wb') as w:
                w.write(File2.getvalue())
            # once the save path exists for both documents you are trying to compare...
            if save_path_1.exists() and save_path_2.exists():
                # write a success message saying the first file has been successfully saved
                st.success(f'File {File1.name} is successfully saved!')
                # write a success message saying the second file has been successfully saved
                st.success(f'File {File2.name} is successfully saved!')
                # creates a timer to time the length of the summarization task and starts the timer
                start = time.time()
                # running the document comparison task, and outputting the results to the front end
                st.write(doc_compare(save_path_1, save_path_2))
                # ending the timer
                end = time.time()
                # using the timer, we calculate the minutes and seconds it took to perform the summarization task
                seconds = int(((end - start) % 60))
                minutes = int((end - start) // 60)
                # string to highlight the amount of time taken to complete the summarization task
                total_time = f"""Time taken to compare the documents:
                Minutes: {minutes} Seconds: {round(seconds, 2)}"""
                # sidebar is created to display the total time taken to complete the summarization task
                with st.sidebar:
                    st.header(total_time)
                # removing the first PDF that was temporarily saved to perform the comparison task
                os.remove(save_path_1)
                # removing the second PDF that was temporarily saved to perform the comparison task
                os.remove(save_path_2)
    
with tab3:
    st.header(f""":rainbow[Diagram Analysis (Claude 3 Sonnet)]""")
    with st.container():
        # header that is shown on the web UI
        st.subheader('Image File Upload:')
        # the image upload field, the specific ui element that allows you to upload an image
        # when an image is uploaded it saves the file to the directory, and creates a path to that image
        File = st.file_uploader('Upload an Image', type=["png", "jpg", "jpeg"], key="diag")
        # this is the text box that allows the user to insert a question about the uploaded image or a question in general
        text = st.text_input("OPTIONAL: Do you have a question about the image? Or about anything in general?")
        # this is the button that triggers the invocation of the model, processing of the image and/or question
        result1 = st.button("Describe Diagram")
        result2 = st.button("Generate CDK Code")
        input_text = ""

        if File is not None:
            # the image is displayed to the front end for the user to see
            st.image(File)
            # determine the path to temporarily save the image file that was uploaded
            save_folder = os.getenv("save_folder")
            # create a posix path of save_folder and the file name
            save_path = Path(save_folder, File.name)
            # write the uploaded image file to the save_folder you specified
            with open(save_path, mode='wb') as w:
                w.write(File.getvalue())
            # once the save path exists...
            if save_path.exists():
                # write a success message saying the image has been successfully saved
                st.success(f'Image {File.name} is successfully saved!')
            if result1:
                input_text = "You are a AWS solution architect. The image provided is an architecture diagram. Explain the technical data flow in detail. Do not use preambles."
                # if text is not empty, concatenate the input text with the text that the user inserted
                if text != "":
                    input_text = input_text + "Answer these questions: " + text
                # running the image to text task, and outputting the results to the front end
                st.write(image_to_text(File.name, input_text))
                # removing the image file that was temporarily saved to perform the question and answer task
                os.remove(save_path)
                input_text = ""
            elif result2:
                input_text = "You are a AWS solution architect. The image provided is an architecture diagram. Provide cdk python code to implement using aws-cdk-lib in detail. Do not use preambles. Be extremely precise and detailed."
                # if text is not empty, concatenate the input text with the text that the user inserted
                if text != "":
                    input_text = input_text + "Before providing the code, also answer these questions: " + text
                # running the image to text task, and outputting the results to the front end
                st.write(image_to_text(File.name, input_text))
                # removing the image file that was temporarily saved to perform the question and answer task
                os.remove(save_path)
                input_text = ""
