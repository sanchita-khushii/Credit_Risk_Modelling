import joblib
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

model_path=r"C:\Users\PREDATOR\Downloads\artifacts.joblib"

#load the data and its components
model_data=joblib.load(model_path)
model=model_data["model"]
scaler=model_data["scaler"]
features=model_data["features"]
cols_to_scale=model_data["cols_to_scale"]




def prepare_df(age, income, loan_amount, loan_tenure, avg_dpd, open_loans, delinquency_ratio, credit_utilization, residence_type, loan_purpose, loan_type):
   input_data = {
    # Numerical Features
    "number_of_open_accounts": open_loans,
    "number_of_closed_accounts": 1,       # dummy
    "enquiry_count": 1,                   # dummy
    "credit_utilization_ratio": credit_utilization,
    "age": age,
    "number_of_dependants": 1,            # dummy
    "years_at_current_address": 1,        # dummy
    "zipcode": 1,                         # dummy
    "sanction_amount": 1,                 # dummy
    "processing_fee": 1,                  # dummy
    "gst": 1,                             # dummy
    "net_disbursement": 1,                # dummy
    "loan_tenure_months": loan_tenure,
    "principal_outstanding": 1,           # dummy
    "loan_to_income_ratio": loan_amount / income if income > 0 else 0,
    "deliquency_ratio": delinquency_ratio,
    "avg_dpd_per_deliquency": avg_dpd,
    "bank_balance_at_application": 1,     # dummy

    # Categorical Features (One-Hot Encoded)
    "residence_type_Mortgage": 1 if residence_type == "Mortgage" else 0,
    "residence_type_Owned": 1 if residence_type == "Owned" else 0,
    "residence_type_Rented": 1 if residence_type == "Rented" else 0,

    "loan_purpose_Auto": 1 if loan_purpose == "Auto" else 0,
    "loan_purpose_Business": 1 if loan_purpose == "Business" else 0,
    "loan_purpose_Education": 1 if loan_purpose == "Education" else 0,
    "loan_purpose_Home": 1 if loan_purpose == "Home" else 0,
    "loan_purpose_Personal": 1 if loan_purpose == "Personal" else 0,

    "loan_type_Secured": 1 if loan_type == "Secured" else 0,
    "loan_type_Unsecured": 1 if loan_type == "Unsecured" else 0

}
   
   df=pd.DataFrame([input_data])

   df[cols_to_scale]=scaler.transform(df[cols_to_scale])

   df=df[features]

   return df


def predict(age, income, loan_amount, loan_tenure, avg_dpd, open_loans,
            delinquency_ratio, credit_utilization, residence_type,
            loan_purpose, loan_type):

    df = prepare_df(age, income, loan_amount, loan_tenure, avg_dpd,
                    open_loans, delinquency_ratio, credit_utilization,
                    residence_type, loan_purpose, loan_type)

    # get probability of default
    default_prob = model.predict_proba(df)[:, 1][0]

    # map probability to score
    credit_score = int(900 - (default_prob * 600))  # wider range 300–900

    # assign rating
    if credit_score < 500:
        rating = "Poor"
    elif credit_score < 650:
        rating = "Average"
    elif credit_score < 750:
        rating = "Good"
    else:
        rating = "Excellent"

    return round(default_prob, 2), credit_score, rating



