import json
from serpapi.google_search import GoogleSearch

# Running this script will correctly scrape google images into a json file, but it will consume a search with the API key

api_key = "meow"

params = {
  "q": "Scizor",
  "engine": "google_images",
  "ijn": "0",
  "safe": "active",
  "nfpr": "1",
  "api_key": api_key
}

with open("scizor_res.json","w") as f:
    search = GoogleSearch(params)
    results = search.get_dict()
    images_results = results["images_results"]
    f.write(json.dumps(images_results))

