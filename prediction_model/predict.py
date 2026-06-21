import pickle
import pandas as pd
from schema.models import Patient, PredictionResponse


with open("prediction_model/" \
"insurance_model.pkl", "rb") as f:
    model = pickle.load(f)

class_labels = model.classes_.tolist()

def predict_insurance_premium(patient: Patient):
    input_data = pd.DataFrame([{
        'bmi': patient.bmi,
        'age_group': patient.age_group,
        'lifestyle_risk': patient.lifestyle_risk,
        'income_lpa': patient.income_lpa,
        'occupation': patient.occupation
    }])
    prediction = model.predict(input_data)
    probs = model.predict_proba(input_data)[0]
    confidence = max(probs)
    class_probabilities = {class_labels[i]: probs[i] for i in range(len(class_labels))}
    return PredictionResponse(
        predicted_category=prediction[0],
        confidence=confidence,
        class_probabilities=class_probabilities
    )