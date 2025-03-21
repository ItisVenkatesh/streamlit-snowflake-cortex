import streamlit as st
import snowflake.connector
import json
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(message)s')

# Streamlit UI
st.title("💬 Snowflake Cortex Chatbot")
logging.debug("test")
logging.info("test")
# User Inputs for Snowflake Connection
snowflake_account = st.text_input("Snowflake Account (e.g., xyz123 in xyz123.snowflakecomputing.com)", "")
user = st.text_input("Username", "")
password = st.text_input("Password", type="password")
database = st.text_input("Database", "YOUR_DB")
schema = st.text_input("Schema", "PUBLIC")
warehouse = st.text_input("Warehouse", "COMPUTE_WH")
# List of AI models
models = ['snowflake-arctic', 'llama3.1-70b', 'reka-flash']

# Create a dropdown for users to select an AI model
selected_model = st.selectbox("Choose an AI Model", models)
# Function to connect to Snowflake and query Cortex
def query_snowflake(question):
    try:
        conn = snowflake.connector.connect(
            user=user,
            password=password,
            account=snowflake_account,
            warehouse=warehouse,
            database=database,
            schema=schema
        )
        logging.debug("before conn")
        cur = conn.cursor()
        # Use Cortex AI to generate answers
        cortex_query = f"""
        SELECT snowflake.cortex.complete(
            '{selected_model}',
            '{question}'
        )
        """
        
        cur.execute(cortex_query)
        result = cur.fetchone()
        
        return result[0] if result else "No response from Cortex."

    except Exception as e:
        return f"❌ Error: {str(e)}"

# Chatbot Interaction
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if user and password and snowflake_account:
    question = st.chat_input("Ask me anything...")
    if question:
        st.session_state.messages.append({"role": "user", "content": question})

        with st.chat_message("user"):
            st.write(question)

        # Get response from Snowflake Cortex
        response = query_snowflake(question)
        st.session_state.messages.append({"role": "assistant", "content": response})

        with st.chat_message("assistant"):
            st.write(response)

# Footer
st.markdown("---")
st.markdown("Made with ❤️ by Venkatesh.")