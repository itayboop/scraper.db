import requests


def import_table(section, start_char1, start_char2, end_char1, end_char2, path):
    url = "https://beta.wikiversity.org/w/index.php?title=%D7%9C%D7%99%D7%9E%D7%95%D7%93%D7%99%D7%9E%D7%97%D7%A9%D7%91%D7%99%D7%9D%D7%91%D7%A9%D7%99%D7%98%D7%AA%D7%91%D7%98%D7%90&action=edit&section=" + section

    r = requests.get(url, 'r')

    page = r.content
    page = page.decode()

    for letter in range(len(page)):
        if page[letter] == start_char1 and page[letter + 1] == start_char2:
            start_of_table_index = letter
            break

    for letter in range(len(page) - 1, 0, -1):
        if page[letter] == end_char1 and page[letter - 1] == end_char2:
            end_of_table_index = letter
            break

    page = page[start_of_table_index:end_of_table_index]

    with open(path, 'w') as file:
        file.write(page)


def username_slice(page):
    usernames = {}
    break_point = 0

    for times in range(page.count('[[User:')):
        f_index = page.find("[[User:", break_point) + 7
        l_index = page.find("|", f_index)

        break_point = l_index

        usernames[page[f_index:l_index]] = {}

    return usernames


def read_file(path):
    with open(path, 'r') as file:
        table_context = file.read()
    return table_context


def main():
    import_table('14', '{', '|', '}', '|', 'page_context')
    table_context = read_file("page_context")
    usernames = username_slice(table_context)

    print(usernames.keys())


if __name__ == 'main':
    main()