from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel, Field
from faker import Faker
import uvicorn

fake = Faker()

# --- Recommendation Functions (Your Model Logic) ---
loan_types = ['Personal Loan', 'Auto Loan', 'Mortgages', 'Home Equity Loan', 'Student Loan', 'Business Loan', 'Credit Card']

def assign_product_rankings(customer_data):
    """Assigns a score to each loan type based on customer data, then ranks them."""
    loan_scores = {loan: 0 for loan in loan_types}

    # Credit Score impact
    if customer_data['Credit_Score'] < 600:
        loan_scores['Business Loan'] -= 5
        loan_scores['Mortgages'] -= 3
        loan_scores['Home Equity Loan'] -= 2
    elif customer_data['Credit_Score'] > 750:
        loan_scores['Credit Card'] -= 1

    # Student Loan rules
    if customer_data['Age'] < 30 and customer_data['Loan_Purpose'] == "Education":
        loan_scores['Student Loan'] += 5
    else:
        loan_scores['Student Loan'] -= 3

    # Home ownership impact
    if customer_data['Residential_Status'] == "Owns house":
        loan_scores['Mortgages'] += 4
        loan_scores['Home Equity Loan'] += 3

    # Debt Consolidation
    if customer_data['Loan_Purpose'] == "Debt Consolidation":
        loan_scores['Personal Loan'] += 3
        loan_scores['Home Equity Loan'] += 1

    # Self-employment impact
    if customer_data['Employment_Status'] == 'Self-Employed':
        loan_scores['Business Loan'] += 3

    # Income level considerations
    if customer_data['Income_Level'] == "Low":
        loan_scores['Mortgages'] -= 2

    # Auto Purchase rule
    if customer_data['Loan_Purpose'] == 'Auto Purchase':
        loan_scores['Auto Loan'] += 4

    # Sort loan types by score in descending order
    ranked_loans = sorted(loan_scores.items(), key=lambda item: item[1], reverse=True)
    return ranked_loans

# --- FastAPI Application Setup ---
class CustomerInput(BaseModel):
    Age: int = Field(..., alias="Age")
    Gender: str = Field(..., alias="Gender")
    Marital_Status: str = Field(..., alias="Marital Status")
    Income_Level: str = Field(..., alias="Income Level")
    Occupation: str = Field(..., alias="Occupation")
    Residential_Status: str = Field(..., alias="Residential Status")
    Dependents: int = Field(..., alias="Dependents")
    Debt_to_Income: float = Field(..., alias="Debt-to-Income")
    Credit_Score: int = Field(..., alias="Credit Score")
    Employment_Status: str = Field(..., alias="Employment Status")
    Loan_Purpose: str = Field(..., alias="Loan Purpose")

app = FastAPI(title="Bank Recommendation API", description="Provides product ranking based on customer data.")

@app.post("/recommend")
def recommend_product(customer: CustomerInput = Body(...)):
    try:
        customer_data = customer.dict()
        recommendations = assign_product_rankings(customer_data)
        return {
            "ranked_recommendations": recommendations,
            "best_recommendation": recommendations[0][0]
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    # Change this line
    uvicorn.run("service_rec:app", host="0.0.0.0", port=8000, reload=True)
