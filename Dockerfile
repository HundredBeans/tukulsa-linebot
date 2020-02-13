FROM python:3.6.5
RUN pip install --upgrade pip
RUN mkdir -p /tukulsa-linebot
COPY . /tukulsa-linebot
RUN pip install --no-cache-dir -r /tukulsa-linebot/requirements.txt
WORKDIR /tukulsa-linebot
ENTRYPOINT [ "python" ]
CMD [ "app.py" ]
