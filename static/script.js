function predictPerformance() {
    const hours = document.getElementById('hours_studied').value || 0;
    const attendance = document.getElementById('attendance').value || 0;
    const assignments = document.getElementById('assignments').value || 0;

    fetch('/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            hours_studied: hours,
            attendance: attendance,
            assignments: assignments
        }),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not OK');
        }
        return response.json();
    })
    .then(data => {
        if (data.prediction) {
            document.getElementById('result').innerText = `Predicted Performance: ${data.prediction}`;
        } else {
            document.getElementById('result').innerText = `Error: ${data.error}`;
        }
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('result').innerText = 'An error occurred while predicting performance.';
    });
}
