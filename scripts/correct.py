import requests as rq
import os
import time

champions = [ "Akshan", "Annie", "BelVeth", "DrMundo", "Galio", "Gangplank","Janna","Jinx", "Karthus", "Malzahar", "MasterYi", "Neeko","Orianna", "Poppy", "Renata", "Skarner", "TwistedFate", "Yone" ,"Zed", "Ziggs" ]

for ch in champions:
  os.remove(f'./ChampionBuildHTML/{ch}.html')

'''
output_dir = "ChampionBuildHTML"
os.makedirs(output_dir, exist_ok=True)


for champion in champions:
    try:
        champion_lower= champion.lower()
        response = rq.get(f'https://mobalytics.gg/lol/champions/{champion_lower}/build/')

        if response.status_code == 200:
            file_path = os.path.join(output_dir, f"{champion}.html")
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(response.text)
            print(f"Saved HTML for {champion}")
        else:
            print(f"Failed to fetch {champion}: Status code {response.status_code}")
    except Exception as e:
        print(f"Error fetching {champion}: {e}")
'''