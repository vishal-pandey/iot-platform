FROM ubuntu:22.04
ENV PYTHONUNBUFFERED 1
# RUN apt install libpq-dev python3-dev
RUN mkdir /airtrik
WORKDIR /airtrik
ADD requirement1.txt /airtrik/
RUN apt-get update -y
RUN apt-get upgrade -y
RUN apt install python3 -y
RUN apt install python3-pip -y
RUN apt install libpq-dev -y
RUN apt-get install gcc -y
RUN apt-get install python3-dev -y
RUN apt-get install libmysqlclient-dev -y
# RUN pip3 install virtualenv  --break-system-packages
RUN apt install python3-venv -y
RUN python3 -m venv env
# RUN source env/bin/activate
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirement1.txt

# RUN pip install --upgrade --user urllib3
# RUN pip install --upgrade --user six
ADD . /airtrik/
ENTRYPOINT [ "python3", "manage.py", "runserver", "0.0.0.0:8085" ]
