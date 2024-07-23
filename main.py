import streamlit as st


# Function to determine loan eligibility
def determine_eligibility(credit_score, annual_income, loan_amount, loan_term):
    # Simple eligibility criteria
    if credit_score < 600:
        return "Ineligible due to low credit score"
    elif annual_income < 25000:
        return "Ineligible due to low annual income"
    elif loan_amount > annual_income * 0.5:
        return "Ineligible due to high loan amount relative to income"
    elif loan_term > 30:
        return "Ineligible due to excessively long loan term"
    else:
        return "Eligible for the loan"


# Streamlit application
def main():
    st.title("Loan Eligibility Checker")

    # Collecting user input
    st.header("Please enter your details:")
    credit_score = st.number_input("Credit Score", min_value=0, max_value=850, step=1)
    annual_income = st.number_input("Annual Income ($)", min_value=0, step=1000)
    loan_amount = st.number_input("Loan Amount ($)", min_value=0, step=1000)
    loan_term = st.number_input("Loan Term (years)", min_value=0, max_value=50, step=1)

    # Determine eligibility when the button is clicked
    if st.button("Check Eligibility"):
        eligibility_status = determine_eligibility(credit_score, annual_income, loan_amount, loan_term)
        st.subheader("Loan Eligibility Status:")
        st.write(eligibility_status)


if __name__ == "__main__":
    main()
