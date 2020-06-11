FROM python:3.7

WORKDIR /var/www/project

# requirements
COPY requirements.txt ./
RUN pip3 install -r ./requirements.txt

RUN nohup python3 /var/www/project/periodic/app.py &
CMD ["python3", "/var/www/project/website/manage.py", "runserver", "0.0.0.0:8000"]
