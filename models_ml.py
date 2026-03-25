import pickle

with open("models/feature_names.pkl", "rb") as f:
    feature_names = pickle.load(f)

with open("models/rf_model.pkl", "rb") as f:
    rf_model = pickle.load(f)

with open("models/shap_explainer.pkl", "rb") as f:
    shap_explainer = pickle.load(f)