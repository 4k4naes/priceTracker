#Price Tracker

Prosty bot w Pythonie do monitorowania cen produktów z Media Expert i Media Markt.
Pozwala dodawać, usuwać i wyświetlać śledzone produkty przez menu w konsoli.
Wyniki zapisuje do data/prices.csv, a produkty trzyma w data/products.json.
Automatycznie odświeża ceny co 6 godzin.

## Instalacja

```
git clone https://github.com/twoj-nick/price-tracker.git

cd price-tracker
pip install -r requirements.txt
playwright install
```
## Użycie

```bash
python main.py
```
## Menu:

1. Dodaj produkt

3. Lista produktów

5. Usuń produkt

7. Sprawdź ceny teraz

9. Automatyczne śledzenie (co 6h)

11. Wyjdź

## Dane

Śledzone produkty: data/products.json
Historia cen: data/prices.csv

Przykład rekordu:
datetime: 2025-10-07 12:30:15
product: PS5 Slim
store: Media Markt
price: 2849.00

## Struktura projektu

price_tracker/
├── main.py
├── stores/
│ ├── mediaExpert.py
│ ├── mediaMarkt.py
├── data/
│ ├── prices.csv
│ └── products.json
├── requirements.txt
└── README.md
