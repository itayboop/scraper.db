import requests

HOUSE_FROM_USER = 9


def import_table(section: int, start_char1: str, start_char2: str, end_char1: str, end_char2: str, path: str):
    start_of_table_index = ''
    end_of_table_index = ''
    url = "https://beta.wikiversity.org/w/index.php?title=%D7%9C%D7%99%D7%9E%D7%95%D7%93%D7%99_%D7%9E%D7%97%D7%A9%D7%91%D7%99%D7%9D_%D7%91%D7%A9%D7%99%D7%98%D7%AA_%D7%91%D7%98%D7%90&action=edit&section=" + str(
        section)

    r = requests.get(url, 'r')  # sending a GET request to the page's url

    # decoding the content
    page = r.content
    page = page.decode()

    # finding the start of the table by 2 special characters
    for letter in range(len(page)):
        if page[letter] == start_char1 and page[letter + 1] == start_char2:
            start_of_table_index = letter
            break

    # finding the end of the table by 2 special characters
    for letter in range(len(page) - 1, 0, -1):
        if page[letter] == end_char1 and page[letter - 1] == end_char2:
            end_of_table_index = letter
            break

    table = page[start_of_table_index:end_of_table_index]  # slicing to get the table

    with open(path, 'w') as file:  # writing the content to a file
        file.write(table)


def username_slice(table: str) -> dict:
    user_names = {}  # the dictionary of the user names
    start_point = 0  # setting a start point to 0

    # finding the username
    for times in range(table.count('[[User:')):
        f_index = table.find("[[User:", start_point) + 7
        l_index = table.find("|", f_index)

        start_point = l_index  # setting the start point to the end of the username

        user_names[table[f_index:l_index]] = {}  # adding the usernames to the dictionary as keys

    return user_names  # return the dictionary


def read_file(path: str) -> str:
    # reads the file and return its context
    with open(path, 'r') as file:
        table_context = file.read()
    return table_context


def user_info(username: str, table_context: str) -> dict:
    table_context = table_context.split('\n')  # splitting the context by rows

    for row in range(len(table_context)):
        if table_context[row].find(username) != -1:
            topics = import_subjects_and_points(row, table_context)
            houses = import_houses(row, table_context)
            # title = import_title(row, table_context)

            return topics, houses


def import_subjects_and_points(row: str, table_context: list) -> dict:
    points_index = 0
    topics = {}  # declaring a dictionary of the whole topics and points
    subjects_and_points = {}  # declaring a dictionary of subject and points

    for i in range(2, 8, 2):
        subject_index = row + i
        points_index = subject_index + 1
        subjects_and_points[table_context[subject_index][2:]] = table_context[points_index][2:]
    print(table_context[points_index + 1])  # bad points

    topics["topics"] = subjects_and_points  # assign the dictionary

    return topics


def import_houses(row: int, table_context: list) -> dict:
    houses = {}
    house_lst = []
    houses_index = row + HOUSE_FROM_USER

    houses_row = table_context[houses_index]
    houses_row = houses_row.replace(']', '|')
    houses_row = houses_row.split('|')

    for word in range(len(houses_row)):
        if 'px' in houses_row[word]:
            house_lst.append(houses_row[word + 1])

    houses["houses"] = house_lst

    return houses


def import_title(row: int, table_context: list) -> dict:
    pass


def main():
    import_table(14, '{', '|', '}', '|', 'page_context')
    table_context = read_file("page_context")
    user_names = username_slice(table_context)

    for username in user_names.keys():
        user_names[username] = user_info(username, table_context)

    print(user_names)


if __name__ == '__main__':
    main()
