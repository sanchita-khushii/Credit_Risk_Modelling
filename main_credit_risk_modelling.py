import streamlit as st
from credit_risk_modelling_helper import predict

# --- Page Config ---
st.set_page_config(page_title="Credit Risk Modelling", layout="wide")

# --- Custom CSS ---
st.markdown("""
    <style>
        /* Whole App Background */
        .stApp {
            background: linear-gradient(135deg, #fdf2f8, #e0f2fe, #fef9c3, #dcfce7);
            background-attachment: fixed;
        }

        /* Title */
        h1 {
            background: linear-gradient(90deg, #7c3aed, #ec4899, #06b6d4, #16a34a);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-family: 'Trebuchet MS', sans-serif;
            font-weight: 900;
            text-align: center;
            margin-bottom: 18px;
            font-size: 34px;
        }

        /* Section Containers with brighter gradient */
        .section {
            background: linear-gradient(135deg, #fef9c3cc, #f3e8ffcc, #bae6fdcc);
            padding: 10px 14px;
            border-radius: 12px;     
            box-shadow: 0 3px 8px rgba(0,0,0,0.12);
            margin-bottom: 14px;
            display: inline-block;
        }
        .section h3 {
            font-size: 16px;
            margin: 0;
            line-height: 1.3;
            color: #374151;
        }

        /* Unified Input Labels (Number + Selectbox) */
        div[data-testid="stNumberInput"] label,
        div[data-testid="stSelectbox"] label {
            background: linear-gradient(135deg, #f0f9ff, #e0f2fe); /* soft sky blue */
            color: #1f2937 !important; /* dark gray text */
            padding: 4px 8px;
            border-radius: 8px;
            font-weight: 600;
            font-size: 14px;
            display: inline-block;
        }

        /* Input Widgets background */
        .stNumberInput, .stSelectbox {
            background: #ffffffdd !important;
            padding: 6px;
            border-radius: 10px;
        }
        .stNumberInput input, .stSelectbox div {
            background: linear-gradient(135deg, #f0f9ff, #e0f2fe);
            border-radius: 6px;
            padding: 4px 8px;
            font-size: 14px;
        }

        /* Loan to Income Ratio special card */
        .ratio-box {
            background: linear-gradient(135deg, #22d3ee, #0ea5e9);
            padding: 10px;
            border-radius: 12px;
            text-align: center;
            font-weight: 600;
            font-size: 14px;
            color: white;
            box-shadow: 0 2px 8px rgba(0,0,0,0.15);
        }

        /* Result Boxes */
        .result-box {
            padding: 14px;
            border-radius: 14px;
            text-align: center;
            font-weight: 700;
            font-size: 16px;
            color: white;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        }
        .prob { background: linear-gradient(135deg, #f43f5e, #be123c); }
        .score { background: linear-gradient(135deg, #10b981, #065f46); }
        .rating { background: linear-gradient(135deg, #fbbf24, #f59e0b); color: #1f2937; }
    </style>
""", unsafe_allow_html=True)




# --- Title ---
st.markdown("<h1> Credit Risk Modelling</h1>", unsafe_allow_html=True)

# --- Applicant Information ---
st.markdown("<div class='section'><h3>👤 Applicant Information</h3>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1:
    age = st.number_input("Age", min_value=18, max_value=100, value=30, step=1)
with col2:
    income = st.number_input("Income", min_value=10000, max_value=10000000, value=500000, step=10000)
with col3:
    loan_amount = st.number_input("Loan Amount", min_value=5000, max_value=10000000, value=200000, step=10000)
st.markdown("</div>", unsafe_allow_html=True)

# --- Credit Profile ---
st.markdown("<div class='section'><h3>💳 Credit Profile</h3>", unsafe_allow_html=True)
col4, col5, col6 = st.columns(3)
with col4:
    loan_tenure = st.number_input("Loan Tenure (months)", min_value=1, max_value=360, value=36, step=1)
with col5:
    avg_dpd = st.number_input("Avg DPD", min_value=0, max_value=100, value=2, step=1)
with col6:
    loan_to_income_ratio = round(loan_amount / income, 2) if income > 0 else 0
    st.markdown(f"<div class='ratio-box'>Loan to Income Ratio<br>{loan_to_income_ratio}</div>", unsafe_allow_html=True)

col7, col8, col9 = st.columns(3)
with col7:
    open_loans = st.number_input("Open Loan Accounts", min_value=0, max_value=20, value=1, step=1)
with col8:
    delinquency_ratio = st.number_input("Delinquency Ratio (%)", min_value=0, max_value=100, value=10, step=1)
with col9:
    credit_utilization = st.number_input("Credit Utilization Ratio (%)", min_value=0, max_value=100, value=30, step=1)
st.markdown("</div>", unsafe_allow_html=True)

# --- Loan Details ---
st.markdown("<div class='section'><h3>🏦 Loan Details</h3>", unsafe_allow_html=True)
col10, col11, col12 = st.columns(3)
with col10:
    residence_type = st.selectbox("Residence Type", ["Owned", "Rented", "Mortgage"])
with col11:
    loan_purpose = st.selectbox("Loan Purpose", ["Auto", "Home", "Education", "Personal", "Business"])
with col12:
    loan_type = st.selectbox("Loan Type", ["Secured", "Unsecured"])
st.markdown("</div>", unsafe_allow_html=True)

# --- Results ---
st.markdown("---")
if st.button("🚀 Calculate Risk", use_container_width=True):
    probability, credit_score, rating = predict(
        age, income, loan_amount, loan_tenure, avg_dpd, open_loans,
        delinquency_ratio, credit_utilization, residence_type, loan_purpose, loan_type
    )

    colr1, colr2, colr3 = st.columns(3)
    with colr1:
        st.markdown(f"<div class='result-box prob'>❌ Probability of Default<br>{probability:.2f}</div>", unsafe_allow_html=True)
    with colr2:
        st.markdown(f"<div class='result-box score'>💳 Credit Score<br>{credit_score}</div>", unsafe_allow_html=True)
    with colr3:
        st.markdown(f"<div class='result-box rating'>⭐ Rating<br>{rating}</div>", unsafe_allow_html=True)






