import requests
from bs4 import BeautifulSoup

BLACK_MAGIC = 11
PWN_GAME = 12
START = 2
END = 5


def write_content(path: str, content: dict):
    """Writes the content of the found users and solved challenges to a file.

    :param path: where the file will be save.
    :type path: str
    :param content: the cotent to be written into the file.
    """
    with open(path, 'w') as file:
        file.writelines(str(content))
        file.writelines('\n')


def get__descrip_title(titles):
    title_and_discription = list()
    j = 0
    context = list()

    for i in range(3, len(titles) - 1):
        title = titles[i].get_text()
        title = title.replace('[edit]', '')

        context = titles[i].find_next_sibling()
        if context.name == 'p':
            context = context.get_text()
            title_and_discription.append({'name': title, 'description': context})
        else:
            title_and_discription.append({'name': title, 'description': ''})

    print(title_and_discription)


def get_pwn_game(table, game_name: str) -> dict:
    image = {}
    image['game'] = game_name
    image['ranks'] = []

    for row in table.find_all('tr')[START:END]:
        pictures_attrs = row.find_all('img')

        for img in pictures_attrs:
            title_name = img.attrs['alt']
            title_source = img.attrs['src']
            image['ranks'].append({'name': title_name, 'image': title_source})

    return image


def main():
    main_page_url = "https://beta.wikiversity.org/wiki/%D7%9C%D7%99%D7%9E%D7%95%D7%93%D7%99_%D7%9E%D7%97%D7%A9%D7%91%D7%99%D7%9D_%D7%91%D7%A9%D7%99%D7%98%D7%AA_%D7%91%D7%98%D7%90"
    r = requests.get(main_page_url)
    src = r.text
    soup = BeautifulSoup(src, 'lxml')
    tables = soup.find_all('table')
    titles = soup.find_all('h2')

    pwn_game_content = get_pwn_game(tables[PWN_GAME], 'Game_of_Pwns')
    write_content('/home/itay5245/pwn_game.txt', pwn_game_content)

    get__descrip_title(titles)


if __name__ == '__main__':
    main()