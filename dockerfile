# 1. Use the official slim Python 3.11 image as the base
FROM python:3.11-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy only the requirements file first (this speeds up future builds via caching)
COPY requirements.txt .

# 4. Install your Python packages
RUN pip install --no-cache-dir -r requirements.txt

# 5. Download the SpaCy model package
RUN python -m spacy download en_core_web_sm

# 6. Copy the rest of your local project files into the container
COPY . .

# 7. Expose the port Flask runs on (usually 5000)
EXPOSE 5000

# 8. Define the command to start your Flask application
CMD ["python", "stream.py"]
