document.getElementById('predictBtn').addEventListener('click', function() {
    // Get user input values
    const studyHours = parseFloat(document.getElementById('studyHours').value) || 0;
    const attendance = parseFloat(document.getElementById('attendance').value) || 0;
    const assignments = parseInt(document.getElementById('assignments').value) || 0;
  
    // Simple Prediction Logic (Mocked for now)
    const predictedPerformance = (studyHours * 10 + attendance * 0.5 + assignments * 5).toFixed(2);
  
    // Display Prediction
    document.getElementById('predictedPerformance').textContent = `${predictedPerformance}%`;
  
    // Store data for report generation
    localStorage.setItem('studyHours', studyHours);
    localStorage.setItem('attendance', attendance);
    localStorage.setItem('assignments', assignments);
    localStorage.setItem('predictedPerformance', predictedPerformance);
  });
  
  document.getElementById('downloadReport').addEventListener('click', function() {
    const studyHours = localStorage.getItem('studyHours');
    const attendance = localStorage.getItem('attendance');
    const assignments = localStorage.getItem('assignments');
    const predictedPerformance = localStorage.getItem('predictedPerformance');
  
    const reportContent = `
      Student Performance Report\n
      --------------------------------\n
      Study Hours: ${studyHours}\n
      Attendance: ${attendance}%\n
      Assignments Completed: ${assignments}\n
      Predicted Performance: ${predictedPerformance}%
    `;
  
    const blob = new Blob([reportContent], { type: 'text/plain' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = 'performance_report.txt';
    link.click();
  });
  
  document.getElementById('analyticsDashboard').addEventListener('click', function() {
    alert('Visual Analytics Dashboard will be integrated soon!');
  });
  