def httpGet(url):
	client = system.net.httpClient()
	response = client.get(url)
	code = response.statusCode
	json = response.getJson()
	return {'code': code,
			'json':json}
	