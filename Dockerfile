FROM python:3.9-slim

# Set working directory inside container
WORKDIR /app

# Copy backend app into container
COPY backend/ /app/

# Upgrade pip
RUN pip install --upgrade pip

# Install Python dependencies
RUN pip install -r /app/requirements.txt

# Expose Flask port
EXPOSE 5000

# Start Flask app
CMD ["python", "app.py"]
