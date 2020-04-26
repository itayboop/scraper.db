import requests
from bs4 import BeautifulSoup


def write_content(path: str, content: dict):
    with open(path, 'w') as file:
        file.writelines(str(content))


def import_usernames(table: str):
    user_names = {}

    for row in table.find_all('tr'):
        for name in row.find_all('a'):
            if name.text != '':  # not valid text
                user_names[name.text] = {}  # create the usernames dictionary

    return user_names  # return the dictionary


def import_houses(table, user_names):
    table = table.find_all('tr')

    for row in range(len(user_names) + 1):
        houses = []

        for user_info in table[row].find_all('a', class_="image"):
            if "House" in user_info['title']:
                houses.append(user_info['title'])
        user_names[list(user_names.keys())[row - 1]] = {"houses": houses}

    return user_names


def status(user_names: dict, status: str) -> dict:
    for i in range(len(list(user_names.keys()))):
        user_names[list(user_names.keys())[i]].update({"status": status})

    return user_names


def import_challenges(table):
    challenges_table = list()

    for row_table in table.find_all('tr'):
        row = list()

        for column_attr in row.find_all('td'):
            column = column_attr.text.replace('\n', '')
            row.append(column)
        challenges_table.append(lst)

    return challenges_table[1:]


def import_remarks(table, user_names):
    remarks = []
    for row in table.find_all('tr')[1:]:
        columns = row.find_all('td')

        for remark_column in range(3, len(columns), 14):  # qordination of remarks in table
            remarks.append({"remarks": columns[remark_column].text.replace('\n', '')})

    for i in range(len(remarks)):
        user_names[list(user_names.keys())[i]].update(remarks[i])

    return user_names


def import_games(table, game_name):
    game = {}
    game['game'] = game_name
    game['ranks'] = []

    for row in table.find_all('tr')[:4]:
        column_attr = row.find_all('td')

        for column in range(0, len(column_attr), 4):  # qordination of images in table
            title_images = column_attr[column].find_all('img')
            title_name = column_attr[column - 2].text.replace('\n', '')  # qordination of title names in table

            for title_image in title_images:
                game['ranks'].append({'name': title_name, 'image': title_image.get('src')})

    return game


def import_table_name(heads):
    tables_names = list()

    for head in heads:
        if "[edit]" in head.text:  # contatins in every h3 header in the page that relates to the tables headers
            tables_names.append(head.text.replace('[edit]', ''))

    print(tables_names)
    return tables_names


def import_solved_challenges(table):
    creators_and_solvers = list()
    result = list()

    for row in table.find_all('tr'):
        lst = list()
        cells = row.find_all('td')

        for cell in range(0, len(cells), 2):
            creator = cells[cell].text.replace('\n', '')
            solver = cells[cell - 1].text.replace('\n', '')
            creators_and_solvers.append({creator: solver})

    return creators_and_solvers


def users_tables_organize(tables):
    for table in range(2, 6):
        current_table = tables[table]

        user_names = import_usernames(current_table)
        user_names = import_houses(current_table, user_names)

        if table == 2:
            user_names = status(user_names, "active")

            write_content("code_ninja.txt", user_names)
        elif table == 3:
            user_names = status(user_names, "zombie")
            user_names = import_remarks(tables[table], user_names)
            write_content("zombies.txt", user_names)
        elif table == 4:
            user_names = status(user_names, "pension")

            write_content("pensions.txt", user_names)
        elif table == 5:
            user_names = status(user_names, "Commemoration")

            write_content("Commemoration.txt", user_names)


def games_tables_organize(tables):
    games = []

    for table in range(7, 11):
        current_table = tables[table]

        if table == 7:
            games.append(import_games(current_table, "samorai_c"))
        if table == 8:
            games.append(import_games(current_table, "+game"))
        if table == 9:
            games.append(import_games(current_table, "python_slayer"))
        if table == 10:
            games.append(import_games(current_table, "coffee_makers"))

    write_content("games.txt", games)


def solved_challnges_table_organize():
    final = list()
    second_page_url = 'https://beta.wikiversity.org/wiki/User:The_duke/solved_beta_challenges'
    r = requests.get(second_page_url)

    src = r.text
    soup = BeautifulSoup(src, 'lxml')
    tables = soup.find_all('table')
    heads = soup.find_all('h3')

    tables_names = import_table_name(heads)

    for name in range(len(tables_names)):
        print(import_solved_challenges)


def main():
    main_page_url = "https://beta.wikiversity.org/wiki/%D7%9C%D7%99%D7%9E%D7%95%D7%93%D7%99_%D7%9E%D7%97%D7%A9%D7%91%D7%99%D7%9D_%D7%91%D7%A9%D7%99%D7%98%D7%AA_%D7%91%D7%98%D7%90"
    r = requests.get(main_page_url)

    src = r.text

    soup = BeautifulSoup(src, 'lxml')
    tables = soup.find_all('table')

    users_tables_organize(tables)
    games_tables_organize(tables)
    solved_challnges_table_organize()


if __name__ == '__main__':
    main()