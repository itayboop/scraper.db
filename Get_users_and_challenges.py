import requests
from bs4 import BeautifulSoup

cells = []
result = requests.get("https://beta.wikiversity.org/wiki/%D7%9C%D7%99%D7%9E%D7%95%D7%93%D7%99_%D7%9E%D7%97%D7%A9%D7%91%D7%99%D7%9D_%D7%91%D7%A9%D7%99%D7%98%D7%AA_%D7%91%D7%98%D7%90")

src = result.content

soup = BeautifulSoup(src, 'lxml')
tables = soup.findChildren('table')

my_table = tables[19]


rows = my_table.findChildren(['tr'])

i = 0
for row in rows[1:]:
	cells.append([])
	row = row.find_all('td')
	cells[i].append(row[0]) 
	cells[i].append(row[1]) 
	cells[i].append(row[3])
	i += 1


for cell in range(len(cells)):
	cells[cell] = str(cells[cell]).replace('<td>', '')
	cells[cell] = str(cells[cell]).replace('</td>', '')
	cells[cell] = cells[cell].split('\n')
	cells[cell] = str(cells[cell]).replace("'[", '')
	cells[cell] = str(cells[cell]).replace("]'", '')
	cells[cell] = str(cells[cell]).replace("', '", '')

print(cells[9])
