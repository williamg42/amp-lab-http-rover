#!/bin/bash
uci set wireless.sta.disabled='0'; uci commit wireless; wifi
sleep 30
if ping -q -c 1 -W 1 8.8.8.8 >/dev/null; then
  echo "IPv4 is up"
  
else
  echo "IPv4 is down"
  uci set wireless.sta.disabled='1'; uci commit wireless; wifi
fi

sleep 10
