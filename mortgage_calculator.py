with st.sidebar.form(key="loan_form"):
    st.header("Loan Details")
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
    
    # Replacing the slider with a number input for potential rate cut:
    rate_cut = st.number_input(
        "Potential Interest Rate Cut (%)",
        value=0.0,
        min_value=0.0,
        max_value=10.0,
        step=0.01,
        help="Enter the potential drop in interest rate (%)"
    )
    
    submitted = st.form_submit_button("Calculate Savings")
