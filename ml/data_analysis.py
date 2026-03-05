import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, roc_auc_score
from sklearn.preprocessing import StandardScaler
import joblib

# Load banking dataset
df = pd.read_csv("../dataset/Churn_Modelling.csv")

print("="*50)
print("Original Shape:", df.shape)

# Drop unnecessary columns
df.drop(["RowNumber", "CustomerId", "Surname"], axis=1, inplace=True)

print("\nShape after dropping ID columns:", df.shape)

print("\nChurn value counts:")
print(df["Exited"].value_counts())

print("\nData Types:")
print(df.dtypes)

# Separate features and target
X = df.drop("Exited", axis=1)
y = df["Exited"]

# Identify categorical and numeric columns
categorical_cols = X.select_dtypes(include=["object"]).columns
numeric_cols = X.select_dtypes(exclude=["object"]).columns

print("\nCategorical Columns:", list(categorical_cols))
print("Numeric Columns:", list(numeric_cols))

# Preprocessing


preprocessor = ColumnTransformer(
    transformers=[
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_cols),
        ("num", StandardScaler(), numeric_cols)
    ]
)

# Model pipeline
model_pipeline = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("classifier", RandomForestClassifier(
        n_estimators=200,
        max_depth=None,
        random_state=42,
        class_weight="balanced"
    ))
])

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model_pipeline.fit(X_train, y_train)

import pandas as pd

feature_names = model_pipeline.named_steps['preprocessor'].get_feature_names_out()
importances = model_pipeline.named_steps['classifier'].feature_importances_

importance_df = pd.DataFrame({
    "Feature": feature_names,
    "Importance": importances
}).sort_values(by="Importance", ascending=False)

print("\nTop Important Features:")
print(importance_df.head(10))

# Predictions
y_prob = model_pipeline.predict_proba(X_test)[:, 1]
y_pred = (y_prob > 0.35).astype(int)

def retention_strategy(customer):
    suggestions = []
    
    if customer["NumOfProducts"] <= 1:
        suggestions.append("Offer cross-sell products (credit card / loan)")
    
    if customer["IsActiveMember"] == 0:
        suggestions.append("Send engagement campaign")
    
    if customer["Balance"] > 100000:
        suggestions.append("Assign relationship manager")
    
    if customer["Tenure"] < 3:
        suggestions.append("Provide onboarding benefits")
    
    return suggestions

# Evaluation
print("\nModel Evaluation:")
print("Accuracy:", accuracy_score(y_test, y_pred))
print("ROC-AUC Score:", roc_auc_score(y_test, y_prob))

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# Save model
joblib.dump(model_pipeline, "banking_model.pkl")

print("\nModel saved successfully for Banking project.")