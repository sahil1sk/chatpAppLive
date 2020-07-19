FROM python:3

ENV PYTHONUNBUFFERED 1

# so working directory is app
WORKDIR /app

# add all the data into the app
ADD . /app

# copy requirements.txt file into app requirements.txt file
COPY ./requirements.txt /app/requirements.txt

# now here we run the install requirements.txt
RUN pip install -r requirements.txt

# after that copy all the data into the app
COPY . /app

RUN python manage.py migrate