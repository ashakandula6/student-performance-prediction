import pickle

# Load the trained model
def load_model():
    with open('./models/performance_model.pkl', 'rb') as f:
        return pickle.load(f)
