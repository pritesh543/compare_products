# Base Image
FROM python:3.8.6


# create and set working directory
RUN mkdir /app
WORKDIR /app


# Add current directory code to working directory
#ADD ./app /app


# Install project dependencies
COPY ./requirement.txt /app/requirement.txt

RUN pip install -r requirement.txt

COPY . /app/

CMD ["python", "manage.py", "runserver", "8000"]
#RUN python manage.py runserver 0.0.0.0:8000

