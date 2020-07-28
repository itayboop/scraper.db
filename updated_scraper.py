import requests
from os import mkdir
from bs4 import BeautifulSoup

PWN_GAME_TABLE_INDEX = -5
NINJAS_TABLE_INDEX = 0
ACTIVES_TABLE_INDEX = 1
ZOMBIES_TABLE_INDEX = 2
PENSIONS_TABLE_INDEX = 3
COMMEMORATION_TABLE_INDEX = 4
TABLE_OFFSET = 16
LAST_CHALLENGES_TABLE = 36
USELESS_TABLE_1 = 18
USELESS_TABLE_2 = 20


global g_users

g_users = 	g_users = [{'status': 'ninja', 'users':[]},
			{'status': 'active', 'users':[]},
			{'status': 'zombie', 'users':[]},
			{'status': 'pension', 'users':[]},
			{'status': 'commemoration', 'users':[]}]

def soup_site(url):
	r = requests.get(url)

	return BeautifulSoup(r.text, 'html.parser')


def write_content(path: str, content: str):
	"""Writes the content of the found users and solved challenges to a file.
	:param path: where the file will be save.
	:type path: str
	:param content: the cotent to be written into the file.
	"""
	while True:
		try:
			with open(path, 'w') as file:
				file.writelines(str(content))

				break
		except IOError:
			mkdir(path[:path.index('\\')])

		
def download_image(content, title):
	while True:
		try:
			with open("pics\\" + title + ".png", "wb") as file:
				file.write(content)

				break
		except FileNotFoundError:
			mkdir("pics")


def users_tables_organize(tables):
	"""connect to all the function that collects data about users and organize the data.
	:param tables: all of the tables in the page.
	:type tables: bs4 element.
	"""
	ninja, active, zombie, pension, commemoration, *_ = tables
	
	ninja_active(ninja, NINJAS_TABLE_INDEX)
	ninja_active(active, ACTIVES_TABLE_INDEX)
	zombie_info(zombie)
	pension_commemoration_info(pension, PENSIONS_TABLE_INDEX)
	pension_commemoration_info(commemoration, COMMEMORATION_TABLE_INDEX)


def ninja_active(table, table_index):
	for tr in table.tbody.find_all('tr')[1:]:
		_, name, *_, houses = tr.find_all('td')
		houses = [house['title'] for house in houses.find_all('a')]
		g_users[table_index]['users'].append(dict({'name': name.a.text, 'houses': houses}))


def zombie_info(table):
	for tr in table.tbody.find_all('tr')[1:]:
		_, name, _, remark, *_, houses = tr.find_all('td')

		houses = [house['title'] for house in houses.find_all('a')]
		g_users[ZOMBIES_TABLE_INDEX]['users'].append(dict({'name': name.a.text, 'houses': houses, 'remarks': remark.text.replace('\n', '')}))


def pension_commemoration_info(table, table_index):
	for tr in table.tbody.find_all('tr')[1:]:
		name, *_, houses = tr.find_all('td')

		if not houses.a is None:
			houses = [house['title'] for house in houses.find_all('a')] 
			g_users[table_index]['users'].append(dict({'name':name.text.replace('\n', ''), 'houses': houses}))
		else:
			g_users[table_index]['users'].append(dict({'name':name.text.replace('\n', ''), 'houses': []}))


def games_tables_organize(tables):
	"""connect to all of the functions that collects data about the games and organize the data.
	:param tables: all of the tables in the page.
	:type tables: bs4 element
	"""
	games = [{'name': 'samorai_c', 'ranks': []},
			{'name': 'python_slayer', 'ranks': []},
			{'name': 'coffee_makers', 'ranks': []}]

	*_, samorai_c, python_slayer, coffee_makers, _, _, _, _, _= tables

	for i, game_name in enumerate([samorai_c, python_slayer, coffee_makers]):
		games[i]['ranks'] = import_games(game_name)

def import_games(table) -> list:
	"""Gets all the games of beta and the first 3 rankes.
	:param table: the context to be analyzed.
	:type table: bs4 element
	:return: game table with the name of it and first 3 ranks.
	:rtype: list

	"""
	ranks = list()

	for row in table.find_all('tr')[1:4]:
		*_, title, _, image = row.find_all('td')

		title = title.text.replace('\n', '')
		image = image.a.img['src']
		
		r = requests.get('https:' + image)

		download_image(r.content, title)

		ranks.append(dict({'title': title, 'image': r.content}))
	
	return ranks


def import_challenges_organize(tables, challenges: list):
	for table in range(TABLE_OFFSET, LAST_CHALLENGES_TABLE):
		if table != USELESS_TABLE_1 and table != USELESS_TABLE_2:
			challenges[table - TABLE_OFFSET - (table > USELESS_TABLE_1) - (table > USELESS_TABLE_2)]['challenges'] = import_challenges(tables[table])

	for challenge in challenges:
		write_content("challenges_tables\\" + challenge['table_name'], challenge['challenges'])


def import_challenges_table_name(soup) -> list:
	"""Gets the challenges names from the page (c, python, java... etc)
	:param soup: all of the page in 'lxml' format.
	:type soup: bs4 element
	:return: list of the challenges names
	:rtype: list
	"""
	div_tags = soup.find_all('div', class_="mw-content-ltr")

	for div_tag in div_tags:
		li_tags = div_tag.find_all('li', class_="toclevel-1 tocsection-54")

		for li_tag in li_tags:
			challenges_table_names = [challenge_name.text for challenge_name in li_tag.find_all('span', class_="toctext")[1:]]

			break
	challenges_table_names = [{'table_name': challenges_table_names[i], 'challenges': []} for i in range(len(challenges_table_names))]
	 
	return challenges_table_names


def import_challenges(table) -> list:
	"""Gets the challenges of each category from the page (c, python, java... etc)
	:param table: each table is a new category.
	:type table: bs4 element
	:return: list of the challenges of each category
	:rtype: list
	"""
	challenges  = list()

	for row in table.tbody.find_all('tr')[1:]:
		challenge_name, points, _, discription, _, dl = row.find_all('td')

		dl = dl.text.replace('\n', '')
		
		if dl == '':
			dl = '-'

		challenges.append(dict({'challenge_name': challenge_name.text.replace('\n', ''), 
								'points': points.text.replace('\n', ''),
								'discription': discription.text.replace('\n', ''),
								'deadline': dl}))

	return challenges


def solved_challenges_table_organize():
	"""connects to all of the functions that collects data on the solved challenges table an organize
		 the data.
	"""
	solved_challenges = list()
	second_page_url = 'https://beta.wikiversity.org/wiki/User:The_duke/solved_beta_challenges'
	
	soup = soup_site(second_page_url)
	tables = soup.find_all('table')
	heads = soup.find_all('h3')

	table_names = [table_name.text.replace('[edit]', '') for table_name in heads if '[edit]' in table_name.text]

	for table_name in range(len(table_names)):
		challenges_and_solvers = import_solved_challenges(tables[table_name])
		solved_challenges.append({'subject': table_names[table_name], 'challenges': challenges_and_solvers})

	write_content('solved_challenges.txt', str(solved_challenges))


def import_solved_challenges(table) -> list:
	"""Gets the solved challenges and their solvers.
	:param table: the context to be analyzed (isnt the same as the previous ones).
	:type table: bs4 element
	:return: challenges name and its solvers.
	:rtype: list
	"""
	solved_challenges_table = list()

	for row in table.find_all('tr')[1:]:
		challenge_name, solvers = row.find_all('td')
		challenge_name = challenge_name.text.replace('\n', '')
		solvers = solvers.text.replace('\n', '').split('* ')[1:]
		solved_challenges_table.append(dict({'challenge_name': challenge_name, 'solvers': solvers}))

	return solved_challenges_table


def get_pwn_game(table, game_name: str) -> dict:
    ninja_games_ranks = list()

    for row in table.find_all('tr')[1:]:
        try:
            _, image, *_ = row.find_all('td')

            title = image.a['title']
            image_url = 'https:' + image.img['src']
        
            r = requests.get(image_url)

            download_image(r.content, title)

            ninja_games_ranks.append(dict({'title': title, 'image': r.content}))
        except TypeError:
            continue


def main():
	main_page_url = "https://beta.wikiversity.org/wiki/%D7%9C%D7%99%D7%9E%D7%95%D7%93%D7%99_%D7%9E%D7%97%D7%A9%D7%91%D7%99%D7%9D_%D7%91%D7%A9%D7%99%D7%98%D7%AA_%D7%91%D7%98%D7%90"
	
	soup = soup_site(main_page_url)
	main_tables = soup.find_all('table', class_="wikitable sortable")
	challenges_tables = soup.find_all('table', class_="wikitable")

	challenges = import_challenges_table_name(soup)
	users_tables_organize(main_tables)
	games_tables_organize(main_tables)
	solved_challenges_table_organize()
	import_challenges_organize(challenges_tables, challenges)
	get_pwn_game(main_tables[PWN_GAME_TABLE_INDEX], 'Game_of_Pwns')


if __name__ == '__main__':
	main()
