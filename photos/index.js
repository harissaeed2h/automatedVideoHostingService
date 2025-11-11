var mainDiv = document.getElementById("mainDiv")
var jsonData

async function loadJson() {
	const response = await fetch("../imagesIndex.json")
	const data = await response.json()
	return data
}

async function openPhoto(fileHash) {
	if (window.location.search != `?${fileHash}`){
		history.pushState(null, null, `?file=${fileHash}`)
	}
	displaySearchImage()
}

async function main(){
	mainDiv.innerHTML = ""
	jsonData = await loadJson()
	for (let i1 = Object.keys(jsonData).length-1; i1>=0; i1--){
		var imageHolderButton = document.createElement("button")
		var ImageDiv = document.createElement("img")
		var imagesKeys = Object.keys(jsonData)
		ImageDiv.src = jsonData[imagesKeys[i1]]["fileLocation"]
		imageHolderButton.appendChild(ImageDiv)
		imageHolderButton.setAttribute("onClick", `openPhoto("${imagesKeys[i1]}")`)
		mainDiv.appendChild(imageHolderButton)
		//mainDiv.appendChild(document.createElement("br"))
	}
	window.onpopstate = (event) => {
		main()
	}
}

async function displaySearchImage(){
	jsonData = await loadJson()
	var imageHolder = document.createElement("img")
	const searchParameters = new URLSearchParams(window.location.search)
	fileHash = searchParameters.get("file")
	imageHolder.src = jsonData[fileHash]["fileLocation"]
	mainDiv.innerHTML = ""
	mainDiv.appendChild(imageHolder)
}

if (window.location.search == ""){
	main()
}
else{
	displaySearchImage()
}