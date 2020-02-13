FROM python:3.6.5
RUN mkdir -p /tukulsa-linebot
COPY . /tukulsa-linebot
RUN pip install -r /tukulsa-linebot/requirements.txt
WORKDIR /tukulsa-linebot
ENTRYPOINT [ "python" ]
CMD [ "app.py" ]
