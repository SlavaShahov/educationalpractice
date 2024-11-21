import csv
import requests
from bs4 import BeautifulSoup

filename = "coin.csv"#файл для хранения информации о монетах
url = 'https://coinmarketcap.com/'#ссылка на сайт
#браузеры, с котороых может открыться сайт
headers ={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 YaBrowser/24.1.0.0 Safari/537.36"}
data=[]#массив для дальнейшего заполнения файла 

def t_line():#функция выводит горизонтальные линии таблицы 
    print("+-------+-----------------------+-----------------------+-------------------------------+")

def table():#функция выводит "шапку" таблицы
    print("\t\t    <<Parsing of ten popular cryptocurrencies>>")
    t_line()
    print("| №\t|\tName(Symbol)\t|\t  Prise  \t|\t   Market_Cap   \t|")
    t_line()
    

def pars_from_site():#функция парсинга с сайта
    resp = requests.get(url, headers=headers).text#запрос на работу сайта, если сайт работает то возвращает код 200
    soup = BeautifulSoup(resp, "lxml")#передаёт весь код сайта
    tbody = soup.find("tbody")#возвращает код html блока tbody
    coins=tbody.find_all("tr")#возвращает код блока tr, тк в tbody у нас дальше в tr вся инфа о монетах
    coin_data=[]#массив для промежуточной записи информации о монетах
 
    table()#выводим шапку таблицы
    for coin in coins:
         namber = coin.find(class_="sc-4984dd93-0 iWSjWE")#возвращают коды HTML по классам
         name = coin.find(class_="sc-4984dd93-0 kKpPOn")
         symbol = coin.find(class_="sc-4984dd93-0 iqdbQL coin-item-symbol")
         price = coin.find(class_="sc-9d064f2d-0 cAhksY")
         marketcap=coin.find(class_="sc-7bc56c81-1 bCdPBp")
    

         if name:#выводим информацию о манетах в виде таблицы
            print(f"|{namber.text}\t|\t{name.text}({symbol.text}) \t|\t  {price.text}  \t|\t {marketcap.text} \t|")
            #записываем информацию о монетах в промежуточный массив 
            coin_data=[name.text,symbol.text,price.text,marketcap.text]
            
            data.append(coin_data)#добавляем в массив для заполнения файла информацию о монете
            
            t_line()#рисуем линию таблицы



def write_in_file():# функция записи в файл
    with open(filename, 'w', newline='') as csvfile:
         csv_writer = csv.writer(csvfile)
    
         for row in data:
             csv_writer.writerow(row)



def find_by_name(_data, name):#функция поиска по имени 
    items = []
    for item in _data:
        for i in item:
            if name in i:
                items.append(item)
                break
            else: 
                break
    return items



def print_data(_data):#функция вывода результатов поиска
    
    print(f"{'Name':10}\t\t{'Symbol':10}\t\t{'Prise':10}\t\t{'Market_Cap':10} ")
    
    for item in _data:
        print(*[i + '\t\t\t' for i in item])
    
    print("Кол-во элементов: ", len(_data))



def main():
    pars_from_site()
    write_in_file()
    while True:
        found = find_by_name(data, input("Введите строку для поиска криптовалюты: "))
        if found:
            print_data(found)
        else:
            print("Криптовалюты не найдены!")

        print("\n\nПовторить поиск?")
        while True:
            choice = input("[Y]es|[N]o: ").upper()
            if choice not in ['Y', 'N']:
                print("Ошибка! Некорректный ввод!" )
            else:
                break

        if choice == 'N':
            break

 


if __name__ == '__main__':
    main()
