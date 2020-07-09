import requests
from bs4 import BeautifulSoup


def write_content(path: str, content: str):
	"""Writes the content of the found users and solved challenges to a file.
	:param path: where the file will be save.
	:type path: str
	:param content: the cotent to be written into the file.
	"""
	with open(path, 'w') as file:
		file.writelines(str(content))


def import_usernames(table) -> list:
	"""Takes the username from the tables into a dictionary.
	:param table: The content of the page to be analyzed.
	:type table: bs4 element
	:return: the usernames from the table
	:rtype: dict
	"""
	users = list()

	for row in table.find_all('tr'):
		for name in row.find_all('a'):
			if name.text != '':  # not valid text
				users.append({'name': name.text})

	return users  # return the list


def import_houses(table, users):
	"""Takes the houses of each username
	:param table: The content of the page to be analyzed.
	:type table: bs4 element
	:param users: the extracted users from the table.
	:user_names type: dict
	:return: user_names updated with the houses for each username.
	:rtype: list
	"""
	table = table.find_all('tr')

	for row in range(len(users))[1:]:
		houses = list()

		for user_info in table[row].find_all('a', class_="image"):
			if "House" in user_info['title']:		# all of the houses contains the word 'house'.
				houses.append(user_info['title'])

		users[row - 1].update({"houses": houses})

	return users


def set_status(users: list, status: str) -> list:
	"""Gets and sets the status for each username (zombie, pension, active, commoration).
	:param users: list of users.
	:type users: list
	:param status: the status of each username (see func brief).
	:type status: str
	:return: user_names updated with status.
	:rtype: dict
	"""
	for user in range(len(users)):
		users[user].update({"status": status})

	return users


def import_remarks(table, users: list) -> list:
	"""Gets all the remarks of each user.
	:param table: the context to be analyzed.
	:type table: bs4 element
	:param users: the user names dict to append the remarks into.
	:type users: list
	:return: the username updated with the remarks.
	:rtype: list
	"""
	remarks = []

	for row in table.find_all('tr')[1:]:
		columns = row.find_all('td')

		for remark_column in range(3, len(columns), 14):  # coordination of remarks in table
			remarks.append({"remarks": columns[remark_column].text.replace('\n', '')})

	for i in range(len(remarks)):
		users[i].update({"remarks": remarks[i]})

	return users


def import_games(table, game_name: str) -> dict:
	"""Gets all the games of beta and the first 3 ranked players.
	:param table: the context to be analyzed.
	:type table: bs4 element
	:param game_name: the name of the game to be extracted.
	:type game_name: str
	:return: game table with the name of it and first 3 players.
	:rtype: dict
	"""
	game = dict()
	game['game'] = game_name
	game['ranks'] = []

	for row in table.find_all('tr')[:4]:
		column_attr = row.find_all('td')

		for column in range(0, len(column_attr), 4):  # coordination of images in table
			title_images = column_attr[column].find_all('img')
			title_name = column_attr[column - 2].text.replace('\n', '')  # coordination of title names in table

			for title_image in title_images:
				game['ranks'].append({'name': title_name, 'image': title_image.get('src')})

	return game


def import_table_name(heads) -> list:
	"""Gets the name of each table.
	:param heads: all of the h3 tags.
	:type heads: bs4 element
	:return: the names of the tables.
	:rtype: list
	"""
	tables_names = list()

	for head in heads:
		if "[edit]" in head.text:  # contains in every h3 header in the page that relates to the tables headers
			tables_names.append(head.text.replace('[edit]', ''))

	return tables_names


def import_solved_challenges(table) -> list:
	"""Gets the solved challenges and their solvers.
	:param table: the context to be analyzed (isnt the same as the previous ones).
	:type table: bs4 element
	:return: challenges name and its solvers.
	:rtype: list
	"""
	creators_and_solvers = list()

	for row in table.find_all('tr'):
		cells = row.find_all('td')

		for cell in range(0, len(cells), 2):
			challenge_name = cells[cell].text.replace('\n', '')
			solvers = cells[cell - 1].text.replace('\n', '').split('* ')[1:]

			creators_and_solvers.append({'challenge_name': challenge_name, 'solvers': solvers})

	return creators_and_solvers


def users_tables_organize(tables):
	"""connect to all the function that collects data about users and organize the data.
	:param tables: all of the tables in the page.
	:type tables: bs4 element.
	"""
	for table in range(2, 6):
		current_table = tables[table]

		users = import_usernames(current_table)
		users = import_houses(current_table, users)

		if table == 2:		# code ninja table
			users = set_status(users, "active")

			write_content("code_ninja.txt", str(users))
		elif table == 3:	# zombies table
			users = set_status(users, "zombie")
			users = import_remarks(tables[table], users)

			write_content("zombies.txt", str(users))
		elif table == 4:		# pension talbe
			users = set_status(users, "pension")

			write_content("pensions.txt", str(users))
		elif table == 5:	# commemoration table
			users = set_status(users, "Commemoration")

			write_content("Commemoration.txt", str(users))


def games_tables_organize(tables):
	"""connect to all of the functions that collects data about the games and organize the data.
	:param tables: all of the tables in the page.
	:type tables: bs4 element
	"""
	games = list()

	for table in range(7, 11):
		current_table = tables[table]

		if table == 7:		# samorai C game
			games.append(import_games(current_table, "samorai_c"))
		if table == 8:		# +game - java game
			games.append(import_games(current_table, "+game"))
		if table == 9:		# python slayer game
			games.append(import_games(current_table, "python_slayer"))
		if table == 10:		# coffee makers game - _
			games.append(import_games(current_table, "coffee_makers"))

	write_content("games.txt", str(games))


def solved_challenges_table_organize():
	"""connects to all of the functions that collects data on the solved challenges table an organize the data.
	"""
	solved_challenges = list()
	second_page_url = 'https://beta.wikiversity.org/wiki/User:The_duke/solved_beta_challenges'
	r = requests.get(second_page_url)

	src = r.text
	soup = BeautifulSoup(src, 'lxml')
	tables = soup.find_all('table')
	heads = soup.find_all('h3')

	tables_names = import_table_name(heads)

	for table_name in range(len(tables_names)):
		challenges_and_solvers = import_solved_challenges(tables[table_name])
		solved_challenges.append({'subject': tables_names[table_name], 'challenges': challenges_and_solvers})

	write_content('solved_challenges.txt', str(solved_challenges))


def import_challenges_organize(tables: bs4, challenges: list):
	for table in range(17, 39):
		if table != 19 and table != 21:
			challenges[table - 17 - int(table > 19) - int(table > 21)]['challenges'].append(import_challenges(tables[table]))

	for challenge in challenges:
		write_content("challenges_tables\\" + challenge['challenge_name'], challenge['challenges'])


def challenges_table_name(soup: bs4) -> list:
	"""Gets the challenges names from the page (c, python, java... etc)
	:param soup: all of the page in 'lxml' format.
	:type soup: bs4 element
	:return: list of the challenges names
	:rtype: list
	"""
	challenges = list()
	div_tags = soup.find_all('div', class_="mw-content-ltr")

	for div_tag in div_tags:
		li_tags = div_tag.find_all('li', class_="toclevel-1 tocsection-54")

		for li_tag in li_tags:
			challenges = [challenge_name.text for challenge_name in li_tag.find_all('span', class_="toctext")[1:]]

			break

	for i, challenge_name in enumerate(challenges):
		challenges[i] = dict({'challenge_name': challenge_name, 'challenges': []})

	return challenges


def import_challenges(table: bs4) -> list:
	"""Gets the challenges of each category from the page (c, python, java... etc)
	:param table: each table is a new category.
	:type table: bs4 element
	:return: list of the challenges of each category
	:rtype: list
	"""
	info_keys = ['name', 'points', 'description', 'deadline']  # the required challenges' information
	challenges_list = list()

	for row in table.find_all('tr')[1:]:
		current_challenge = dict()

		challenge_info = [cell for cell in row.text.split('\n') if
						  cell != '']  # scraping the whole challenge information
		challenge_info = challenge_info[:2] + challenge_info[3:6:2]  # slicing the required challenge information

		if len(challenge_info) == 3:
			challenge_info.append('-')

		for key, info in zip(info_keys, challenge_info):
			current_challenge.update({key: info})

		challenges_list.append(current_challenge)

	return challenges_list


def main():
	main_page_url = "https://beta.wikiversity.org/wiki/%D7%9C%D7%99%D7%9E%D7%95%D7%93%D7%99_%D7%9E%D7%97%D7%A9%D7%91%D7%99%D7%9D_%D7%91%D7%A9%D7%99%D7%98%D7%AA_%D7%91%D7%98%D7%90"
	r = requests.get(main_page_url)

	src = r.text

	soup = BeautifulSoup(src, 'lxml')
	tables = soup.find_all('table')

	challenges = challenges_table_name(soup)
	users_tables_organize(tables)
	games_tables_organize(tables)
	solved_challenges_table_organize()
	import_challenges_organize(tables, challenges)


if __name__ == '__main__':
	main()
