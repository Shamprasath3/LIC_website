import streamlit as st
import pandas as pd
import datetime

# --- Configuration ---
st.set_page_config(page_title="LIC Agent Portal", layout="wide")
st.markdown(
    """
    <style>
    body {
        background-color: #f5f5f5;
        font-family: 'Arial', sans-serif;
    }
    .header {
        text-align: center;
        color: #0077B5;
    }
    .card {
        background-color: white;
        border-radius: 8px;
        padding: 20px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Initialize Session State ---
if 'agent_data' not in st.session_state:
    st.session_state['agent_data'] = {}
if 'customer_data' not in st.session_state:
    st.session_state['customer_data'] = {}

# --- Helper Functions ---
def display_customer_data(customer_data):
    """Displays customer data in a DataFrame."""
    if customer_data:
        df = pd.DataFrame.from_dict(customer_data, orient='index')
        st.dataframe(df)
    else:
        st.info("No customer data available.")

# --- Functions ---
def display_profile():
    st.header("Agent Profile")
    
    with st.form("profile_form"):
        name = st.text_input("Enter your Name", key="agent_name")
        email = st.text_input("Enter your Email", key="agent_email")
        phone = st.text_input("Enter your Phone Number", key="agent_phone")
        achievements = st.text_area("Enter Your Achievements", key="agent_achievements")
        profile_pic = st.file_uploader("Upload Profile Picture", type=["png", "jpg", "jpeg"], key="agent_pic")

        submit_button = st.form_submit_button(label="Save Profile")

        if submit_button:
            st.session_state['agent_data'][name] = {
                "email": email,
                "phone": phone,
                "achievements": achievements,
                "profile_pic": profile_pic
            }
            st.success("Profile saved successfully!")

            # Display saved profile immediately
            st.write("### Your Profile")
            if profile_pic is not None:
                st.image(profile_pic, width=150)
            st.write(f"**Name:** {name}")
            st.write(f"**Email:** {email}")
            st.write(f"**Phone:** {phone}")
            st.write(f"**Achievements:** {achievements}")

def manage_customers():
    st.header("Customer Management")

    with st.form("customer_form"):
        customer_name = st.text_input("Customer Name", key="customer_name")
        policy_number = st.text_input("Policy Number", key="policy_number")
        policy_amount = st.number_input("Policy Amount", value=10000, step=1000, key="policy_amount")
        policy_due_date = st.date_input("Policy Due Date", datetime.date.today(), key="policy_due_date")
        event_type = st.selectbox("Select Event Type", ["Birthday", "Wedding Anniversary", "Payment Reminder"], key="event_type")

        save_button = st.form_submit_button(label="Save Customer Data")

        if save_button:
            st.session_state['customer_data'][customer_name] = {
                "policy_number": policy_number,
                "amount": policy_amount,
                "due_date": policy_due_date,
                "event": event_type
            }
            st.success("Customer Data Saved Successfully!")

    display_customer_data(st.session_state['customer_data'])

def insurance_calculator():
    st.header("Insurance Calculator")
    
    with st.form("calculator_form"):
        amount = st.number_input("Enter Policy Amount", value=10000, step=1000)
        years = st.number_input("Enter Policy Duration (Years)", value=10, step=1)
        rate = st.number_input("Enter Interest Rate (%)", value=6.0, step=0.1)

        calculate_button = st.form_submit_button(label="Calculate Maturity Amount")

        if calculate_button:
            maturity_amount = amount * ((1 + (rate / 100)) ** years)
            st.success(f"Maturity Amount: {maturity_amount:.2f}")

# --- Main Function ---
def main():
    # Header
    st.markdown("<h1 class='header'>📜 LIC Agent Dashboard</h1>", unsafe_allow_html=True)

    menu = ["Profile", "Customer Management", "Insurance Calculator"]
    choice = st.sidebar.selectbox("Select an Option", menu)

    if choice == "Profile":
        display_profile()
    elif choice == "Customer Management":
        manage_customers()
    elif choice == "Insurance Calculator":
        insurance_calculator()

if __name__ == "__main__":
    main()
