import requests
from bs4 import BeautifulSoup


def write_content(path: str, content: dict):
    with open(path, 'w') as file:
        file.write(str(content))


def import_usernames(table: str):
    user_names = {}

    for tr in table.find_all('tr'):
        for name in tr.find_all('a'):
            if name.text != '':
                user_names[name.text] = {}
    return user_names


def import_houses(table, user_names):
    table = table.find_all('tr')

    for tr in range(len(user_names) + 1):
        houses = []
        titles = []

        for user_info in table[tr].find_all('a', class_="image"):
            if "House" in user_info['title']:
                houses.append(user_info['title'])
        user_names[list(user_names.keys())[tr - 1]] = {"houses": houses}
    return user_names


def status(user_names: dict, status: str) -> dict:
    for i in range(len(list(user_names.keys()))):
        user_names[list(user_names.keys())[i]].update({"status": status})

    return user_names


def challenges_taker(table):
    final = list()

    for row in table.find_all('tr'):
        lst = list()

        for column_attr in row.find_all('td'):
            column = column_attr.text.replace('\n', '')
            lst.append(column)
        final.append(lst)

    return final[1:]


def main():
    url = "https://beta.wikiversity.org/wiki/%D7%9C%D7%99%D7%9E%D7%95%D7%93%D7%99_%D7%9E%D7%97%D7%A9%D7%91%D7%99%D7%9D_%D7%91%D7%A9%D7%99%D7%98%D7%AA_%D7%91%D7%98%D7%90"
    r = requests.get(url)
    src = r.text

    soup = BeautifulSoup(src, 'lxml')
    tables = soup.find_all('table')

    write_content("table20.txt", challenges_taker(tables[20]))

    for table in range(2, 6):
        current_table = tables[table]

        user_names = import_usernames(current_table)
        user_names = import_houses(current_table, user_names)

        if table == 2:
            user_names = status(user_names, "active")
            write_content("code_ninja.txt", user_names)
        elif table == 3:
            user_names = status(user_names, "zombie")
            write_content("zombies.txt", user_names)
        elif table == 4:
            user_names = status(user_names, "pension")
            write_content("pensions.txt", user_names)
        elif table == 5:
            user_names = status(user_names, "Commemoration")
            write_content("Commemoration.txt", user_names)


if __name__ == '__main__':
    main()
