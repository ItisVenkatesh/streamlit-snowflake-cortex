import streamlit as st
import json

# Simulate the mock response (this would be replaced with a real API call in production)
def simulate_cortex_response(query):
    # Simulating the mock response for a specific query
    mock_response = {
        "status": "success",
        "query": query,
        "answer": {
            "value": 25.7,
            "summary": "The average value of column_2 is 25.7 based on the provided dataset.",
            "metadata": {
                "column": "column_2",
                "table": "<YOUR_SNOWFLAKE_TABLE_NAME>",
                "record_count": 1200,
                "null_count": 15
            }
        },
        "insights": [
            {
                "insight_type": "outlier",
                "message": "There is an outlier value of 200.0 in column_2 that might skew the average.",
                "row_id": 205
            },
            {
                "insight_type": "distribution",
                "message": "The distribution of values in column_2 is skewed, with a mean of 25.7 and a median of 24.5."
            }
        ],
        "duration": 2.35,
        "credits_remaining": 450,
        "error": None
    }
    return mock_response

# Initialize Streamlit app
st.set_page_config(page_title="Snowflake Cortex Chatbot", page_icon="🤖")
st.title("Snowflake Cortex Chatbot")
st.markdown("### Ask data-related questions to Cortex, and get insights from Snowflake.")

# Add some styling
st.markdown("""
    <style>
        .user-msg {
            background-color: #DCF8C6;
            padding: 10px;
            border-radius: 10px;
            max-width: 80%;
            margin: 5px 0;
            font-size: 16px;
        }
        .cortex-msg {
            background-color: #E6E6E6;
            padding: 10px;
            border-radius: 10px;
            max-width: 80%;
            margin: 5px 0;
            font-size: 16px;
        }
        .chat-box {
            padding: 10px;
            max-height: 400px;
            overflow-y: scroll;
            border: 1px solid #ddd;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        .input-box {
            display: flex;
            flex-direction: row;
            justify-content: space-between;
            margin-top: 20px;
        }
        .input-box input {
            width: 80%;
            padding: 10px;
            font-size: 16px;
            border-radius: 5px;
            border: 1px solid #ddd;
        }
        .input-box button {
            padding: 10px 20px;
            font-size: 16px;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        .input-box button:hover {
            background-color: #45a049;
        }
    </style>
""", unsafe_allow_html=True)

# Create a session state to store the chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history in a scrollable box
with st.container():
    st.markdown('<div class="chat-box">', unsafe_allow_html=True)
    for message in st.session_state.messages:
        if message['role'] == 'User':
            st.markdown(f'<div class="user-msg">{message["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="cortex-msg">{message["content"]}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# User input for the chatbot
user_input = st.text_input("Ask a data-related question:")

# Submit button with a more interactive design
col1, col2 = st.columns([4, 1])
with col2:
    if st.button("Submit"):
        if user_input.strip():
            # Show user query in chat history
            st.session_state.messages.append({"role": "User", "content": user_input})

            # Get the simulated answer from Cortex
            response = simulate_cortex_response(user_input)

            # Display the answer from the mock response
            if response['status'] == 'success':
                answer = response['answer']['summary']
                insights = response['insights']
                answer_message = f"{answer}\n\nInsights:\n"
                for insight in insights:
                    answer_message += f"- {insight['message']}\n"

                st.session_state.messages.append({"role": "Cortex", "content": answer_message})

            else:
                st.session_state.messages.append({"role": "Cortex", "content": "Sorry, I couldn't find an answer to your question."})

            # Scroll to the bottom of the chat
            st.rerun()
        else:
            st.warning("Please enter a question.")

# Footer
st.markdown("---")
st.markdown("Made with ❤️ by Venkatesh.")