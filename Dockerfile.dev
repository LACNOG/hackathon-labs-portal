FROM python:3.10

ENV PYTHONUNBUFFERED 1

WORKDIR /app/student_portal

COPY requirements.txt /app/
RUN pip install -r /app/requirements.txt

COPY student_portal /app/

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000", "--traceback" ]
