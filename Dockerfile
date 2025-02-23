# Use official Python image
FROM python:3.10

# Set the working directory
WORKDIR /app

# Copy dependencies and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Expose the port Flask runs on
EXPOSE 5000

# Run Flask application
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]