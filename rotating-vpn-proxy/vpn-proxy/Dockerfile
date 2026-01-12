FROM alpine:latest

RUN apk add --no-cache openvpn tinyproxy gettext socat curl

COPY entrypoint.sh /entrypoint.sh
COPY tinyproxy.conf /etc/tinyproxy/tinyproxy.conf

ENTRYPOINT ["/entrypoint.sh"]