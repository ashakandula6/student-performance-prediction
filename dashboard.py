import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from flask import Blueprint, render_template
from io import BytesIO
import base64

dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/dashboard')
def dashboard_view():
    data = pd.read_csv("dataset/student_data.csv")
    plt.figure(figsize=(6, 4))
    sns.barplot(x='study_hours', y='final_score', data=data)
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    
    return render_template('dashboard.html', plot_url=plot_url)
