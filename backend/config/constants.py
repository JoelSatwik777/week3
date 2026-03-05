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

LOW_RISK_MAX = 0.35
MEDIUM_RISK_MAX = 0.60

ALLOWED_UPLOAD_EXTENSIONS = {'.csv', '.xlsx', '.xls'}
MAX_BATCH_ROWS = 20000

AGE_BUCKETS = [
    ('18-30', 18, 30),
    ('31-45', 31, 45),
    ('46-60', 46, 60),
    ('60+', 61, 200),
]

CREDIT_SCORE_BANDS = [
    ('Poor', 300, 579),
    ('Fair', 580, 669),
    ('Good', 670, 739),
    ('Excellent', 740, 1000),
]
