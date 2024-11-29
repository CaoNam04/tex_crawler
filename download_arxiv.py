import requests

# Replace with your desired arXiv paper ID
arxiv_id = "2010.11644"
url = f"https://arxiv.org/e-print/{arxiv_id}"

response = requests.get(url)
with open(f"{arxiv_id}.tar.gz", 'wb') as f:
    f.write(response.content)
