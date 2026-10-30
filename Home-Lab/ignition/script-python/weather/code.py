apiKey = system.secrets.readSecretValue('Default','openWeather').getSecretAsString()
fiveDayUrl = 'https://api.openweathermap.org/data/2.5/forecast?lat=YOUR_LAT&lon=YOUR_LON&appid={}&units=imperial'.format(apiKey)
hourlyReportUrl = 'https://api.openweathermap.org/data/2.5/weather?lat=YOUR_LAT&lon=YOUR_LON&appid={}&units=imperial'.format(apiKey)

def weatherReport(url,tagPath):
	response = API.httpGet(url)
	if 200 <= response['code'] <= 299:
		system.tag.writeBlocking(tagPath, response['json'])
	return response
def getCurrentWeather():
	weatherReport(hourlyReportUrl,'[default]openWeather/hourlyWeather')
def getFiveDay():
	weatherReport(fiveDayUrl,'[default]openWeather/fiveDayReport')
