FROM crazymax/linguist:latest

RUN apk --update --no-cache add fish git rsync \
  && rm -rf /var/cache/apk/*

COPY generate_lang_history.fish /usr/bin/

ENTRYPOINT [ "/usr/bin/generate_lang_history.fish" ]
