import pickle
import pandas as pd
from typing import List, Optional
from fastapi.responses import JSONResponse
import uvicorn
from fastapi import FastAPI, HTTPException, Path, Query
import json
from prediction_model.predict import predict_insurance_premium
from schema.models import ListPatientsResponse, Patient, PatientUpdate


DATA_PATH = "/home/adi/Projects/Learning/FastAPI/sample_data.json"

app = FastAPI()

def load_data():
    try:
        with open(DATA_PATH, "r") as file:
            data = file.read()
    except FileNotFoundError:
        print(f"File not found: {DATA_PATH}")
        return {}

    if not data.strip():
        print(f"File is empty: {DATA_PATH}")
        return {}

    try:
        return json.loads(data)
    except json.JSONDecodeError:
        print(f"Invalid JSON in file: {DATA_PATH}")
        return {}

def save_data(data):
    with open(DATA_PATH, "w") as file:
        json.dump(data, file, indent=2)

@app.get("/")
async def root():
    return {"message": "Welcome to the Insurance Premium Prediction API!"}

@app.get("/health")
async def health_check():
    return {"status": "OK"}


@app.get("/patient/all", response_model=ListPatientsResponse)
async def get_patients(city: Optional[str] = Query(None, description="Filter patients by city")):
    data = load_data()
    if not data:
        raise HTTPException(status_code=404, detail="No patients found")
    if city:
        data = {id: item for id, item in data.items() if item.get("city") == city}
    list_patients = [Patient(**item) for item in data.values()]
    return ListPatientsResponse(total=len(data), patients=list_patients)


@app.get("/patient/{patient_id}", response_model=Patient)
async def read_patient(patient_id: str = Path(..., description="The ID of the patient to get", min_length=1)):
    data = load_data()
    if data.get(patient_id):
        return Patient(**data[patient_id])
    raise HTTPException(status_code=404, detail="Patient not found")


@app.post("/patient")
async def create_patient(patient: Patient):
    data = load_data()
    data[patient.id] = patient.model_dump(mode="json")
    save_data(data)
    return JSONResponse(content={"message": "Patient created successfully", "patient_id": patient.id}, status_code=201)


@app.put("/patient/update/{patient_id}")
async def update_patient(patient_id: str, updated_patient: PatientUpdate):
    data = load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")
    existing_patient = data[patient_id]
    existing_patient.update(updated_patient.model_dump(exclude_unset=True))
    updated_data = Patient(**existing_patient)
    data[patient_id] = updated_data.model_dump(mode="json")
    save_data(data)
    return JSONResponse(content={"message": "Patient updated successfully"}, status_code=200)


@app.delete("/patient/delete/{patient_id}")
async def delete_patient(patient_id: str):
    data = load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")
    del data[patient_id]
    save_data(data)
    return JSONResponse(content={"message": "Patient deleted successfully"}, status_code=200)


@app.post("/patient/predict/{patient_id}")
async def predict_insurance_cost(patient_id: str = Path(..., description="The ID of the patient to predict insurance cost for", min_length=1)):
    data = load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")
    patient = Patient(**data[patient_id])
    try:
        prediction = predict_insurance_premium(patient)
        return prediction
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@app.post("/patient/predict")
async def predict_insurance_cost_from_data(patient: Patient):
    try:
        prediction = predict_insurance_premium(patient)
        return prediction
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8001, reload=True)
