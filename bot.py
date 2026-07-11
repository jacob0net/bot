import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Ziel-Schule: Jakob-Fugger-Gymnasium Augsburg
URL = "https://antenne.de"
INTERVALL = 61  # Sekunden Wartezeit zwischen den Klicks

print("🤖 Online-Cloud-Bot gestartet.")
print("Hinweis: Hält automatisch die offizielle Nachtruhe zwischen 22:00 und 06:00 Uhr ein.")

try:
    while True:
        # Aktuelle Stunde prüfen für die Nachtpause
        aktuelle_stunde = datetime.now().hour
        
        # Nachtruhe-Prüfung (22:00 Uhr abends bis 06:00 Uhr morgens)
        if aktuelle_stunde >= 22 or aktuelle_stunde < 6:
            jetzt = datetime.now()
            morgen_06 = jetzt.replace(hour=6, minute=0, second=0, microsecond=0)
            if aktuelle_stunde >= 22:
                from datetime import timedelta
                morgen_06 += timedelta(days=1)
            schlaf_zeit = int((morgen_06 - jetzt).total_seconds())
            
            print(f"🌙 [{time.strftime('%H:%M:%S')}] Offizielle Voting-Pause.")
            print(f"😴 Cloud-Server schläft für {schlaf_zeit // 3600} Stunden bis 06:00 Uhr...")
            time.sleep(schlaf_zeit)
            continue
            
        print(f"\n🚀 [{time.strftime('%H:%M:%S')}] Öffne Browser in der Cloud...")
        
        # Cloud-Optimierte Einstellungen für Google Chrome
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # Wichtig: Macht den Browser in der Cloud unsichtbar
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--incognito")  # Startet jedes Mal ohne alte Cookies
        
        driver = webdriver.Chrome(options=options)
        
        try:
            # 1. Webseite laden
            driver.get(URL)
            time.sleep(6)  # Wartezeit für den vollständigen Seitenaufbau
            
            # 2. Cookie-Banner automatisch entfernen
            try:
                cookie_knopf = WebDriverWait(driver, 8).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Akzeptieren') or contains(., 'Zustimmen') or contains(., 'Zulassen') or contains(., 'Alles erlauben') or contains(., 'Einverstanden')]"))
                )
                cookie_knopf.click()
                print("🍪 Cookie-Banner automatisch weggedrückt.")
                time.sleep(2)
            except Exception:
                print("ℹ️ Cookie-Banner nicht gefunden oder blockiert nicht.")
            
            # 3. Den Abstimm-Button klicken
            knopf = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Jetzt abstimmen')]"))
            )
            knopf.click()
            print("🎉 Erfolgreich abgestimmt für das Jakob-Fugger-Gymnasium!")
            time.sleep(2)
            
        except Exception as e:
            print("❌ Fehler beim Klicken. (Möglicherweise Voting-Knopf im Moment ausgeblendet)")
        
        # Browser sauber schließen, um Arbeitsspeicher zu sparen
        driver.quit()
        time.sleep(INTERVALL)

except KeyboardInterrupt:
    print("\n🛑 Cloud-Bot gestoppt.")
