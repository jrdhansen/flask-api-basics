FROM python:3.9
WORKDIR /usr/src/app
# Copy all contents from same original dir as Dockerfile into container workdir
COPY ./ ./
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "app_restful_calculator.py"]
