import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.metrics import classification_report, accuracy_score
import numpy as np


def age_group(age):
    if age < 25:
        return 'young'
    elif age < 45:
        return 'adult'
    elif age < 60:
        return 'middle_aged'
    else:
        return 'senior'

def lifestyle_risk(row):
    if row['bmi'] > 30:
        return 'high'
    if row['smoker'] == 'smoker' and row['bmi'] > 24:
        return 'high'
    elif row['smoker'] == 'smoker' or row['bmi'] > 24:
        return 'medium'
    else:
        return 'low'

def main():
    df = pd.read_csv('insurance.csv')
    print(df.sample(5))

    df_feat = df.copy()

    df_feat['bmi'] = df['weight'] / ((df['height']) ** 2)
    df_feat['age_group'] = df['age'].apply(age_group)

    df_feat['lifestyle_risk'] = df_feat.apply(lifestyle_risk, axis=1)

    print(df_feat['lifestyle_risk'].unique())
    print(df_feat['age_group'].unique())
    print(df_feat['bmi'].max())

    df_feat = df_feat.drop(columns=['age', 'weight', 'height','city', 'smoker'])

    x = df_feat[['bmi', 'age_group', 'lifestyle_risk','income_lpa', 'occupation']]
    y = df_feat['insurance_premium_category']

    categorical_features = ['age_group', 'lifestyle_risk', 'occupation']
    numeric_features = ['bmi', 'income_lpa']

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', 'passthrough', numeric_features),
            ('cat', OneHotEncoder(), categorical_features)
        ])

    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', RandomForestClassifier(random_state=42))
    ])

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

    pipeline.fit(x_train, y_train)

    y_pred = pipeline.predict(x_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model Accuracy: {accuracy:.2f}")

    import pickle
    with open('insurance_model.pkl', 'wb') as f:
        pickle.dump(pipeline, f)

if __name__ == "__main__":
    main()
    print("Model training and saving completed.")