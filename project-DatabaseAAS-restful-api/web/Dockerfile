FROM python:3.9
RUN rm -rf /usr/src/app/
WORKDIR /usr/src/app
COPY ./ ./
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "app.py"]