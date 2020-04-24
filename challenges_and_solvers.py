import requests
from bs4 import BeautifulSoup

def write_content(path: str, content: dict):
	with open(path, 'w') as file:
		file.write(str(content))

def solved_challenges(table):
	creators_and_solvers = {}
	result = list()

	for row in table.find_all('tr'):
		lst = list()
		cells = row.find_all('td')

		for cell in range(0, len(cells), 2):
			creators_and_solvers.update({cells[cell].text.replace('\n', ''):cells[cell - 1].text.replace('\n', '')})

	return creators_and_solvers


def main():
	url = 'https://beta.wikiversity.org/wiki/User:The_duke/solved_beta_challenges'
	r = requests.get(url)

	src = r.text
	soup = BeautifulSoup(src, 'lxml')
	tables = soup.find_all('table')


	i = 0
	for i in range(len(tables)):
		path = '/home/itay5245/table' + str(i)
		write_content(path, solved_challenges(tables[i]))


if __name__ == '__main__':
	main()