FROM python:3
WORKDIR /usr/src/app
COPY . .
RUN pip3 install -U pip
RUN pip3 install -U -r requirements.txt
CMD ["main.py"]
ENTRYPOINT ["python3"]
