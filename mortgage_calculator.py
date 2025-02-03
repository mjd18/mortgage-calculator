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

        # Display metrics in columns
        col1, col2, col3 = st.columns(3)
        col1.metric("Current Monthly Payment", f"${current_repayment}")
        col2.metric("New Monthly Payment", f"${new_repayment}")
        col3.metric("Monthly Savings", f"${savings_per_month:.2f}")
        st.markdown(f"### Annual Savings: **${savings_per_year:.2f}**")
        
        # --- RBA One-Liners ---
        rba_jokes = [
            "The RBA says they don’t predict the future—just strongly suggest how bad it’s going to be.",
            "My bank balance and the RBA have one thing in common—both are consistently disappointing.",
            "The RBA raised interest rates again—at this point, I think they just want to be invited to more barbecues for a 'friendly chat.'",
            "Every month, the RBA meets to decide how much extra I’ll be paying for my own house. Generous of them!",
            "The RBA keeps saying 'inflation is coming down.' Where? I think it’s lost like my socks in the dryer.",
            "The RBA says they’re 'monitoring the situation closely.' You know who else says that? My boss when he doesn't want to give me a pay rise.",
            "RBA: 'We’re independent of the government.' Also the RBA: Changes rates based on what the government says.",
            "Inflation’s so bad even Monopoly money is outperforming the Aussie dollar.",
            "I checked my mortgage balance and now I’m considering taking financial advice from a vending machine.",
            "RBA meetings are like horror movies. You know something bad’s coming, but you still watch anyway.",
            "If the RBA was a person, they’d be that mate who tells you they’re 'just coming for one drink' and then stays all night ruining your plans.",
            "The RBA says wage growth is too high. I’d love to meet someone whose wages are growing—sounds like an endangered species!",
            "The RBA’s solution to everything: 'Have you considered being richer?'",
            "Interest rates are like my in-laws—always popping up unannounced and costing me money.",
            "The RBA is like a DJ at a wedding—constantly adjusting the tempo, and no one’s ever happy.",
            "The RBA says inflation is 'stubbornly high.' So is my blood pressure when I read their updates.",
            "If the RBA was a Tinder date, they’d promise a good time and then leave you with a massive bill.",
            "My bank app should just have a 'cry' button after every RBA announcement.",
            "The RBA’s idea of a balanced economy is like my diet—completely out of whack.",
            "'We’re pausing rate hikes this month.' Ah yes, the RBA equivalent of saying 'We’ll see.'",
            "If the RBA worked in customer service, their default response would be: 'Unfortunately, that’s just our policy.'",
            "The RBA says higher rates will slow spending. Mate, my spending’s already so slow it’s in reverse.",
            "They say home ownership is the great Australian dream. With the RBA around, that dream comes with a lifetime of nightmares.",
            "The RBA’s reports are like IKEA instructions—confusing, full of missing pieces, and guaranteed to make you stressed.",
            "The RBA keeps talking about 'economic resilience.' Mate, I’m so resilient I’ve been using my loyalty card points to buy groceries.",
            "RBA: 'Rising interest rates will help the economy.' Also RBA: Destroys everyone’s savings, spending, and hope.",
            "The RBA raising rates again is like your boss announcing unpaid overtime—unexpected but not surprising.",
            "I’d like to thank the RBA for my new financial diet—eating nothing but anxiety.",
            "The RBA keeps using 'temporary' to describe inflation. Funny, my mortgage stress feels pretty permanent.",
            "The RBA says renters are being squeezed. Yeah, by their landlord, their real estate agent, and now the RBA too!",
            "The RBA’s got a new interest rate hike planned. And a new excuse planned.",
            "The RBA says 'we’re not aiming to crash the economy.' But they’re definitely swerving all over the road!",
            "The RBA should start a YouTube channel: 'How to make everyone poorer, explained in 60 seconds.'",
            "They say the RBA is independent. Independent of what? Logic? Compassion?",
            "If my mortgage repayments go up any more, I’ll be paying in tears instead of dollars.",
            "I asked my bank for advice on affording my mortgage. They just sent me a link to the lottery.",
            "The RBA says they’re slowing down spending. Mission accomplished—I just canceled my Netflix.",
            "The RBA says inflation is still high. So’s my stress level.",
            "'The RBA has decided to hold rates this month.' Yeah, but for how long? Longer than my last relationship? Doubt it.",
            "If the RBA was a car, it would be stuck in reverse—always pulling us back."
        ]
        st.markdown("#### RBA One-Liner")
        st.info(random.choice(rba_jokes))

# --- Expandable Disclaimer ---
with st.expander("Disclaimer"):
    st.write("""
    **Disclaimer:** This tool is for **illustrative purposes only** and does not constitute financial advice. 
    The calculations are based on general assumptions, including fixed monthly repayments. 
    Actual loan terms, interest rates, and savings may vary depending on your lender and financial situation. 
    Please consult a professional for personalized financial advice.
    """)
