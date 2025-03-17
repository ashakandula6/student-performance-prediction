from flask import Flask, request, render_template, send_file, session
import pickle
import numpy as np
import random
import os
import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a secure secret key

# List of motivational quotes
quotes = [
    "Keep pushing forward! Your hard work is paying off!",
    "Success is the sum of small efforts repeated daily!",
    "You're on the right track—stay focused!",
    "Every step forward counts—great job!",
    "Believe in yourself; you're doing amazing!"
]

# Improvement tips based on metrics
def get_improvement_tips(study_hours, attendance, assignments):
    tips = []
    if study_hours < 5:
        tips.append("Try to increase your study hours to at least 5 per day for better performance.")
    if attendance < 80:
        tips.append("Aim for at least 80% attendance to stay on track with your classes.")
    if assignments < 5:
        tips.append("Completing more assignments can boost your understanding—aim for at least 5.")
    if not tips:
        tips.append("Great job! Keep up the excellent work.")
    return tips

# Function to determine rating (1-4 scale)
def get_rating(value, max_value):
    normalized_value = value / max_value
    if normalized_value < 0.25:
        return 1  # Poor
    elif normalized_value < 0.5:
        return 2  # Fair
    elif normalized_value < 0.75:
        return 3  # Satisfactory
    else:
        return 4  # Good/Excellent

# Load the trained model or data
model_path = os.path.join('models', 'student_performance_model.pkl')
model = None
try:
    with open(model_path, 'rb') as file:
        loaded_object = pickle.load(file)
        print(f"Loaded object type: {type(loaded_object)}")  # Debug the type
        if hasattr(loaded_object, 'predict'):  # Check if it’s a model
            model = loaded_object
        else:
            print("Warning: Loaded object is not a model. Using fallback formula.")
            model = None  # Fallback to formula if not a model
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get the form inputs
        study_hours = float(request.form['study_hours'])
        attendance = float(request.form['attendance'])
        assignments = float(request.form['assignments'])
        name = request.form['name']
        student_id = request.form['student_id']
        department = request.form['department']
        
        # Prepare input data
        input_data = np.array([[study_hours, attendance, assignments]])
        
        # Make prediction
        if model is not None:
            prediction = model.predict(input_data)[0] * 100  # Scale to percentage if needed
        else:
            # Fallback formula if model is not available
            prediction = (0.3 * study_hours * 10) + (0.4 * attendance) + (0.3 * assignments * 10)
            if prediction > 100:
                prediction = 100.0
        
        # Select a random motivational quote
        quote = random.choice(quotes)
        
        # Store data in session
        session['study_hours'] = study_hours
        session['attendance'] = attendance
        session['assignments'] = assignments
        session['prediction'] = prediction
        session['name'] = name
        session['student_id'] = student_id
        session['department'] = department
        
        # Debug: Print session data
        print("Session data after prediction:", session)
        
        return render_template('index.html', 
                             prediction=f"{prediction:.2f}", 
                             quote=quote,
                             study_hours=study_hours,
                             attendance=attendance,
                             assignments=assignments,
                             name=name,
                             student_id=student_id,
                             department=department)
    
    except Exception as e:
        error_message = f"An error occurred while predicting performance: {str(e)}"
        return render_template('index.html', error=error_message)

@app.route('/dashboard')
def dashboard():
    # Retrieve data from session
    study_hours = session.get('study_hours', 0)
    attendance = session.get('attendance', 0)
    assignments = session.get('assignments', 0)
    prediction = session.get('prediction', 0)
    
    # Generate improvement tips
    tips = get_improvement_tips(study_hours, attendance, assignments)
    
    # Assume maximum values for scaling (adjust based on your data)
    max_study_hours = 10  # e.g., max 10 hours per day
    max_assignments = 10  # e.g., max 10 assignments
    
    # Scale values for doughnut charts (0-100)
    scaled_study_hours = (study_hours / max_study_hours) * 100
    scaled_attendance = attendance  # Already in percentage
    scaled_assignments = (assignments / max_assignments) * 100
    
    return render_template('dashboard.html', 
                         study_hours=study_hours, 
                         attendance=attendance, 
                         assignments=assignments,
                         scaled_study_hours=scaled_study_hours,
                         scaled_attendance=scaled_attendance,
                         scaled_assignments=scaled_assignments,
                         prediction=prediction,
                         tips=tips)

@app.route('/download_report')
def download_report():
    # Retrieve data from session
    study_hours = session.get('study_hours', 0)
    attendance = session.get('attendance', 0)
    assignments = session.get('assignments', 0)
    prediction = session.get('prediction', 0)
    name = session.get('name', 'Unknown')
    student_id = session.get('student_id', 'N/A')
    department = session.get('department', 'N/A')

    # Debug: Print session data to verify
    print("Session data in download_report:", session)

    # Convert to float for rating calculation
    try:
        study_hours = float(study_hours)
        attendance = float(attendance)
        assignments = float(assignments)
        prediction = float(prediction)
    except (ValueError, AttributeError):
        study_hours = 0
        attendance = 0
        assignments = 0
        prediction = 0

    # Define maximum values for rating
    max_study_hours = 10
    max_attendance = 100
    max_prediction = 100

    # Calculate ratings
    rating_attendance = get_rating(attendance, max_attendance)
    rating_communication = get_rating(prediction, max_prediction)
    rating_listening_skills = get_rating(study_hours, max_study_hours)  # Using study hours as a proxy

    # Create a PDF in memory
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Title
    p.setFillColor(colors.blue)
    p.rect(0, height - 50, width, 50, fill=1, stroke=0)
    p.setFillColor(colors.white)
    p.setFont("Helvetica-Bold", 16)
    p.drawCentredString(width / 2, height - 30, "Student Performance Review")

    # Student Information Section
    p.setFillColor(colors.black)
    p.setFont("Helvetica", 12)
    p.line(50, height - 60, width - 50, height - 60)  # Separator line
    p.drawString(50, height - 90, "Name")
    p.rect(150, height - 100, 200, 20)
    p.drawString(50, height - 120, "Student ID")
    p.rect(150, height - 130, 200, 20)
    p.drawString(50, height - 150, "Department")
    p.rect(150, height - 160, 200, 20)
    p.drawString(400, height - 90, "Date")
    p.rect(500, height - 100, 100, 20)

    # Fill in the values
    p.drawString(155, height - 95, str(name))
    p.drawString(155, height - 125, str(student_id))
    p.drawString(155, height - 155, str(department))
    p.drawString(505, height - 95, str(os.environ.get('CURRENT_DATE', 'March 17, 2025')))

    # Ratings Section
    p.setFillColor(colors.blue)
    p.rect(0, height - 200, width, 20, fill=1, stroke=0)
    p.setFillColor(colors.black)
    p.line(50, height - 210, width - 50, height - 210)  # Separator line
    p.setFont("Helvetica-Bold", 10)
    p.drawString(50, height - 230, "1 = Poor  2 = Fair  3 = Satisfactory  3 = Good  4 = Excellent")

    # Rating fields for Attendance, Communication, and Listening Skills
    y_start = height - 260
    items = [
        ("Attendance", rating_attendance),
        ("Communication", rating_communication),
        ("Listening Skills", rating_listening_skills)
    ]
    for i, (label, rating) in enumerate(items):
        p.setFont("Helvetica", 12)
        p.drawString(50, y_start - (i * 30), label)
        for j in range(1, 5):
            p.rect(200 + (j * 40), y_start - (i * 30) - 5, 20, 20)
            if j == rating:
                p.drawCentredString(210 + (j * 40), y_start - (i * 30), "✓")

    p.showPage()
    p.save()
    
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name='performance_report.pdf', mimetype='application/pdf')

if __name__ == '__main__':
    app.run(debug=True)