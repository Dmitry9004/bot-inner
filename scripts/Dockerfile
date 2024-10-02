FROM python:3
COPY . /app
RUN pip3 install pypsrp
RUN apt-get install libkrb5-dev
RUN  pip install gssapi
RUN pip install krb5
CMD ["python", "./app/exc.py"]
