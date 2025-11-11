import os, json, hashlib, subprocess

def videosSetup():
	def makeThumbnail(v,o="thumb.jpg"):#ChatGPT made this Function-modded a lot by me
		existingThumbnailFiles = [f"../thumbnails/{fn}" for fn in os.listdir("../thumbnails/")]
		if o in existingThumbnailFiles:
			return
		else:
			d = json.loads(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","json",f"../videos/{v}"],capture_output=True,text=True).stdout)
			d = float(d["format"]["duration"])/2
			subprocess.run(["ffmpeg","-ss",str(int(d)),"-i",f"../videos/{v}","-frames:v","1",o,"-y"])

	videoFiles = os.listdir("../videos/")
	thumbnailFiles = [(".".join(videoFile.split(".")[:-1]))+".jpg" for videoFile in videoFiles]

	with open("../videosIndex.json", "r") as f:
		indexDict = json.load(f)
	for i1,videoFile in enumerate(videoFiles):
		videoID = str(hashlib.md5(videoFile.encode()).hexdigest())
		if not videoID in indexDict.keys():
			indexDict[videoID] = {}
			indexDict[videoID]["fileLocation"] = f"videos/{videoFile}"
			indexDict[videoID]["title"] = thumbnailFiles[i1].replace(".jpg", "")
			indexDict[videoID]["thumbnail"] = f"thumbnails/{thumbnailFiles[i1]}"

	filesInVideosDir = os.listdir("../videos")
	indexDictTemp = indexDict
	filesInIndexDict = list(indexDict.keys())
	for file in filesInIndexDict:
		if not indexDict[file]["fileLocation"][7:] in filesInVideosDir:
			del indexDictTemp[file]
	indexDict = indexDictTemp

	with open("../videosIndex.json", "w") as f:
		json.dump(indexDict, f,indent=4)


	for i1,videoFile in enumerate(videoFiles):
		makeThumbnail(videoFile, f"../thumbnails/{thumbnailFiles[i1]}")

def picturesSetup():
	baseLocation = "../images"
	pictureFiles = os.listdir(baseLocation)
	imageExtensions = [".png", ".jpg", ".jpeg", ".webp"]
	try:
		with open("../imagesIndex.json") as f:
			picturesJson = json.load(f)
	except:
		picturesJson = {}

	for pictureFile in pictureFiles:
		PictureTitle = pictureFile
		for extension in imageExtensions:
			PictureTitle.replace(extension, "")
		picturesJson[hashlib.md5(pictureFile.encode()).hexdigest()] = {"fileLocation":f"{baseLocation}/{pictureFile}", "title":f"{PictureTitle}"}

	with open("../imagesIndex.json", "w") as f:
		print("making file")
		json.dump(picturesJson, f, indent=4)

videosSetup()
picturesSetup()