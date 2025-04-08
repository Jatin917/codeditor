# Use official Python image
FROM python:3.10

# Set working directory
WORKDIR /app

# Copy everything into the container
COPY ./game .

# Install dependencies
RUN pip install -r requirements.txt

# Expose the Flask port
EXPOSE 10000

# Run the Flask app
CMD ["python", "server.py"]
