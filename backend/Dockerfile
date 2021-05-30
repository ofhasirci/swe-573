FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY ./requirements.txt /app/
RUN pip install -r /app/requirements.txt
RUN ls /app/
COPY . /app/
CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]