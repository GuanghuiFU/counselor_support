# LLM-Counselors Support System

## Overview

The LLM-Counselors Support System aims to enhance the quality and efficacy of communication between counselors and individuals facing depression. It operates as an iterative system that takes an initial response formulated by a counselor and refines it into an enhanced "Reply+." This Reply+ is then reviewed by the counselor before being sent to the individual. This ensures that the advice given is both supportive and efficient.

## Workflow

![Workflow]([overflow.pdf](https://github.com/GuanghuiFU/counselor_support/blob/main/overflow.pdf))

The overall workflow is as follows:
1. The client initiates a dialogue with the counselor.
2. For complex questions, the counselor can seek assistance from the system.
3. The counselor inputs their initial response and the client's comment into the system.
4. The system performs analysis and generates an enhanced response ("Reply+") along with a report.
5. Counselors review and verify these enhanced responses before communicating them to the client.

## Features

### Privacy Information Filtering

The system has robust privacy filtering protocols, which include:
- Automatic recognition and masking of personally identifiable information.
- Trained counselors to preserve user data confidentiality.

### Construction of Prompt

The system uses a structured prompt with various components such as:
- LLM Role Definition
- Task Definition
- Role Boundaries
- Contextual and Response Requirements
- Error Identification and Rectification
- Resources
- Cognitive Distortion Classification
- Input and Output Formats

### Report Generation and Detoxify

- Utilizes GPT-3.5 for generating comprehensive reports.
- Measures similarity to offensive entries in a dataset to ensure non-offensive content.


## Usage

### Running the `chapters2chroma_csv.py` script to extract COLD dataset as vector database

The `chapters2chroma_csv.py` script serves as a utility for preparing text embeddings, specifically designed to work with the LLM-Counselors Support System. It employs the Langchain library to load documents from a CSV dataset, splits the documents into manageable chunks, and then utilizes OpenAI's GPT-3.5 model to generate text embeddings. These embeddings are stored in a Chroma vector database for further use. 


### Running the `counselor_support_gradio.py` script

The counselor_support_gradio.py script serves as the main interface and core engine of the LLM-Counselors Support System. It uses Gradio to provide a user interface and integrates OpenAI's GPT-3.5 model to assist counselors in formulating enhanced replies ("Reply+"). The script includes a privacy filtering function that uses regular expressions to mask personally identifiable information in text. Overall, this script embodies the system's iterative approach to enhancing counseling communications.


## Dependencies

- Python >= 3.8
- Gradio
- LangChain
- Chromadb

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Acknowledgements

This project makes use of the following datasets and models:
- GPT-3.5
- Chinese public dataset COLD: https://github.com/thu-coai/COLDataset
- OpenAI's embedding extraction model
