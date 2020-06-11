FROM python:3.7

WORKDIR /var/www/project

# requirements
COPY requirements.txt ./
RUN pip3 install -r ./requirements.txt

CMD ["python3", "/var/www/project/website/manage.py", "runserver", "0.0.0.0:8000"]
