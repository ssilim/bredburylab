#!/usr/bin/bash

exec 3<> /dev/tcp/${1:-127.0.0.1}/8000

printf "GET / HTTP/1.0\r\n" >&3
printf "\r\n" >&3

while read LINE <&3
do
   echo $LINE
done