import pandas as pd
import numpy as np

# Ustawienie ziarna losowości, aby wyniki były powtarzalne
np.random.seed(42)

# Liczba rekordów (od 300 do 1000)
n_records = 800

# Generowanie cech (od 10 do 30)
data = {
    'Wiek': np.random.randint(18, 70, n_records),
    'Dochod_Miesieczny_PLN': np.random.normal(6000, 2000, n_records).round(2),
    'Kwota_Kredytu_PLN': np.random.randint(10000, 500000, n_records),
    'Okres_Kredytowania_Miesiace': np.random.choice([12, 24, 36, 48, 60, 120, 240, 360], n_records),
    'Liczba_Dzieci': np.random.randint(0, 4, n_records),
    'Staz_Pracy_Lata': np.random.randint(0, 35, n_records),
    'Ocena_BIK': np.random.randint(300, 850, n_records), # Skoring kredytowy
    'Wklad_Wlasny_Procent': np.random.uniform(0.0, 0.4, n_records).round(2),
    'Liczba_Spóźnionych_Rat': np.random.randint(0, 5, n_records),
    'Wydatki_Stale_PLN': np.random.normal(2500, 1000, n_records).round(2),
    'Karta_Kredytowa': np.random.choice([0, 1], n_records) # 0 - nie, 1 - tak
}

df = pd.DataFrame(data)

# Korekta nierealistycznych wartości (np. ujemne dochody)
df['Dochod_Miesieczny_PLN'] = df['Dochod_Miesieczny_PLN'].apply(lambda x: max(x, 2000))
df['Wydatki_Stale_PLN'] = df['Wydatki_Stale_PLN'].apply(lambda x: max(x, 500))

# TWORZENIE ZMIENNEJ DOCELOWEJ (Target) do klasyfikacji: "Czy_Splaci_Kredyt"
# Budujemy logikę, na której model będzie mógł się uczyć:
# Wyższy dochód, wyższa ocena BIK i większy wkład własny = większa szansa na spłatę
prawdopodobienstwo = (
    (df['Dochod_Miesieczny_PLN'] / 10000) * 1.5 + 
    (df['Ocena_BIK'] / 850) * 2.0 - 
    (df['Kwota_Kredytu_PLN'] / 500000) * 1.2 -
    (df['Liczba_Spóźnionych_Rat'] * 0.3)
)

# Dodajemy trochę szumu (random noise), żeby zadanie nie było dla modelu w 100% trywialne
szum = np.random.normal(0, 0.5, n_records)
df['Czy_Splaci_Kredyt'] = (prawdopodobienstwo + szum > 1.5).astype(int)

# Zapis do pliku CSV
df.to_csv('dane_ryzyko_kredytowe.csv', index=False)
print("Pomyślnie wygenerowano plik 'dane_ryzyko_kredytowe.csv' z", n_records, "rekordami.")