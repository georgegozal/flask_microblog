FROM python:3.10.6-slim-bullseye
# ENV PYTHONUNBUFFERED 1

RUN mkdir /flask_app
WORKDIR /flask_app

COPY requirements.txt /flask_app/
RUN pip install --no-cache-dir -r requirements.txt

# copy everything to the flask_app directory
COPY . /flask_app/ 

ENV FLASK_APP=app \
    FLASK_ENV=production

EXPOSE 5000

# # everything is above, is created during container build

#CMD ["flask", "run", "--host=0.0.0.0"] 
CMD ["python", "app.py"]
