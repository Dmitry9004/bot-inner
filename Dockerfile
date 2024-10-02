FROM python:3
COPY . ./app
RUN ["sh", "./app/package-pwsh"]
RUN pip3 install aiogram
RUN pip3 install pypsrp
CMD ["python", "./app/BOT-TEST.py"]
