FROM python:2.7
LABEL maintainer="Walid A. Shaari"
### add more labels as a metadata for the project and also  to make it possible to run in openshift
COPY ./techtrends /app
WORKDIR /app

### created a user to run app/container as a regular user not root
### however, faced issues with pip install, so had to add user and make
### thier home directory the app directory

RUN     useradd -u 100001 -d /app app-user

### apply image security best practices.
RUN    chown -R app-user /app

USER   app-user

RUN pip install --no-warn-script-location --user -r requirements.txt
EXPOSE 3111

# command to run on container start
CMD [ "python", "app.py" ]
