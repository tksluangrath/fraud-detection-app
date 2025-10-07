import streamlit as st
import pandas as pd
import joblib

model = joblib.load("fraud_detection_model.pkl")

st.title("Fraud Detection Prediction App")

st.markdown("Please enter the transaction details and use the predict button")

st.divider()

ui_to_model_type = {
    "Payment": "PAYMENT",
    "Transfer": "TRANSFER",
    "Withdrawal": "CASH_OUT",
    "Deposit": "CASH_IN",
}
type_display = st.selectbox(
    "Transaction Type",
    list(ui_to_model_type.keys()),
    index=0
)
transaction_type = ui_to_model_type[type_display]
amount = st.number_input("Transaction Amount", min_value=0.0, value=1000.0)
oldbalanceOrg = st.number_input("Old Balance (Sender)", min_value=0.0, value=10000.0)
newbalanceOrig = st.number_input("New Balance (Sender)", min_value=0.0, value=9000.0)
oldbalanceDest = st.number_input("Old Balance (Receiver)", min_value=0.0, value=0.0)
newbalanceDest = st.number_input("New Balance (Receiver)", min_value=0.0, value=0.0)

if st.button("Predict"):
    input_data = pd.DataFrame({
        "type": [transaction_type],
        "amount": [amount],
        "oldbalanceOrg": [oldbalanceOrg],
        "newbalanceOrig": [newbalanceOrig],
        "oldbalanceDest": [oldbalanceDest],
        "newbalanceDest": [newbalanceDest]
    })
    
    prediction = model.predict(input_data)
    label = "Legitimate" if prediction == 0 else "Fraudulent"

    st.subheader(f"Prediction: {label}")
    
    if prediction[0] == 1:
        st.success("The transaction is likely to be fraudulent.")
    else:
        st.success("The transaction is likely to be legitimate.")