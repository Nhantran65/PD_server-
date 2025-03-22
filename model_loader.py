import pickle
import numpy as np

# Load mô hình CatBoost đã lưu
MODEL_PATH = "model/CatBoost.pkl"

def load_model():
    with open(MODEL_PATH, "rb") as file:
        model = pickle.load(file)
    return model

# Khởi tạo model khi import file này
catboost_model = load_model()
