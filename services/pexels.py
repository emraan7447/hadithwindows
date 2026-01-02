import requests, random, os

def fetch_background(api_key, out):
    headers = {"Authorization": api_key}
    q = random.choice(["mosque","islamic","prayer","sky","nature"])
    r = requests.get(
        f"https://api.pexels.com/videos/search?query={q}&orientation=portrait&size=small",
        headers=headers
    ).json()
    video = random.choice(r["videos"])
    url = video["video_files"][0]["link"]
    data = requests.get(url).content
    with open(out, "wb") as f:
        f.write(data)
