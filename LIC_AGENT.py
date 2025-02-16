import streamlit as st
import pandas as pd
import datetime

# Database for storing agent and customer details
agent_data = {}
customer_data = {}

# Function to display profile information
def display_profile():
    st.header("Agent Profile")
    name = st.text_input("Enter your Name")
    email = st.text_input("Enter your Email")
    phone = st.text_input("Enter your Phone Number")
    achievements = st.text_area("Enter Your Achievements")
    profile_pic = st.file_uploader("Upload Profile Picture", type=["png", "jpg", "jpeg"])
    
    if st.button("Save Profile"):
        agent_data[name] = {"email": email, "phone": phone, "achievements": achievements, "profile_pic": profile_pic}
        st.success("Profile saved successfully!")
        st.write(f"### {name}")
        st.image(profile_pic, width=150)
        st.write(f"**Email:** {email}")
        st.write(f"**Phone:** {phone}")
        st.write(f"**Achievements:** {achievements}")

# Function for customer data management
def manage_customers():
    st.header("Customer Management")
    customer_name = st.text_input("Customer Name")
    policy_number = st.text_input("Policy Number")
    policy_amount = st.number_input("Policy Amount", value=10000, step=1000)
    policy_due_date = st.date_input("Policy Due Date", datetime.date.today())
    event_type = st.selectbox("Select Event Type", ["Birthday", "Wedding Anniversary", "Payment Reminder"])
    
    if st.button("Save Customer Data"):
        customer_data[customer_name] = {"policy_number": policy_number, "amount": policy_amount, "due_date": policy_due_date, "event": event_type}
        st.success("Customer Data Saved Successfully!")
        
    st.subheader("Send Notifications")
    for customer, details in customer_data.items():
        if st.button(f"Send {details['event']} Message to {customer}"):
            st.success(f"{details['event']} message sent to {customer}!")

# Function for insurance-related calculations
def insurance_calculator():
    st.header("Insurance Calculator")
    amount = st.number_input("Enter Policy Amount", value=10000, step=1000)
    years = st.number_input("Enter Policy Duration (Years)", value=10, step=1)
    rate = st.number_input("Enter Interest Rate (%)", value=6.0, step=0.1)
    
    if st.button("Calculate Maturity Amount"):
        maturity_amount = amount * ((1 + (rate / 100)) ** years)
        st.success(f"Maturity Amount: {maturity_amount:.2f}")

# Main function
def main():
    st.set_page_config(page_title="LIC Agent Portal", layout="wide")
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
