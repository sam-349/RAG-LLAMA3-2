import streamlit as st

# Set the page configuration
st.set_page_config(page_title="Chatbot UI", page_icon="💬")

# Sidebar:
st.sidebar.title("Scenario Selection")
scenario = st.sidebar.selectbox(
    "Choose a scenario:",
    ["Personal Loan", "Education", "Healthcare", "General"]
)

st.sidebar.write(f"**Selected scenario:** {scenario}")


# Chat Interface
st.title("Chatbot Interface")
st.write("This is a demo chatbot UI. No AI model is integrated.")

# Initialize session state for messages if not already set
if "messages" not in st.session_state:
    st.session_state["messages"] = []  # List of dicts: {"role": "user" or "bot", "content": str}

# Display chat history
for msg in st.session_state["messages"]:
    if msg["role"] == "user":
        st.markdown(f"**User:** {msg['content']}")
    else:
        st.markdown(f"**Bot:** {msg['content']}")


user_input = st.text_input("Your message:", key="user_input")

# Send Button
if st.button("Send") and user_input:

    st.session_state["messages"].append({"role": "user", "content": user_input})

    dummy_response = f"This is a dummy response for the scenario '{scenario}'."
    st.session_state["messages"].append({"role": "bot", "content": dummy_response})

    # Clear the input
    st.experimental_rerun()
