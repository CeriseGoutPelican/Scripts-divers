"""Permet de vérifier si un cabinet inscrit au registre de la transparence a communiqué sur un sujet particulier.

L'ensemble du script a besoin du registre de la transparence au format .csv (UTF-8) et d'une clé d'API Bing.

Author:
	Grégoire

Date:
	Avril 2021

See:
	Bing API : https://www.microsoft.com/en-us/bing/apis/bing-web-search-api
	Dataset du registre : https://data.europa.eu/euodp/en/data/dataset/transparency-register
"""

"""Dépendances
"""
try:
	import re
	import glob
	import os.path
	import sys
	import xml.etree.ElementTree as ET
	import requests
	import csv
except ImportError:
    sys.exit("""⚠️ Certains des bibliothèques ne sont pas correctement installées. \nVérifiez la partie 'Dépendances' du programme.\n\n""")

"""Paramètres d'entrée

Sous formes de constantes
"""
# Le dataset du registre de la transparence
REGISTER_XML = "full_export_new.xml"
# Namespace
REGISTER_NAMESPACE = "http://intragate.ec.europa.eu/transparencyregister/intws/20200626"
# Mot clé de la recherche à effectuer dans le registre de la transparence
COLUMN_KEYWORD = "Digital economy and society"
# Mot clé à vérifier sur le moteur de recherche
SEARCH_KEYWORD = "Digital Decade"
# Fichier à exporter
EXPORT_FILE = "final_analytic.csv"
# Bing API
BING_API = ""

"""Affichage des variables
"""
def display_constants():
	print("    REGISTER_XML       = " + REGISTER_XML)
	print("    REGISTER_NAMESPACE = " + REGISTER_NAMESPACE)
	print("    COLUMN_KEYWORD     = " + COLUMN_KEYWORD)
	print("    SEARCH_KEYWORD     = " + SEARCH_KEYWORD)
	print("    EXPORT_FILE        = " + EXPORT_FILE)
	print("    BING_API           = " + len(BING_API)*'*')

def bing_search(search_term):
	headers = {"Ocp-Apim-Subscription-Key": BING_API}
	params = {"q": search_term, "textDecorations": True, "textFormat": "HTML"}
	response = requests.get("https://api.bing.microsoft.com/v7.0/search", headers=headers, params=params)
	response.raise_for_status()
	return response.json()

"""Programme principal
"""
def main():
	# Affichage des paramètres
	print("Lancement du programme, affichage des paramètres : ")
	display_constants()
	print("\n\n")

	# Ouverture du registre
	print("Ouverture du registre... (habituellement entre 3 et 10 secondes)")

	try:
		register_tree = ET.parse(REGISTER_XML)
		register_root = register_tree.getroot()
	except:
		sys.exit("""⚠️ Impossible d'ouvrir le registre. \n\n""")

	# CSV
	with open(EXPORT_FILE, 'w', newline='') as file:
		writer = csv.writer(file)
		writer.writerow(["website", "results"])

		# Recherche dans le registre
		ns = {'ns': REGISTER_NAMESPACE}
		for interest in register_tree.findall('.//*[.="'+COLUMN_KEYWORD+'"]../../../ns:webSiteURL', namespaces=ns):
			website = interest.attrib['{http://www.w3.org/1999/xlink}href']

			# Recherche Bing
			try:
				results = bing_search('site:'+website+' "'+SEARCH_KEYWORD+'"')

				if "webPages" in results:
					total = str(results['webPages']['totalEstimatedMatches'])
				else:
					total = "0"

			except:

				total = "ERROR"

			print(website + " : " + total)
			writer.writerow([website, total])

	print("Terminé... Export effectué dans : " + EXPORT_FILE)

if __name__ == "__main__":
	main()

