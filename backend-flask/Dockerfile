FROM python:3.10-slim-buster

WORKDIR /backend-flask

# Install backend dependencies
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# Copy the rest of the backend source
COPY . .

# Development environment
ENV FLASK_ENV=development

EXPOSE 4567

CMD [ "python3", "-m", "flask", "run", "--host=0.0.0.0", "--port=4567" ]
