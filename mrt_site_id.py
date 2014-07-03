import requests
from bs4 import BeautifulSoup
import json
import re

response = requests.get('http://web.trtc.com.tw/c/index_ticket_price.asp')
response.encoding = 'utf-8'
soup = BeautifulSoup(response.text)

#print soup.prettify().encode('utf-8')
root = soup.find('select')
output = []
for line in root.find_all('optgroup'):
	line_name = line['label'].encode('utf-8')
	#print line_name
	for station in line.find_all('option'):
		temp = {}
		temp['id'] = station['value']
		temp['name'] = station.get_text().encode('utf-8')
		temp['line'] = line_name
		post_data = {'ID':temp['id']}
		response = requests.get('http://web.trtc.com.tw/c/stationdetail2010.asp',data=post_data)
		response.encoding = 'utf-8'
		station_soup = BeautifulSoup(response.text)
		for link in station_soup.find_all('a'):
			if link['href'].startswith('googlemap.asp'):
				pattern = re.compile(u'>(.+?)<')
				address = pattern.findall(str(link.find_parent('td').find('font')))
				#print address
				temp['address'] = ','.join(address)
				co = link['href'].split("?")[1].split("&")
				for val in co:
					if val.lower().startswith("latitude"):
						temp['lat'] = float(val.split("=")[1])
					elif val.lower().startswith("longitude"):
						temp['lng'] = float(val.split("=")[1])
				break
		output.append(temp)
		#print station['value'] + station.get_text().encode('utf-8')
print json.dumps(output)
