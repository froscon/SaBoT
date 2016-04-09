import requests
from django.conf import settings

class SmskaufenException(Exception):
	pass

SMSKAUFEN_RETURN_VALS = {
	112 : "Invalid Authentication",
	123 : "No Reciepient detected",
}

def sendLetter(letterFile, color=False, noDuplex=None, email=None, feedUrl=None, international=False):
	API_URL = "https://www.smskaufen.com/sms/post/postin.php"

	if color == True:
		color = "f"

	params = {
		"id" : settings.SMSKAUFEN_UID,
		"apikey" : settings.SMSKAUFEN_APIKEY,
		"art" : "b", # type "b"rief / letter
		"mode" : "1", # test 1 or live 0
		"color" : color,
	}
	if noDuplex != None:
		params["duplexaus"] = "1"
	if feedUrl != None:
		params["feed"] = feedUrl
	if email != None:
		params["email"] = email
	if international == True:
		params["ausland"] = "1"
		params["luftpost"] = "1"

	files = {
		"document" : letterFile
	}



	r = requests.post(API_URL, data=params, files=files, verify=True)
	if r.status_code != 200:
		raise SmskaufenException("API Failure. HTTP request returned with code {}. Message: {}".format(r.status_code,r.text))
	if int(r.text) < 200:
		error_code = int(r.text)
		error_message = SMSKAUFEN_RETURN_VALS.get(error_code, "unknown error code " + r.text)

		raise SmskaufenException("API returned error \"{}\"".format(error_message))

	return int(r.text)

