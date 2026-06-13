from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
from catboost import CatBoostClassifier

app = FastAPI(
    title="Credit Scoring API",
    description="Микросервис для предсказания дефолта по кредиту",
    version="1.0.0"
)

scaler = joblib.load("models/scaler.pkl")
cb_model = CatBoostClassifier()
cb_model.load_model("models/catboost_model.cbm")

class ClientFeatures(BaseModel):
    RevolvingUtilizationOfUnsecuredLines: float
    age: int
    NumberOfTime30_59DaysPastDueNotWorse: int
    DebtRatio: float
    MonthlyIncome: float
    NumberOfOpenCreditLinesAndLoans: int
    NumberOfTimes90DaysLate: int
    NumberRealEstateLoansOrLines: int
    NumberOfTime60_89DaysPastDueNotWorse: int
    NumberOfDependents: int

@app.post("/predict")
def predict_default(client: ClientFeatures):
    
    if client.age < 18 or client.age > 85:
        return{
            "risk_probability": 1,
            "decision": "REJECT - Age out of bounds"
        }
    
    input_df  = pd.DataFrame([client.model_dump()])

    input_df.columns = [column.replace('_', '-') for column in input_df.columns]

    input_scaled = scaler.transform(input_df)

    probability = cb_model.predict_proba(input_scaled)[0, 1]

    return{
        "risk_probability": round(probability, 4),
        "decision": "REJECT" if probability > 0.5 else "APPROVE"
    }