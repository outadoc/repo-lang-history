FROM crazymax/linguist:latest

RUN apk --update --no-cache add python3 py3-pip git \
  && rm -rf /var/cache/apk/*

COPY ./generate-history /src

WORKDIR /src

RUN pip3 install -r requirements.txt

ENTRYPOINT [ "/usr/bin/python3", "main.py" ]
