let videosIndexesGlobal
let defaultThumbnail = "nude1.jpg"

function openVideo(videoID){
	let MainHolder = document.getElementById("MainHolder")
	let videoTitle = videosIndexesGlobal[videoID]["title"]
	let videoFileName = videosIndexesGlobal[videoID]["fileLocation"]
	if (window.location.pathname+window.location.search+window.location.hash !== window.location.pathname+`?v=${videoID}`+window.location.hash){
		history.pushState({file:videoFileName}, null, `?v=${videoID}`)
	}
	let videoThumbnail = videosIndexesGlobal[videoID]["thumbnail"]
	MainHolder.innerHTML = ""
	let singleVideoHolder = document.createElement("div")
	let VideoFrame = document.createElement("video")
	VideoFrame.src = videoFileName
	VideoFrame.setAttribute("controls", "")
	singleVideoHolder.appendChild(VideoFrame)
	MainHolder.appendChild(singleVideoHolder)
}

function loadHome(videosIndexes){
	videosIndexesGlobal = videosIndexes
	videosIndexKeys = Object.keys(videosIndexes)
	let MainHolder = document.getElementById("MainHolder")
	MainHolder.innerHTML = ""
	for (let i1=videosIndexKeys.length-1; i1>=0;i1--){
		let videoID = videosIndexKeys[i1]
		let videoFileName = videosIndexes[videoID]["fileLocation"]
		let videoTitle = videosIndexes[videoID]["title"]
		let videoThumbnail = videosIndexes[videoID]["thumbnail"]

		let videoBox = document.createElement("button")
		videoBox.className = "videoBox"
		let thumbnailObject = document.createElement("img")
		thumbnailObject.setAttribute("src", videoThumbnail)
		thumbnailObject.onerror = function (){
			thumbnailObject.setAttribute("src", defaultThumbnail)
		}
		let titleObject = document.createElement("p")
		titleObject.textContent = videoTitle
		videoBox.appendChild(thumbnailObject)
		videoBox.appendChild(titleObject)
		videoBox.setAttribute("onClick", `openVideo("${videoID}")`)
		MainHolder.appendChild(videoBox)
		MainHolder.appendChild(document.createElement("br"))
	}
}

async function main(videosIndexes) {
	let params = new URLSearchParams(window.location.search)
	if (params.size === 0){
		loadHome(videosIndexes)
	}
	else{
		const response = await fetch("videosIndex.json")
		videosIndexesGlobal = await response.json()
		openVideo(params.get("v"))
	}
	window.onpopstate = (event) => {
		main(videosIndexesGlobal)
	}
}

fetch("videosIndex.json")
	.then(response => { return response.json() })
	.then( data => main(data))
