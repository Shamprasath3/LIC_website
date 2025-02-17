import streamlit as st
import pandas as pd
import datetime

# --- Configuration ---
st.set_page_config(page_title="LIC Agent Portal", layout="wide")
st.markdown(
    """
    <style>
    [data-testid="stAppViewContainer"]{
        background-image: url("https://images.unsplash.com/photo-1519389950473-47a0b9c578dd?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D");
        background-size: cover;
        background-position: top left;
        background-repeat: no-repeat;
    }

    [data-testid="stHeader"]{
    background-color: rgba(0,0,0,0);
    }

    [data-testid="stToolbar"]{
        right: 2rem;
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
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Enter your Name", key="agent_name")
        email = st.text_input("Enter your Email", key="agent_email")
        phone = st.text_input("Enter your Phone Number", key="agent_phone")
    with col2:
        achievements = st.text_area("Enter Your Achievements", key="agent_achievements")
        profile_pic = st.file_uploader("Upload Profile Picture", type=["png", "jpg", "jpeg"], key="agent_pic")

    if st.button("Save Profile"):
        st.session_state['agent_data'][name] = {"email": email, "phone": phone, "achievements": achievements, "profile_pic": profile_pic}
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

    col1, col2 = st.columns(2)
    with col1:
        customer_name = st.text_input("Customer Name", key="customer_name")
        policy_number = st.text_input("Policy Number", key="policy_number")
        policy_amount = st.number_input("Policy Amount", value=10000, step=1000, key="policy_amount")
    with col2:
        policy_due_date = st.date_input("Policy Due Date", datetime.date.today(), key="policy_due_date")
        event_type = st.selectbox("Select Event Type", ["Birthday", "Wedding Anniversary", "Payment Reminder"], key="event_type")

    if st.button("Save Customer Data"):
        st.session_state['customer_data'][customer_name] = {"policy_number": policy_number, "amount": policy_amount, "due_date": policy_due_date, "event": event_type}
        st.success("Customer Data Saved Successfully!")
        
    st.subheader("Existing Customer Data")
    display_customer_data(st.session_state['customer_data'])

    st.subheader("Send Notifications")
    for customer, details in st.session_state['customer_data'].items():
        if st.button(f"Send {details['event']} Message to {customer}"):
            st.success(f"{details['event']} message sent to {customer}!")


def insurance_calculator():
    st.header("Insurance Calculator")
    col1, col2, col3 = st.columns(3)
    with col1:
        amount = st.number_input("Enter Policy Amount", value=10000, step=1000)
    with col2:
        years = st.number_input("Enter Policy Duration (Years)", value=10, step=1)
    with col3:
        rate = st.number_input("Enter Interest Rate (%)", value=6.0, step=0.1)

    if st.button("Calculate Maturity Amount"):
        maturity_amount = amount * ((1 + (rate / 100)) ** years)
        st.success(f"Maturity Amount: {maturity_amount:.2f}")

        # Optional: Display in a chart
        import matplotlib.pyplot as plt
        import numpy as np

        years_range = np.arange(1, years + 1)
        maturity_values = amount * ((1 + (rate / 100)) ** years_range)

        fig, ax = plt.subplots()
        ax.plot(years_range, maturity_values)
        ax.set_xlabel("Years")
        ax.set_ylabel("Maturity Amount")
        ax.set_title("Maturity Amount Over Time")
        st.pyplot(fig)

# --- Main Function ---
def main():
    st.title("📜 LIC Agent Dashboard")
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
