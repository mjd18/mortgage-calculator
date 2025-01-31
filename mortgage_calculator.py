import streamlit as st
import random

def mortgage_calculator(loan_amount, loan_term_years, interest_rate):
    """
    Calculate the monthly mortgage repayment with daily compounding interest.
    """
    daily_rate = (interest_rate / 100) / 365  # Convert annual interest rate to daily rate
    monthly_rate = ((1 + daily_rate) ** 30) - 1  # Approximate monthly rate using daily compounding
    total_payments = loan_term_years * 12  # Total number of monthly payments
    
    if monthly_rate > 0:
        monthly_payment = (loan_amount * monthly_rate) / (1 - (1 + monthly_rate) ** -total_payments)
    else:
        monthly_payment = loan_amount / total_payments  # No interest case
    
    return round(monthly_payment, 2)

# Streamlit UI
st.set_page_config(page_title="Count Your Chickens Before They Hatch", page_icon="🐔", layout="centered")
st.title("🐔 Count Your Chickens Before They Hatch 🥚")
st.write("### A fun way to see how much you could save if interest rates drop!")

# User input for loan details
loan_amount = st.number_input("Enter Loan Amount ($)", min_value=1000.0, step=1000.0, format="%.2f")

# Format loan amount with commas for display
formatted_loan_amount = f"{loan_amount:,.2f}"
st.write(f"You entered: **${formatted_loan_amount}**")
loan_term_years = st.number_input("Enter Years Remaining on Loan", min_value=1, max_value=40, step=1)
interest_rate = st.number_input("Enter Current Interest Rate (%)", min_value=0.01, max_value=20.0, step=0.01, format="%.2f")
rate_cut = st.slider("Potential Interest Rate Cut (%)", min_value=0.0, max_value=10.0, step=0.01, format="%.2f")

if loan_amount and loan_term_years and interest_rate:
    # Calculate current repayment
    current_repayment = mortgage_calculator(loan_amount, loan_term_years, interest_rate)
    
    # Calculate potential repayment with rate cut
    new_interest_rate = max(0.01, interest_rate - rate_cut)  # Ensure it doesn't go below 0.01%
    new_repayment = mortgage_calculator(loan_amount, loan_term_years, new_interest_rate)
    
    # Savings per month and year
    savings_per_month = current_repayment - new_repayment
    savings_per_year = savings_per_month * 12
    
    # Fun chicken-related messages
    messages = [
        "Looks like you might hatch some extra savings! 🐣",
        "More savings = more chicken feed for you! 🏡",
        "Don't count your chickens yet, but this looks good! 🥚",
        "Interest rates dropping? That's eggs-cellent news! 🍳",
    ]
    st.write(f"## 🐥 {random.choice(messages)}")
    
    # Display results
    st.write(f"### Your Current Monthly Repayment: **${current_repayment}**")
    st.write(f"### If Rates Drop by {rate_cut}%, Your New Repayment: **${new_repayment}**")
    st.write(f"### You Could Save: **${savings_per_month:.2f} per month / ${savings_per_year:.2f} per year!**")
    
# Disclaimer
st.markdown("""
**Disclaimer:** This tool is for **illustrative purposes only** and does not constitute financial advice. 
The calculations are based on general assumptions, including daily interest compounding and fixed monthly repayments. 
Actual loan terms, interest rates, and savings may vary depending on your lender and financial situation. 
Please consult a professional for personalised financial advice.
""", unsafe_allow_html=True)
