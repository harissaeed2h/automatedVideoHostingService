import json

with open("../videosIndex") as file:
	fileData = json.load(file)

for fileIndex in fileData.keys():
	if not fileData[fileIndex]["fileLocation"]: