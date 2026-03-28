import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def get_proxies():
    """ProxyScrape API'den güncel proxy listesini çeker."""
    print("\n[+] Yeni proxy listesi çekiliyor...")
    # API URL: Sadece HTTP protokolünde ve hızlı yanıt verenleri çeker
    url = "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=5000&country=all&ssl=all&anonymity=all"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            proxies = response.text.splitlines()
            print(f"[!] {len(proxies)} adet potansiyel proxy alındı.")
            return proxies
    except Exception as e:
        print(f"[X] Proxy listesi alınırken hata oluştu: {e}")
    return []

def view_bot(username, proxy):
    """Belirtilen proxy ile hedef profili ziyaret eder."""
    target_url = f"https://guns.lol/{username}"
    
    options = webdriver.ChromeOptions()
    
    # Proxy formatını standartlaştırıyoruz (bazı proxylerde http:// eksik olabilir)
    if not proxy.startswith("http"):
        proxy_address = f"http://{proxy}"
    else:
        proxy_address = proxy

    options.add_argument(f'--proxy-server={proxy_address}')
    
    # --- Stabilite ve Hız Ayarları ---
    options.add_argument("--headless=new") # Arka planda çalışır (pencere açılmaz)
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--log-level=3") # Terminal kirliliğini engeller
    options.add_argument('--blink-settings=imagesEnabled=false') # Resimleri yüklemez (tasarruf)

    driver = None
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.set_page_load_timeout(15) # Yavaş proxylerde sonsuza kadar beklemez
        
        print(f"[*] Deneniyor: {proxy}")
        driver.get(target_url)
        
        # Sayfanın yüklenmesi ve izlenmenin sayılması için bekleme süresi
        time.sleep(8) 
        
        print(f"[✓] {username} başarıyla ziyaret edildi.")
    except Exception:
        # Ücretsiz proxylerin çoğu çalışmayacağı için hata detayını gizliyoruz
        print(f"[X] Başarısız: {proxy}")
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    print("========================================")
    print("   GUNS.LOL ADVANCED VIEW BOT v1.0")
    print("========================================")
    
    target_user = input("Hedef kullanıcı adını girin: ").strip()
    
    if not target_user:
        print("Geçersiz kullanıcı adı. Program kapatılıyor.")
    else:
        while True:
            proxy_list = get_proxies()
            
            if not proxy_list:
                print("Liste boş, 30 saniye sonra tekrar denenecek...")
                time.sleep(30)
                continue

            start_time = time.time()
            
            for p in proxy_list:
                # 5 dakika (300 saniye) dolduysa yeni liste çekmek için döngüyü kır
                if time.time() - start_time > 300:
                    print("\n[!] 5 dakika doldu. Liste tazeleniyor...")
                    break
                
                view_bot(target_user, p)
                
                # Sistem yorulmasın ve site tarafından engellenme riskini azaltmak için
                time.sleep(1)
