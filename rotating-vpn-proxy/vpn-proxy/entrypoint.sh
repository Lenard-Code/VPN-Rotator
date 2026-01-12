#!/bin/sh

openvpn --config "$VPN_CONFIG" --verb 4 &

while ! ip link show tun0 >/dev/null 2>&1; do
  sleep 1
done

# Substitute port in tinyproxy.conf at runtime
envsubst < /etc/tinyproxy/tinyproxy.conf > /tmp/tinyproxy.conf

tinyproxy -c /tmp/tinyproxy.conf

wait