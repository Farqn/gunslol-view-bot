import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# Proxy listesini çeken fonksiyon
def get_proxies():
    print("\n[+] Yeni proxy listesi çekiliyor...")
    url = "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            # Proxy'leri bir listeye çeviriyoruz
            proxies = response.text.splitlines()
            print(f"[!] {len(proxies)} adet proxy alındı.")
            return proxies
    except Exception as e:
        print(f"Proxy çekilirken hata: {e}")
    return []

def view_bot(username, proxy):
    target_url = f"https://guns.lol/{username}"
    
    options = webdriver.ChromeOptions()
    options.add_argument(f'--proxy-server={proxy}')
    # options.add_argument("--headless") # Ekranın açılmasını istemiyorsan bunu aç
    
    # Hızlı çalışması için görselleri yüklememe ayarı (opsiyonel)
    options.add_argument('--blink-settings=imagesEnabled=false')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    # Sayfa yüklenme süresini sınırla (Proxy yavaşsa takılmasın)
    driver.set_page_load_timeout(20) 

    try:
        print(f"[*] Proxy kullanılıyor: {proxy}")
        driver.get(target_url)
        time.sleep(5) # İzlenmenin sayılması için bekleme
        print(f"[✓] {username} başarıyla ziyaret edildi.")
    except Exception as e:
        print(f"[X] Bağlantı başarısız (Proxy çalışmıyor olabilir): {proxy}")
    finally:
        driver.quit()

if __name__ == "__main__":
    print("=== Guns.lol Gelişmiş İzlenme Botu ===")
    kullanici_adi = input("Hedef kullanıcı adı: ")
    
    while True:
        proxy_listesi = get_proxies()
        
        if not proxy_listesi:
            print("Proxy listesi alınamadı, 1 dakika sonra tekrar denenecek.")
            time.sleep(60)
            continue

        start_time = time.time()
        
        # Proxy listesindeki her proxy için döngü
        for proxy in proxy_listesi:
            # Eğer 5 dakika (300 saniye) geçtiyse listeyi güncellemek için döngüden çık
            if time.time() - start_time > 300:
                print("\n[!] 5 dakika doldu, liste yenileniyor...")
                break
            
            view_bot(kullanici_adi, proxy)
            # Siteyi koruma mekanizmalarına takılmamak için kısa bir ara
            time.sleep(2)