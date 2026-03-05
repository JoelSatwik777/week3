from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATASET_PATH = PROJECT_ROOT / 'dataset' / 'Churn_Modelling.csv'
MODEL_PATH = PROJECT_ROOT / 'ml' / 'banking_model.pkl'

TARGET_COLUMN = 'Exited'
DROP_COLUMNS = ['RowNumber', 'CustomerId', 'Surname']

MODEL_FEATURES = [
    'CreditScore',
    'Geography',
    'Gender',
    'Age',
    'Tenure',
    'Balance',
    'NumOfProducts',
    'HasCrCard',
    'IsActiveMember',
    'EstimatedSalary',
]

DEFAULT_THRESHOLD = 0.35