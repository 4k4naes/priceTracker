import json
import os
import pandas as pd
import schedule
import time
from datetime import datetime
from stores.mediaExpert import get_price_mediaexpert
from stores.mediaMarkt import get_price_mediamarkt

PRODUCTS_FILE = "data/products.json"
CSV_PATH = "data/prices.csv"

def load_products():
    if not os.path.exists(PRODUCTS_FILE):
        return []
    with open(PRODUCTS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_products(products):
    with open(PRODUCTS_FILE, "w", encoding="utf-8") as f:
        json.dump(products, f, indent=2, ensure_ascii=False)

#########################################################################

def get_price(store, url):
    if store.lower() == "media expert":
        return get_price_mediaexpert(url)
    elif store.lower() == "media markt":
        return get_price_mediamarkt(url)
    else:
        return None

def track_prices():
    products = load_products()
    if not products:
        print("Brak produktów do śledzenia.")
        return

    records = []
    for p in products:
        price = get_price(p["store"], p["url"])
        if price:
            print(f"[{p['store']}] {p['name']} → {price} zł")
            records.append({
                "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "product": p["name"],
                "store": p["store"],
                "price": price
            })
        else:
            print(f"[BŁĄD] Nie udało się pobrać ceny dla {p['name']}")

    if records:
        df = pd.DataFrame(records)
        df.to_csv(CSV_PATH, mode="a", header=not os.path.exists(CSV_PATH), index=False, encoding="utf-8")
        print("Zapisano dane do CSV.\n")

####################################################################### MENU
def add_product():
    name = input("Nazwa produktu: ").strip()
    store = input("Sklep (Media Expert / Media Markt): ").strip()
    url = input("URL produktu: ").strip()

    price = get_price(store, url)
    if not price:
        print("cena", price)
        print("Nie udało się pobrać ceny. Sprawdź poprawność linku.")
        return

    products = load_products()
    products.append({"name": name, "store": store, "url": url})
    save_products(products)
    print(f"Dodano {name} ({store}) – aktualna cena: {price} zł")

def list_products():
    products = load_products()
    if not products:
        print("Brak produktów na liście.")
        return
    print("\n--- ŚLEDZONE PRODUKTY ---")
    for i, p in enumerate(products, 1):
        print(f"{i}. {p['name']} ({p['store']})")
    print("---------------------------\n")

def remove_product():
    products = load_products()
    if not products:
        print("Brak produktów na liście.")
        return

    list_products()
    try:
        index = int(input("Podaj numer produktu do usunięcia: ")) - 1
        removed = products.pop(index)
        save_products(products)
        print(f"Usunięto: {removed['name']} ({removed['store']})")
    except (ValueError, IndexError):
        print("Niepoprawny numer.")



def run_scheduler():
    schedule.every(6).hours.do(track_prices)
    print("Harmonogram uruchomiony – sprawdzanie cen co 6h.\n")
    while True:
        schedule.run_pending()
        time.sleep(60)

def main_menu():
    while True:
        print("""
========= PRICE TRACKER =========
1. Dodaj produkt do śledzenia
2. Lista produktów
3. Usuń produkt z listy
4. Ręcznie sprawdź ceny teraz
5. Uruchom automatyczne śledzenie (co 6h)
0. Wyjdź
=================================
""")
        choice = input("Wybierz opcję: ").strip()

        if choice == "1":
            add_product()
        elif choice == "2":
            list_products()
        elif choice == "3":
            remove_product()
        elif choice == "4":
            track_prices()
        elif choice == "5":
            run_scheduler()
        elif choice == "0":
            break
        else:
            print("Niepoprawna opcja.\n")

if __name__ == "__main__":
    main_menu()
