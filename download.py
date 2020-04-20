def get_users(start_char1, start_char2, file_path:
	with open(file_path, 'w') as file:
		for char in range(len(file)):
			if page[char] == start_char1 and page[char + 1] == start_char2:
				start_of_table_index = letter
				break
	for char in range(len(page) - 1, 0, -1):
		if page[char] == end_char1 and page[char - 1] == end_char2:
			end_of_table_index = letter
			break

	table = 














def import_and_slice(section, start_char1, start_char2, end_char1, end_char2, path):
	r = requests.get(url, 'r')

	page = r.content
	page = page.decode()															# changes type from bytes to string

	for letter in range(len(page)):
		if page[letter] == start_char1 and page[letter + 1] == start_char2:			# gets the start of the desired table
			start_of_table_index = letter
			break


	for letter in range(len(page) - 1, 0, -1):
		if page[letter] == end_char1 and page[letter - 1] == end_char2:				# gets the end of the desired table
			end_of_table_index = letter
			break


	page = page[start_of_table_index:end_of_table_index]							# inputs the table to page


	with open(path, 'w') as file:
		file.write(page)

url = "https://beta.wikiversity.org/w/index.php?title=%D7%9C%D7%99%D7%9E%D7%95%D7%93%D7%99_%D7%9E%D7%97%D7%A9%D7%91%D7%99%D7%9D_%D7%91%D7%A9%D7%99%D7%98%D7%AA_%D7%91%D7%98%D7%90&action=edit&section=" + section
import_and_slice(14, '{', '|', '}', '|', /home/itay5245/page_import)
