import requests
from bs4 import BeautifulSoup


def write_content(path: str, content: dict):
	"""Writes the content of the found users and solved challenges to a file.

	:param path: where the file will be save.
	:type path: str
	:param content: the cotent to be written into the file.
	"""
	with open(path, 'w') as file:
		file.writelines(str(content))


def import_usernames(table):
	"""Takes the username from the tables into a dicitionary.
	:param table: The content of the page to be analyzed.
	:type table: bs4 element
	:return: the usernames from the table
	:rtype: dict
	"""
	user_names = {}

	for row in table.find_all('tr'):	# take each row from the table
		for name in row.find_all('a'):	# take each cell from the row
			if name.text != '':  # not valid text
				user_names[name.text] = {}  # create the usernames dictionary

	return user_names


def import_houses(table, user_names: dict) -> dict:
	"""Takes the houses of each username
	:param table: The content of the page to be analyzed.
	:type table: bs4 element
	:param user_names: the extracted usernames from the table.
	:user_names type: dict
	:return: user_names updated with the houses for each username.
	:rtype: dict
	"""
	table = table.find_all('tr')	# find all rows from the context.
	for row in range(len(user_names) + 1):
		houses = []

		for user_info in table[row].find_all('a', class_="image"):	# get every tag with a and class image in it.
			if "House" in user_info['title']:	# if that tag contains the word House in that title.
				houses.append(user_info['title'])	# append it into houses dicitionary.
		user_names[list(user_names.keys())[row - 1]] = {"houses": houses}	# appends the houses dict into user_names value.

	return user_names


def status(user_names: dict, status: str) -> dict:
	"""Gets and sets the status for each username (zombie, pension, active, commoration).
	:param user_names: the usernames to be add them the status.
	:type user_names: dict
	:param status: the status of each username (see func brief).
	:type param: str
	:return: usernames updated with status.
	:rtype: dict
	"""
	for i in range(len(list(user_names.keys()))):
		user_names[list(user_names.keys())[i]].update({"status": status})

	return user_names


def import_challenges(table) -> list:
	"""Gets the challenges from the page (c, python, java... etc)
	:param table: the context to analayze.
	:type table: bs4 element
	:return: list of the challenges
	:rtype: list
	"""
	challenges_table = list()

	for row_table in table.find_all('tr'):
		row = list()

		for column_attr in row.find_all('td'):
			column = column_attr.text.replace('\n', '')
			row.append(column)
		challenges_table.append(row)

	return challenges_table[1:]


def import_remarks(table, user_names: dict) -> dict:
	"""Gets all the remarks of each user.
	:param table: the context to be analyzed.
	:type table: bs4 element
	:param user_names: the usernames dict to append the remarks into.
	:type user_names: dict
	:return: the username updated with the remarks.
	:rtype: dict
	"""
	remarks = []
	for row in table.find_all('tr')[1:]:
		columns = row.find_all('td')

		for remark_column in range(3, len(columns), 14):  # qordination of remarks in table
			remarks.append({"remarks": columns[remark_column].text.replace('\n', '')})

	for i in range(len(remarks)):
		user_names[list(user_names.keys())[i]].update(remarks[i])

	return user_names


def import_games(table, game_name: list) -> list:
	"""Gets all the games of beta and the first 3 ranked players.
	:param table: the context to be analyzed.
	:type table: bs4 element
	:param game_name: the name of the game to be extracted.
	:type game_name: str>(?)
	:return: game table with the name of it and first 3 players.
	:rtype: list
	"""
	game = {}
	game['game'] = game_name
	game['ranks'] = []

	for row in table.find_all('tr')[:4]:	# find the three first players of this game
		column_attr = row.find_all('td')

		for column in range(0, len(column_attr), 4):  # coordinates of images in table
			title_images = column_attr[column].find_all('img')
			title_name = column_attr[column - 2].text.replace('\n', '')  # coordinates of title names in table

			for title_image in title_images:
				game['ranks'].append({'name': title_name, 'image': title_image.get('src')})

	return game


def import_table_name(heads) -> list:
	"""Gets the name of each table.
	:param heads: tool variable to find the name of the table.
	:type heads: bs4 element
	:return: the names of the tables.
	:rtype: list
	"""
	tables_names = list()
	for head in heads:
		if "[edit]" in head.text:  # contatins in every h3 header in the page that relates to the tables headers
			tables_names.append(head.text.replace('[edit]', ''))

	return tables_names


def import_solved_challenges(table) -> list:
	"""Gets the solved challenges and their solvers.
	:param table: the context to be analyzed (isnt the same as the previous ones).
	:type table: bs4 element
	:return: challenges name and its solvers.
	:rtype: list
	"""
	challenges_and_solvers = list()
	result = list()

	for row in table.find_all('tr'):
		lst = list()
		cells = row.find_all('td')

		for cell in range(0, len(cells), 2):
			challenge = cells[cell].text.replace('\n', '')
			solver = cells[cell - 1].text.replace('\n', '')
			challenges_and_solvers.append({challenge: solver})

	return challenges_and_solvers


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


def solved_challnges_table_organize(tables):
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