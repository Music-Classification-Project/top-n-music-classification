# Use the official lightweight Python image
FROM python:3.11-slim
# Set working directory
WORKDIR /app
# Copy dependencies and install
COPY requirements.txt .
RUN pip install -r requirements.txt
# Copy code
COPY . .
# Expose port and run
CMD ["gunicorn", "--bind", ":8080", "main:app"]
