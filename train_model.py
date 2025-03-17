from sklearn.linear_model import LinearRegression
import joblib

model = LinearRegression()
# Train model with your dataset (e.g., from dataset/performance_data.csv)
# ...
joblib.dump(model, 'models/student_performance_model.pkl')