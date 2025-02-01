import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


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

output_dir = "ChampionBuildHTMLSelenium"
os.makedirs(output_dir, exist_ok=True)


for champion in champions:
  try:
      # Set up Selenium
      driver = webdriver.Chrome()
      champion_lower= champion.lower()
      # Load the page
      driver.get(f'https://mobalytics.gg/lol/champions/{champion_lower}/build/')
      wait = WebDriverWait(driver, 6) 
      element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "m-ku03qt")))
      html = driver.page_source

      with open(f'./ChampionBuildHTMLSelenium/{champion}.html', 'w', encoding='utf-8') as f:
        f.write(html)
        print(f"Saved HTML for {champion}")
      driver.quit()
      time.sleep(2)

  except Exception as e:
    print(f"Error fetching {champion}: {e}")

