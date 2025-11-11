from concurrent.futures import ThreadPoolExecutor, as_completed
import subprocess
import os, shutil

def worker_function(link):
	print(f"Downloading {link}")
	subprocess.run(["yt-dlp", "--no-playlist", "-o", "/home/haris/downloads/%(title)s.%(ext)s", link, "-N", "4"])  # Adjust the command as needed

def run_tasks_concurrently(data_list, max_workers):
	with ThreadPoolExecutor(max_workers=max_workers) as executor:
		# Submit tasks and create a mapping of futures to links
		futures = {executor.submit(worker_function, link): link for link in data_list}
		
		# Process results as they complete
		for future in as_completed(futures):
			link = futures[future]  # Get the corresponding link
			try:
				future.result()  # Wait for the future to complete and get the result
				print(f"Successfully downloaded: {link}")
			except Exception as exc:
				print(f"Error downloading {link}: {exc}")

if __name__ == "__main__":
	with open("links.txt", "r") as f:
		# Read and clean the links from the file
		data_list = f.read().replace("\n\n", "\n").splitlines()  # Use splitlines() for cleaner splitting
		run_tasks_concurrently(data_list, max_workers=2)
	for file in os.listdir("/home/haris/downloads/"):
		shutil.move(f"/home/haris/downloads/{file}", "/var/www/html/server/videos/")
