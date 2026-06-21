
# Insurance Premium Prediction API (FastAPI)

A small FastAPI project that provides CRUD for patient records and predicts insurance premium categories using a pre-trained model.

## Features

- REST API for managing patient records (create, read, update, delete)
- Predict insurance premium category from patient data or an existing patient
- Data persisted to `sample_data.json` for examples and local development

## Requirements

- Python 3.9+
- See `requirements.txt` for full dependency list

## Installation

1. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Run (local)

Start the app with Uvicorn:

```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8001
```

Or run directly (the project contains a __main__ entry in `app.py`):

```bash
python app.py
```

## API Endpoints

- `GET /` : Root message
- `GET /health` : Health check
- `GET /patient/all` : List all patients. Optional query `city` filters results.
- `GET /patient/{patient_id}` : Get a single patient by ID
- `POST /patient` : Create a patient (JSON body)
- `PUT /patient/update/{patient_id}` : Update a patient (partial update JSON)
- `DELETE /patient/delete/{patient_id}` : Delete a patient
- `POST /patient/predict/{patient_id}` : Predict premium for an existing patient by ID
- `POST /patient/predict` : Predict premium from supplied patient JSON payload

Example: predict from JSON

```bash
curl -X POST http://127.0.0.1:8001/patient/predict \
	-H "Content-Type: application/json" \
	-d '{"name":"Test","email":"a@b.com","gender":"Male","age":30,"weight":70,"height":1.7,"smoker":false,"income_lpa":5.0,"occupation":"private_job"}'
```

## Data and Model

- Example data file: `sample_data.json`
- Trained model: `prediction_model/insurance_model.pkl` (loaded by `prediction_model/predict.py`)
- Prediction logic: `prediction_model/predict.py` produces a `PredictionResponse` with `predicted_category`, `confidence`, and `class_probabilities`.

## Project Structure

- `app.py` - FastAPI application and routes
- `prediction_model/` - model loader and prediction helper
- `schema/models.py` - Pydantic models for request/response validation
- `sample_data.json` - example data storage used by the app
- `requirements.txt` - Python dependencies

## Notes

- This project persists data to `sample_data.json` for simplicity. For production use, swap in a database.
- Ensure `prediction_model/insurance_model.pkl` is present before calling prediction endpoints.

Reference - `https://www.youtube.com/playlist?list=PLKnIA16_RmvZ41tjbKB2ZnwchfniNsMuQ`


