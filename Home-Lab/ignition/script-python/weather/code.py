apiKey = system.secrets.readSecretValue('Default','openWeather').getSecretAsString()
reportUrl = 'https://api.openweathermap.org/data/2.5/{}?lat={}&lon={}&appid={}&units=imperial'
# The gateway's location lives in tags (gateway config), so it never ships with the project
locationTags = ['[default]openWeather/location/latitude', '[default]openWeather/location/longitude']
logger = system.util.getLogger('weather')

def getLocation():
	"""Returns (lat, lon) from the location tags, or None if they are unset or invalid."""
	values = system.tag.readBlocking(locationTags)
	if not all(v.quality.isGood() for v in values):
		logger.warn('Location tags are missing or bad quality: %s' % locationTags)
		return None
	lat, lon = [v.value for v in values]
	if lat is None or lon is None or (lat == 0 and lon == 0):
		logger.warn('Location not set; enter the gateway latitude/longitude in %s' % locationTags)
		return None
	if not (-90 <= lat <= 90 and -180 <= lon <= 180):
		logger.warn('Location out of range: lat=%s lon=%s' % (lat, lon))
		return None
	return lat, lon

def weatherReport(endpoint,tagPath):
	location = getLocation()
	if location is None:
		return None
	response = API.httpGet(reportUrl.format(endpoint, location[0], location[1], apiKey))
	if 200 <= response['code'] <= 299:
		system.tag.writeBlocking(tagPath, response['json'])
	return response
def getCurrentWeather():
	weatherReport('weather','[default]openWeather/hourlyWeather')
def getFiveDay():
	weatherReport('forecast','[default]openWeather/fiveDayReport')
