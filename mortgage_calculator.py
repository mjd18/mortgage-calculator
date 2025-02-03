import streamlit as st
import random
import math

# --- Calculation Functions ---
def calculate_interest_rate(loan_amount, loan_term_years, monthly_repayment):
    total_payments = loan_term_years * 12
    tolerance = 0.001
    low, high = 0.1, 12.0
    iteration = 0
    max_iter = 500

    if monthly_repayment < (loan_amount / total_payments):
        return None  # Repayment is too low to cover the loan

    while iteration < max_iter:
        iteration += 1
        mid = (low + high) / 2
        monthly_rate = (mid / 100) / 12
        estimated_payment = (loan_amount * monthly_rate) / (1 - (1 + monthly_rate) ** -total_payments)
        diff = abs(estimated_payment - monthly_repayment)

        if diff < tolerance:
            return round(mid, 2)
        elif estimated_payment > monthly_repayment:
            high = mid
        else:
            low = mid

    return None

def mortgage_calculator(loan_amount, loan_term_years, interest_rate):
    if interest_rate == 0:
        return round(loan_amount / (loan_term_years * 12), 2)
    monthly_rate = (interest_rate / 100) / 12
    total_payments = loan_term_years * 12
    monthly_payment = (loan_amount * monthly_rate) / (1 - (1 + monthly_rate) ** -total_payments)
    return round(monthly_payment, 2)

# --- Page Configuration and Title ---
st.set_page_config(page_title="Count Your Chickens Before They Hatch", page_icon="🐔", layout="wide")
st.title("🐔 Count Your Chickens Before They Hatch 🥚")
st.write("Discover how a drop in interest rates could hatch extra savings!")

# --- Main Page Form for Inputs ---
with st.form(key="loan_form"):
    st.header("Enter Your Loan Details")
    
    input_type = st.radio("Select Input Method:", ("Monthly Repayment", "Interest Rate"), index=0)
    
    loan_amount = st.number_input(
        "Loan Amount ($)",
        value=100000.0,
        min_value=1000.0,
        step=1000.0,
        help="Enter the total loan amount."
    )
    loan_term_years = st.number_input(
        "Years Remaining",
        value=20,
        min_value=1,
        max_value=40,
        step=1,
        help="Enter the number of years left on your loan."
    )
    
    if input_type == "Monthly Repayment":
        monthly_repayment = st.number_input(
            "Monthly Repayment ($)",
            min_value=100.0,
            step=10.0,
            help="Enter your current monthly repayment."
        )
    else:
        interest_rate = st.number_input(
            "Interest Rate (%)",
            value=3.5,
            min_value=0.01,
            max_value=20.0,
            step=0.01,
            help="Enter your current interest rate."
        )
    
    # Using a number input for the potential rate cut
    rate_cut = st.number_input(
        "Potential Interest Rate Cut (%)",
        value=0.0,
        min_value=0.0,
        max_value=10.0,
        step=0.01,
        help="Enter the potential drop in interest rate (%)"
    )
    
    submitted = st.form_submit_button("Calculate Savings")

# --- Main Calculation & Output ---
if submitted:
    # If the user provided monthly repayment, calculate the interest rate first
    if input_type == "Monthly Repayment":
        interest_rate = calculate_interest_rate(loan_amount, loan_term_years, monthly_repayment)
        if interest_rate is None:
            st.error("⚠️ The monthly repayment is too low for this loan. Please adjust your inputs.")
        else:
            st.success(f"Estimated Interest Rate: {interest_rate}%")
    
    if interest_rate:
        new_interest_rate = max(0.01, interest_rate - rate_cut)
        current_repayment = mortgage_calculator(loan_amount, loan_term_years, interest_rate)
        new_repayment = mortgage_calculator(loan_amount, loan_term_years, new_interest_rate)
        savings_per_month = current_repayment - new_repayment
        savings_per_year = savings_per_month * 12

        messages = [
            "Looks like you might hatch some extra savings! 🐣",
            "More savings = more chicken feed for you! 🏡",
            "Don't count your chickens yet, but this looks good! 🥚",
            "Interest rates dropping? That's eggs-cellent news! 🍳",
        ]
        st.success(random.choice(messages))

        # Display metrics in columns
        col1, col2, col3 = st.columns(3)
        col1.metric("Current Monthly Payment", f"${current_repayment}")
        col2.metric("New Monthly Payment", f"${new_repayment}")
        col3.metric("Monthly Savings", f"${savings_per_month:.2f}")
        st.markdown(f"### Annual Savings: **${savings_per_year:.2f}**")

# --- Expandable Disclaimer ---
with st.expander("Disclaimer"):
    st.write("""
    **Disclaimer:** This tool is for **illustrative purposes only** and does not constitute financial advice. 
    The calculations are based on general assumptions, including fixed monthly repayments. 
    Actual loan terms, interest rates, and savings may vary depending on your lender and financial situation. 
    Please consult a professional for personalized financial advice.
    """)

