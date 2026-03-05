from __future__ import annotations

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from ml.config import DATASET_PATH, DROP_COLUMNS, MODEL_PATH, TARGET_COLUMN


def build_pipeline(categorical_cols, numeric_cols) -> Pipeline:
    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_cols),
            ('num', StandardScaler(), numeric_cols),
        ]
    )

    return Pipeline(
        steps=[
            ('preprocessor', preprocessor),
            (
                'classifier',
                RandomForestClassifier(
                    n_estimators=300,
                    random_state=42,
                    class_weight='balanced',
                    n_jobs=-1,
                ),
            ),
        ]
    )


def train_and_save_model() -> None:
    df = pd.read_csv(DATASET_PATH)
    df = df.drop(columns=DROP_COLUMNS)

    X = df.drop(columns=[TARGET_COLUMN])
    y = df[TARGET_COLUMN]

    categorical_cols = X.select_dtypes(include=['object']).columns.tolist()
    numeric_cols = X.select_dtypes(exclude=['object']).columns.tolist()

    pipeline = build_pipeline(categorical_cols, numeric_cols)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    pipeline.fit(X_train, y_train)

    y_prob = pipeline.predict_proba(X_test)[:, 1]
    y_pred = (y_prob > 0.35).astype(int)

    print('Accuracy:', round(accuracy_score(y_test, y_pred), 4))
    print('ROC-AUC:', round(roc_auc_score(y_test, y_prob), 4))
    print('\nClassification report:\n', classification_report(y_test, y_pred))

    joblib.dump(pipeline, MODEL_PATH)
    print(f'Model saved to {MODEL_PATH}')


if __name__ == '__main__':
    train_and_save_model()