import requests as rq
import os
import time

champions = [
    "Aatrox", "Ahri", "Akali", "Akshan", "Alistar", "Amumu", "Anivia", "Annie", 
    "Aphelios", "Ashe", "AurelionSol", "Azir", "Bard", "BelVeth", "Blitzcrank", 
    "Brand", "Braum", "Briar", "Caitlyn", "Camille", "Cassiopeia", "ChoGath", 
    "Corki", "Darius", "Diana", "DrMundo", "Draven", "Ekko", "Elise", "Evelynn", 
    "Ezreal", "Fiddlesticks", "Fiora", "Fizz", "Galio", "Gangplank", "Garen", 
    "Gnar", "Gragas", "Graves", "Gwen", "Hecarim", "Heimerdinger", "Hwei", 
    "Illaoi", "Irelia", "Ivern", "Janna", "JarvanIV", "Jax", "Jayce", "Jhin", 
    "Jinx", "KaiSa", "Kalista", "Karma", "Karthus", "Kassadin", "Katarina", 
    "Kayle", "Kayn", "Kennen", "KhaZix", "Kindred", "Kled", "KogMaw", 
    "LeBlanc", "LeeSin", "Leona", "Lillia", "Lissandra", "Lucian", "Lulu", 
    "Lux", "Malphite", "Malzahar", "Maokai", "MasterYi", "Milio", "MissFortune", 
    "Mordekaiser", "Morgana", "Naafiri", "Nami", "Nasus", "Nautilus", "Neeko", 
    "Nidalee", "Nilah", "Nocturne", "Nunu", "Olaf", "Orianna", "Ornn", 
    "Pantheon", "Poppy", "Pyke", "Qiyana", "Quinn", "Rakan", "Rammus", "RekSai", 
    "Rell", "Renata", "Renekton", "Rengar", "Riven", "Rumble", "Ryze", 
    "Samira", "Sejuani", "Senna", "Seraphine", "Sett", "Shaco", "Shen", "Shyvana", 
    "Singed", "Sion", "Sivir", "Skarner", "Sona", "Soraka", "Swain", "Sylas", 
    "Syndra", "TahmKench", "Taliyah", "Talon", "Taric", "Teemo", "Thresh", 
    "Tristana", "Trundle", "Tryndamere", "TwistedFate", "Twitch", "Udyr", 
    "Urgot", "Varus", "Vayne", "Veigar", "VelKoz", "Vex", "Vi", "Viego", 
    "Viktor", "Vladimir", "Volibear", "Warwick", "Monkeyking", "Xayah", "Xerath", 
    "XinZhao", "Yasuo", "Yone", "Yorick", "Yuumi", "Zac", "Zed", "Zeri", 
    "Ziggs", "Zilean", "Zoe", "Zyra","Smolder","Aurora", "Ambessa"
]

output_dir = "ChampionBuildHTML"
os.makedirs(output_dir, exist_ok=True)


for champion in champions:
    try:
        champion_lower= champion.lower()
        response = rq.get(f'https://mobalytics.gg/lol/champions/{champion_lower}/build')
        time.sleep(2)
        if response.status_code == 200:
            file_path = os.path.join(output_dir, f"{champion}.html")
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(response.text)
            print(f"Saved HTML for {champion}")
        else:
            print(f"Failed to fetch {champion}: Status code {response.status_code}")
    except Exception as e:
        print(f"Error fetching {champion}: {e}")