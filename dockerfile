# Use an official Python runtime as a parent image
FROM python:3.9-slim

WORKDIR /app

# Copy the requirements file into the working directory
COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose the port that the app runs on
EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
