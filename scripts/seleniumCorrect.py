from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up Selenium
driver = webdriver.Chrome()
champions = [   "Poppy" ,"Zed" ]

for ch in champions:
  chL=ch.lower()    
  # Load the page
  driver.get(f'https://mobalytics.gg/lol/champions/{chL}/build/')
  wait = WebDriverWait(driver, 10)  # Adjust timeout if necessar
  element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "m-ku03qt")))


  # Get rendered HTML
  html = driver.page_source

  with open(f'./ChampionBuildHTML/{ch}.html', 'w', encoding='utf-8') as f:
    f.write(html)

driver.quit()
