# GenAI Architecture PoC

This is sample code demonstrating the use of Amazon Bedrock and Generative AI to simplify some daily tasks:

1. Summarize a long document
2. Compare two documents
3. Insert text questions, images, or both to get a comprehensive description or answers or IaC code based on the architecture diagram and questions that was passed in.

This repo comes with a basic frontend to help users stand up a proof of concept in just a few minutes.

Part of this code is explained [here](https://letsmake.cloud/transforming-diagrams-into-code). It's also heavily inspired by another repo, which you can find [here](https://github.com/aws-samples/genai-quickstart-pocs).

## Prerequisites

1. Amazon Bedrock Access and CLI Credentials.
2. Ensure Python 3.9 installed on your machine, it is the most stable version of Python for the packages we will be using, it can be downloaded [here](https://www.python.org/downloads/release/python-3911/).

## Step 1

After cloning the repo onto your local machine, open it up in your favorite code editor.
Set up a python virtual environment in the root directory of the repository and ensure that you are using Python 3.9. This can be done by running the following commands:

```
pip install virtualenv
python3.9 -m venv venv
```

The virtual environment will be extremely useful when you begin installing the requirements. If you need more clarification on the creation of the virtual environment please refer to this [blog](https://www.freecodecamp.org/news/how-to-setup-virtual-environments-in-python/).
After the virtual environment is created, ensure that it is activated, following the activation steps of the virtual environment tool you are using. Likely:

```
source venv/bin/activate
```

After your virtual environment has been created and activated, you can install all the requirements found in the requirements.txt file by running this command in the root of this repos directory in your terminal:

```
pip install -r requirements.txt
```

## Step 2

Now that the requirements have been successfully installed in your virtual environment we can begin configuring environment variables.
You will first need to create a .env file in the root of this repo. Within the .env file you just created you will need to configure the .env to contain:

```
profile_name=<AWS_CLI_PROFILE_NAME>
save_folder=<PATH_TO_ROOT_OF_THIS_REPO>
```

Please ensure that your AWS CLI Profile has access to Amazon Bedrock.

## Step 3

As soon as you have successfully cloned the repo, created a virtual environment, activated it, installed the requirements.txt, and created a .env file, your application should be ready to go.
To start up the application with its basic frontend you simply need to run the following command in your terminal while in the root of the repository's directory:

```
streamlit run app.py
```
