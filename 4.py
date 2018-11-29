"""
Напишите несложный HTTP-сервер на Ruby или Python или на любом другом языке. Можно скриптовом,
можно нет.
Объём кода не должен превышать 5 КБ. Не забудьте написать тесты.
+ напишите bash скрипт, которым можно позапрашивать HTTP сервер.
"""

from http.server import HTTPServer, CGIHTTPRequestHandler
server_address = ("", 8000)
httpd = HTTPServer(server_address, CGIHTTPRequestHandler)
httpd.serve_forever()