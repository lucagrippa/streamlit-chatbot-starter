# streamlit-chatbot-starter

A simple chatbot powered by OpenAI's language model. This chatbot is built using Streamlit, an easy-to-use Python web app framework for data science and machine learning applications.

## Prerequisites

- Python 3.x
- Install the required packages using the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

## Usage

Create a .env file and add your OpenAI API key in it:

```
OPENAI_API_KEY=your_openai_api_key
```

Run the main script using Streamlit:

```bash
streamlit run main.py
```

This will launch the chatbot web app, and you can start interacting with it.


## Functionality

- The chatbot uses the OpenAI GPT-3 language model to generate responses.
- It stores the conversation history in the session state using Streamlit's `session_state`.
- You can clear the conversation history by clicking the "Clear Conversation" button.


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
