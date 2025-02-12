import streamlit as st
import google.generativeai as genai
import os

# Configure GenAI
GENAI_API_KEY = "AIzaSyBPezIOqsH6A2ZK3mh6KK1pfHwh3qu8pb4"  # Replace with your actual API key
genai.configure(api_key=GENAI_API_KEY)

# Initialize the model
model = genai.GenerativeModel('gemini-pro')

# ---------------------------------------------------
# Sidebar: Select Sales Scenario
# ---------------------------------------------------
st.sidebar.title("Select Sales Scenario")
scenario = st.sidebar.selectbox(
    "Choose a scenario:",
    ["Personal Loan", "Education Loan", "Business Loan", "Car Loan"]
)
st.sidebar.write(f"**Selected Scenario:** {scenario}")

# ---------------------------------------------------
# Main Chat Interface
# ---------------------------------------------------
st.title("🤖 Sales Practice Chatbot")
st.write("Practice your sales skills! You are the salesperson; the bot will act as the customer.")

# Initialize conversation history
if "conversation" not in st.session_state:
    st.session_state.conversation = []
if "evaluated" not in st.session_state:
    st.session_state.evaluated = False


# ---------------------------------------------------
# Function to Generate Customer Response
# ---------------------------------------------------
def generate_customer_response(sales_message: str, scenario: str) -> str:
    prompt = f"""
    You are a potential customer interested in a {scenario}. 
    The salesperson just said: '{sales_message}'. 
    Respond naturally with realistic objections, questions, or concerns that a real customer might have.
    Keep responses concise (1-2 sentences max).
    """
    response = model.generate_content(prompt)
    return response.text.strip()


# ---------------------------------------------------
# Function to Evaluate Conversation
# ---------------------------------------------------
def evaluate_conversation(conversation: list) -> str:
    transcript = "\n".join([f"{msg['role']}: {msg['message']}" for msg in conversation])

    evaluation_prompt = f"""
    Analyze this sales conversation for a {scenario} and provide detailed evaluation:
    {transcript}

    Evaluate on these criteria (1-10 scale):
    1. Communication Clarity
    2. Objection Handling
    3. Persuasion Techniques
    4. Professionalism
    5. Overall Effectiveness

    Provide brief feedback for each category and suggest improvements.
    """

    evaluation = model.generate_content(evaluation_prompt)
    return evaluation.text.strip()


# ---------------------------------------------------
# Display Conversation
# ---------------------------------------------------
st.subheader("Practice Session")
for msg in st.session_state.conversation:
    if msg["role"] == "salesperson":
        st.markdown(f"**You (Sales):** {msg['message']}")
    else:
        st.markdown(f"**Customer:** {msg['message']}")

# ---------------------------------------------------
# User Input
# ---------------------------------------------------
user_input = st.chat_input("Your message as salesperson...")

if user_input and not st.session_state.evaluated:
    # Add user message to conversation
    st.session_state.conversation.append({"role": "salesperson", "message": user_input})

    # Generate customer response
    customer_response = generate_customer_response(user_input, scenario)
    st.session_state.conversation.append({"role": "customer", "message": customer_response})

    # Rerun to update conversation
    st.rerun()

# ---------------------------------------------------
# Evaluation Section
# ---------------------------------------------------
if st.button("End Session & Get Evaluation") and not st.session_state.evaluated:
    st.session_state.evaluated = True
    evaluation = evaluate_conversation(st.session_state.conversation)

    st.subheader("📈 Performance Evaluation")
    st.markdown("---")
    st.markdown(evaluation)
    st.markdown("---")

    # Option to start new session
    if st.button("Start New Session"):
        st.session_state.conversation = []
        st.session_state.evaluated = False
        st.rerun()