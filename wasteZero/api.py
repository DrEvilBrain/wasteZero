import requests
from configparser import ConfigParser
import os

def apiCall(image):
	# grabs current file directory
	curr_dir = os.path.dirname(__file__)

	# grabs API key from config.ini
	config = ConfigParser()
	config.read(curr_dir + "/config.ini")
	API_KEY = config.get("API", "key")
	
	# checks to use URL or locally stored image as determined by config file
	imageIsURL = config.getboolean("DEBUG", "use_url")
	if(imageIsURL):
		# use image URL to call Microsoft Computer Vision API from mashape
		response = requests.post("https://microsoft-azure-microsoft-computer-vision-v1.p.mashape.com/describe",
			headers={
				"X-Mashape-Key": API_KEY,
				"Content-Type": "application/json",
				"Accept": "application/json"
			},
			json=(
				{"url": image}
			)
		)
	else:
		# open image
		with open(image, mode="rb") as f:
			img_data = f.read()
	
		# use stored image to call Microsoft Computer Vision API from mashape
		response = requests.post("https://microsoft-azure-microsoft-computer-vision-v1.p.mashape.com/describe",
			headers={
				"X-Mashape-Key": API_KEY,
				"Content-Type": "application/octet-stream",
				"Accept": "application/json"
			},
			data=img_data
		)
	
	status_code = response.status_code
	print(status_code)
	json = response.json()
	print(json)
	tags = json["description"]["tags"]
	caption = json["description"]["captions"][0]["text"]
	confidence = json["description"]["captions"][0]["confidence"]
	
	return status_code, json, tags, caption, confidence