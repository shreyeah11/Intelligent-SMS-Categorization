# model_compare.py
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.metrics import classification_report, accuracy_score

# Classifiers to test
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.tree import DecisionTreeClassifier

# Load dataset
df = pd.read_csv("dataset.csv")  # must have columns 'text' and 'label'
X = df["text"]
y = df["label"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)

# Define models
models = {
    "Naive Bayes": MultinomialNB(),
    "Logistic Regression": LogisticRegression(max_iter=2000),
    "SVM": LinearSVC(),
    "Decision Tree": DecisionTreeClassifier()
}

best_model = None
best_score = 0

for name, clf in models.items():
    pipe = Pipeline([
        ("vect", CountVectorizer()),
        ("tfidf", TfidfTransformer()),
        ("clf", clf),
    ])
    pipe.fit(X_train, y_train)
    y_pred = pipe.predict(X_test)

    print(f"\n==== {name} ====")
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print(classification_report(y_test, y_pred))

    score = accuracy_score(y_test, y_pred)
    if score > best_score:
        best_score = score
        best_model = pipe
        best_name = name

# Save the best model
joblib.dump(best_model, "sms_pipeline.pkl")
print(f"\nBest model: {best_name} with accuracy {best_score:.2f}")
print("Saved best model as sms_pipeline.pkl")
