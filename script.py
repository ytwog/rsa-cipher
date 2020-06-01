import PySimpleGUI as sg
import math
import sys

element_input = sg.Text('поле ввода.', size=(40,1), text_color='Black')
element_output = sg.Text('поле вывода.', size=(39,1), text_color='Black')
element_prv = sg.InputText(size=(10, 1))
element_pub = sg.InputText(size=(10, 1))
element_out = sg.Output(size=(88, 1))
element_arr = sg.InputText(size=(44,10))
element_text = sg.InputText(size=(44,10))
element_save = sg.FileSaveAs()
element_open = sg.FileBrowse()

str_output = ''

def translate_to_arr(str_inp):
    output_str = ''
    for a in range(len(str_inp)):
        output_str += str(ord(str_inp[a]))
        if a != len(str_inp) - 1:
            output_str += ','
    return output_str

def is_prime(n):
    if n == 2:
        return True
    if n % 2 == 0 or n <= 1:
        return False

    sqr = int(math.sqrt(n)) + 1

    for divisor in range(3, sqr, 2):
        if n % divisor == 0:
            return False
    return True

def keygen(P, Q):
    #example:
        #p = 1009
        #q = 2741
    if not is_prime(P) or not is_prime(Q):
        raise ValueError('P or Q were not prime')
    x = 1
    y = 1

    eq = (P - 1) * (Q - 1) + 1
    xy = x*y

    while xy != eq:
        x += 1
        y = int(eq / x)
        xy = x*y


    print ("Публичный ключ: " + str(x))
    print ("Приватный ключ: " + str(y))
    print ("Число N (P*Q) : " + str(P*Q))
    return [[x,P*Q], y]

def extract_info(flag):
    i = sys.argv.index(flag) + 1
    return sys.argv[i]

def cipher(N, key, message):
    return pow(message, key, N)

layout = [
    [
        sg.Text('Входные данные:'),
        element_input,
        element_open,
        sg.Button('Сбросить способ ввода'),
    ],
    [
        sg.Text('Выходные данные:'),
        element_output,
        element_save,
        sg.Button('Сбросить способ вывода')
    ],
    [
        sg.Text('P = '),
        sg.InputText(size=(10,1)),
        sg.Text('Q = '),
        sg.InputText(size=(10,1)),
        sg.Button('Сгенерировать P и Q', enable_events='GENERATE'),
    ],
    [
        sg.Text('Public = '),
        element_pub,
        sg.Text('Private = '),
        element_prv,
        sg.Button('Сгенерировать ключи', enable_events='GENERATE'),
    ],
    [
        sg.Text('Исходный текст:', size=(38, 1)),
        sg.Text('Представление в виде массива чисел:', size=(44, 1))
    ],
    [
        element_text,
        element_arr
    ],
    [
        sg.Button('Перевести строку в численный массив', size=(38, 1)),
        sg.Button('Перевести массив в строку, если возможно', size=(39, 1))
    ],
    [
        sg.Button('Зашифровать', size=(24,2)),
        sg.Button('Расшифровать', size=(24,2))
    ],

    [
        sg.Text('Результат:'),
        sg.Button('Сохранить в выходной файл', enable_events='SAVE')
    ],
    [
        element_out
    ],
    [
        sg.Text('Отчет:')
    ],
    [
        sg.Output(size=(88, 6))
    ],
    [
        sg.Text('Программа написана в 2020 году', text_color=('Blue'))
    ],
    [
        sg.Text('студентом группы КИ17-02/1б, Апанасенко В.В.', text_color=('Blue'))
    ]
]
window = sg.Window('RSA-Cipher-v1.0', layout)
while True:                             # The Event Loop
    event, values = window.read()
    print(event, values) #debug
    if event in (None, 'Exit', 'Cancel'):
        break
    if event == 'Сгенерировать P и Q':
        print('Генерация P и Q...')
        print('Завершено')
    if event == 'Сгенерировать ключи':
        print('Генерация ключей...')
        if(values[0] == '' or values[1] == ''):
            print('Сначала введите или сгенерируйте P и Q')
            continue
        try:
            resKey = keygen(int(values[0]), int(values[1]))
            public_str = str(resKey[0][0])
            public_str += ','
            public_str += str(resKey[0][1])

            private_str = str(resKey[1])
            private_str += ','
            private_str += str(resKey[0][1])
            element_pub.update(public_str)
            element_prv.update(private_str)
        except:
            print('Ошибка ввода или обработки')
        finally:
            print('Завершено')

    if event == 'Зашифровать' or event == 'Расшифровать':
        decrypt = (event == 'Расшифровать')
        if(decrypt):
            print('Расшифровка...')
            key_p = str(values[3])
        else:
            print('Шифрование...')
            key_p = str(values[2])
        message = str(values[5])
        print('Ключ: ' + key_p)
        # Если ключ пустой:
        if (values[2] == '' and not decrypt) or (values[3] == '' and decrypt):
            print('Сначала введите или сгенерируйте ключи')
            continue
        if len(message) == 0:
            # Получаем массив чисел из строки, если пользователь этого не делал
            message = translate_to_arr(values[4])
            element_arr.update(message)
            if len(message) == 0:
                print('Введите сообщение или выберите входной файл.')
                continue
        # Обработка массива чисел
        try:
            arr_int_str = message.split(',')
            arr_int = {}
            for a in range(len(arr_int_str)):
                arr_int[a] = int(arr_int_str[a])
        except:
            print('Некорректный формат строки. Вводите его следующим образом:')
            print('<int>,<int>,...,<int>,<int>, где <int> - целое число')
            continue

        try:
            K = int(key_p.split(',')[0])
            N = int(key_p.split(',')[1])
        except:
            print('Ошибка ввода или обработки')
            continue
        output_str = ''
        for a in range(len(arr_int)):
            output_str += str(cipher(N, K, arr_int[a]))
            if a != len(arr_int)-1:
                output_str += ','
        print('Результат: ' + str(output_str))
        element_out.update(output_str)
        str_output = output_str
    if event == 'Сохранить в выходной файл':
        if values['Save As...'] == '':
            print('Файл не выбран.')
    if event == 'Сбросить способ ввода':
        element_input.update('поле ввода')
    if event == 'Сбросить способ вывода':
        element_output.update('поле вывода')
        values[1] = 'поле ввода'
        element_save.update()
    if event == 'Перевести строку в численный массив':
        element_arr.update(translate_to_arr(values[4]))
    if event == 'Перевести массив в строку, если возможно':
        str_inp = str(values[5])
        output_str = ''
        try:
            arr_int_str = str_inp.split(',')
            arr_int = {}
            for a in range(len(arr_int_str)):
                arr_int[a] = int(arr_int_str[a])
        except:
            print('Некорректный формат строки. Вводите его следующим образом:')
            print('<int>,<int>,...,<int>,<int>, где <int> - целое число')
            continue
        for a in range(len(arr_int)):
            output_str += str(chr(arr_int[a]))
        element_text.update(output_str)
window.close()