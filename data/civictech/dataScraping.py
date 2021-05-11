import requests
from bs4 import BeautifulSoup
import csv
import time
import random
from fake_useragent import UserAgent

# Configuration
# =============
CSV_INPUT  = "civictechguide.csv"
CSV_OUTPUT = "data_civictech.csv"

# Fonctions
# =========

""" Permet de retirer tout code html d'une chaine de carractères
	
	:param raw_html: "<div>test</div>"
	:type raw_html: string

	:return: "test"
	:rtype: string
"""
def strip_tags(raw_html):
	return str(BeautifulSoup(str(raw_html), "lxml").text)

""" Permet de lire un fichier csv avec un encodage UTF-8
	La partie Titre/URL sont à adapter selon le type de données

	:param file: "file.csv"
	:type file: srting

	:return: liste de liste contenant l'ensenble des colonnes pertinentes [["titre", 10], ["titre 2", 15]]
	:rtype: list
"""
def reading_csv(file):
	with open(file, newline='', encoding='utf-8') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		i = 0

		rows = []

		for row in csv_reader:

			if i == 0:
				i += 1

			else:

				# Titre
				name = row[3]

				print(str(i) + '. ' + name)

				# URL à scrap
				url = row[6]

				# Scraping des pages
				scraped_data = scrap_html_page(url)
				rows.append([name, scraped_data[0], scraped_data[1]])

				time.sleep(random.uniform(1, 8))

				i += 1

		return rows

""" Permet de générer un fichier csv
	
	:input file_input: "file.csv"
	:type file_input: string
	:input file_output: "file2.csv"
	:type file_output: string

	:return: true
	:rtype: bool
"""
def creating_csv(file_input, file_output):
	fields = ['Nom du projet', 'Date de première création', 'Catégories']
	rows = reading_csv(file_input)

	with open(file_output, 'w', encoding='utf-8') as csv_file: 
		csvwriter = csv.writer(csv_file) 
		csvwriter.writerow(fields) 
		csvwriter.writerows(rows)

	return true

""" Permet de récupérer le contenu d'une page HTML distante en se faisant passer pour un véritable utilisateur

	:input url: "http://google.com/"
	:type url: string

	:return: les données pertinentes sous forme d'une liste (a, b, c)
	:rtype: list
"""
def scrap_html_page(url):
	
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
	ua = UserAgent()
	hdr = {'User-Agent': ua.random,
	      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	      'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
	      'Accept-Encoding': 'none',
	      'Accept-Language': 'en-US,en;q=0.8',
	      'Connection': 'keep-alive'}

	page = requests.get(url, headers=hdr)
	soup = BeautifulSoup(page.content, 'html.parser')

	# Publication date
	try:
		publication_date = soup.select('#vitals > div:nth-child(2) > div:nth-child(2)')
		publication_date = strip_tags(publication_date[0])
	except:
		publication_date = ""

	# Categories
	try:
		categories = soup.select('.list-categories-div > a')
		categories_list = ""
		for category in categories:
			categories_list += strip_tags(category)
	except:
		categories = ""
		print("---------------> Possibilité de blocage")

	return publication_date, categories_list

# Début du programme
# ==================
# -> Récupération des données issues de la cartographie
# -> Scraping de toutes les pages citées
# -> Création d'un nouveau fichier csv avec l'ensemble des données
print('start')
creating_csv(CSV_INPUT, CSV_OUTPUT)
print('end')
