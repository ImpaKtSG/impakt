FROM python:3.12
WORKDIR /app

# Install dependencies
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip --no-cache-dir -r requirements.txt

# Copy source code
COPY . .
ENV PYTHON_ENV=development

# Run the application
CMD ["python", "api/app.py"]