# model_train.py
import pandas as pd, joblib, os
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# If you have dataset.csv (columns: text,label) it will be used; otherwise use small built-in examples
df = pd.read_csv("dataset.csv")  # must have 'text' and 'label' columns

X = df["text"]
y = df["label"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

pipe = Pipeline([
    ("vect", CountVectorizer()),
    ("tfidf", TfidfTransformer()),
    ("clf", MultinomialNB()),
])

pipe.fit(X_train, y_train)
pred = pipe.predict(X_test)
print(classification_report(y_test, pred))

joblib.dump(pipe, "sms_pipeline.pkl")
print("Saved sms_pipeline.pkl")