"""
В системе авторизации есть следующее ограничение: 
«Логин должен начинаться с латинской буквы, он может состоять из латинских букв, 
цифр, точки и минуса и должен заканчиваться латинской буквой или цифрой. 
Минимальная длина логина — 1 символ. Максимальная — 20 символов».
Напишите код, проверяющий соответствие входной строки этому правилу.
На выходе должен получиться скрипт или бинарник с regexp&#39;ом и тестами.
Запускаться так:
python 1.py
"""


def check_login(name):
    # alphabet = [a-z], [A-Z]
    alphabet = [chr(x + 97) for x in range(26)] \
               + [chr(x + 65) for x in range(26)]

    if len(name) >= 1 and len(name) <= 20 \
            and not name.endswith('-') \
            and not name.endswith('.') \
            and name[0] in alphabet:

        # good_symbol: [a-z], [A-Z], [0-9], [-, .]
        good_symbol = alphabet \
                   + [chr(x+48) for x in range(10)] \
                   + [chr(45)] + [chr(46)]

        for i in name:
            if i not in good_symbol:
                # print('Логин {} должен состоять из латинских букв, цифр, точки и минуса'.format(name))
                return False
        return True

    else:
        # print('Логин {} должен быть от 1 до 20 символов,'
              # '\nдолжен заканчиваться на цифру или букву латинского алфавита'.format(name))
        return False


if __name__ == '__main__':
    print('='*25, 'TESTS', '='*25)
    def test_one_symbol():
        if check_login('S') == True:
            print('Test test_one_symbol("S") is OK!')
        else:
            print('Test test_one_symbol("S") is Fail!')

    def test_20_symbol():
        if check_login('qwertyuiopasdfghjklz') == True:
            print('Test test_20_symbol("qwertyuiopasdfghjklz") is OK!')
        else:
            print('Test test_20_symbol("qwertyuiopasdfghjklz") is Fail!')

    def test_nick1():
        if check_login('Silimka123') == True:
            print('Test test_nick1("Silimka123") is OK!')
        else:
            print('Test test_nick1("Silimka123") is Fail!')

    def test_nick2():
        if check_login('Silim') == True:
            print('Test test_nick2("Silim") is OK!')
        else:
            print('Test test_nick2("Silim") is Fail!')

    def test_nick3():
        if check_login('2Silim') == True:
            print('Test test_nick3("2Silim") is OK!')
        else:
            print('Test test_nick3("2Silim") is Fail!')

    def test_rus():
        if check_login('Silimka.фф') == True:
            print('Test test_rus("Silimka.фф") is OK!')
        else:
            print('Test test_rus("Silimka.фф") is Fail!')

    def test_minus():
        if check_login('Silimka1-') == True:
            print('Test test_minus("Silimka1-") is OK!')
        else:
            print('Test test_minus("Silimka1-") is Fail!')


    test_one_symbol()
    test_20_symbol()
    test_nick1()
    test_nick2()
    test_nick3()
    test_rus()
    test_minus()