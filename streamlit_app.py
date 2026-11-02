"""Streamlit front-end for the Iris classifier.

Deploy on Streamlit Community Cloud: main file = streamlit_app.py
The model is trained automatically on first start if it doesn't exist
(models/*.joblib is not committed to git).
"""
import os

import joblib
import streamlit as st

from src.train import MODEL_PATH, main as train_model

CLASSES = ["setosa", "versicolor", "virginica"]

st.set_page_config(page_title="Iris Classifier", page_icon="🌸")


@st.cache_resource(show_spinner="Training model (first start only)...")
def load_model():
    if not os.path.exists(MODEL_PATH):
        train_model()
    return joblib.load(MODEL_PATH)


model = load_model()

st.title("🌸 Iris Flower Classifier")
st.write("Adjust the measurements (cm) and predict the species.")

col1, col2 = st.columns(2)
with col1:
    sepal_length = st.slider("Sepal length", 4.0, 8.0, 5.1, 0.1)
    sepal_width = st.slider("Sepal width", 2.0, 4.5, 3.5, 0.1)
with col2:
    petal_length = st.slider("Petal length", 1.0, 7.0, 1.4, 0.1)
    petal_width = st.slider("Petal width", 0.1, 2.5, 0.2, 0.1)

if st.button("Predict", type="primary"):
    features = [[sepal_length, sepal_width, petal_length, petal_width]]
    idx = int(model.predict(features)[0])
    probs = model.predict_proba(features)[0]
    st.success(f"Predicted species: **{CLASSES[idx]}**")
    st.bar_chart({"probability": dict(zip(CLASSES, probs))})
