FROM python:3

WORKDIR /usr/src/app

RUN pip install --no-cache-dir NBT Pillow

COPY . .

CMD [ "python", "-m", "http.server", "--cgi", "8000" ]
