# Есть 2 таблицы — users и messages:
# users
# UID Name
# 1   «Вася»
# 2   «Петя»
# 3   «Маша»
# messages
# UID msg
# 1   “A”
# 1   “B”
# 2   “C”
# Напишите SQL-запрос, результатом которого будет таблица из двух полей: 
# «Имя пользователя» и «Общее количество сообщений».
# Запускаться всё должно из bash, одной строкой, либо bash скриптом.
# clear; ./2.sh;

#+------+-----------+
#| id   | count(id) |
#+------+-----------+
#|    1 |         2 |
#|    2 |         1 |
#+------+-----------+


#!/usr/bin/bash
var='select id, count(id) from messages group by id;'

mysql --user=root --password=qwertyQWERTY123! bredburylab << eof
$var
eof
