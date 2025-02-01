import streamlit as st
import random
import math
import requests
from streamlit_lottie import st_lottie

# Fetch real-time interest rate data (dummy example, replace with real API)
def get_real_time_interest_rate():
    try:
        response = requests.get("https://api.example.com/interest-rates")
        data = response.json()
        return data.get("current_rate", 6.0)
    except:
        return 6.0  # Default fallback

def calculate_interest_rate(loan_amount, loan_term_years, monthly_repayment):
    total_payments = loan_term_years * 12
    tolerance = 0.001
    low, high = 0.1, 12.0
    iteration = 0
    max_iter = 500

    if monthly_repayment < (loan_amount / total_payments):
        return None

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

st.set_page_config(page_title="Count Your Chickens Before They Hatch", page_icon="🐔", layout="wide")
st.markdown("""<style>body { background-color: #fef9e7; color: #333; font-family: Arial, sans-serif; }</style>""", unsafe_allow_html=True)

st.title("🐔 Count Your Chickens Before They Hatch 🥚")
st.write("### A fun way to see how much you could save if interest rates drop!")

# Fetch real-time interest rate
default_interest_rate = get_real_time_interest_rate()

col1, col2 = st.columns(2)

with col1:
    loan_amount = st.number_input("Enter Loan Amount ($)", min_value=1000.0, step=1000.0)
    loan_term_years = st.number_input("Enter Years Remaining on Loan", min_value=1, max_value=40, step=1)
    monthly_repayment = st.number_input("Enter Your Current Monthly Repayment ($)", min_value=100.0, step=10.0)

if loan_amount and loan_term_years and monthly_repayment:
    interest_rate = calculate_interest_rate(loan_amount, loan_term_years, monthly_repayment)
    if interest_rate is None:
        st.error("⚠️ Your monthly repayment seems too low for this loan. Please check your inputs.")
    else:
        st.write(f"### Estimated Current Interest Rate: **{interest_rate}%**")

if interest_rate:
    rate_cut = st.slider("Potential Interest Rate Cut (%)", min_value=0.0, max_value=10.0, step=0.01, format="%.2f")
    new_interest_rate = max(0.01, interest_rate - rate_cut)
    current_repayment = mortgage_calculator(loan_amount, loan_term_years, interest_rate)
    new_repayment = mortgage_calculator(loan_amount, loan_term_years, new_interest_rate)
    savings_per_month = current_repayment - new_repayment
    savings_per_year = savings_per_month * 12
    
    st.success(f"💰 You Could Save: **${savings_per_month:.2f} per month / ${savings_per_year:.2f} per year!**")

    messages = [
        "Looks like you might hatch some extra savings! 🐣",
        "More savings = more chicken feed for you! 🏡",
        "Don't count your chickens yet, but this looks good! 🥚",
        "Interest rates dropping? That's eggs-cellent news! 🍳",
    ]
    st.markdown(f"<p style='font-size:22px; font-weight:bold; text-align:center;'>🐥 {random.choice(messages)}</p>", unsafe_allow_html=True)

# Disclaimer
st.markdown("""
    **Disclaimer:** This tool is for **illustrative purposes only** and does not constitute financial advice. 
    The calculations are based on general assumptions, including daily interest compounding and fixed monthly repayments. 
    Actual loan terms, interest rates, and savings may vary depending on your lender and financial situation. 
    Please consult a professional for personalised financial advice.
    """, unsafe_allow_html=True)
