FROM python:3

ADD cocheV3_5.py /

RUN pip3 install requests

CMD [ "python", "./cocheV3_5.py" ]
