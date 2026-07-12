# Projekt ML: Przewidywanie ocen uczniów (Student Performance)

## 1. Zbiór danych
- Źródło: UCI / Kaggle "Student Alcohol Consumption" (student-mat.csv) - Paulo Cortez, Uniwersytet w Minho
- **395 rekordów, 30 kolumn** (po redukcji z 33 - usunięto `guardian`, `nursery`, `romantic`)
- Problem: **regresja** - przewidzenie końcowej oceny ucznia `G3` (skala 0-20) na podstawie cech demograficznych, społecznych i edukacyjnych
- Zbiór mieszany: zmienne liczbowe (wiek, absencje, czas nauki...) + kategoryczne (płeć, zawód rodziców, powód wyboru szkoły...)

## 2. Preprocessing (`01_preprocessing.py`)
1. Wczytanie danych, podgląd struktury
2. Sprawdzenie duplikatów → **0 duplikatów**
3. Sprawdzenie braków danych → **0 braków** (kod obsługuje oba przypadki: usuwanie przy małej liczbie braków, imputacja medianą/modą przy dużej)
4. Analiza rozkładu zmiennej `G3` (histogram) - rozkład zbliżony do normalnego, z grupą **38 uczniów z G3=0** (wypadnięcie z egzaminu)
5. Histogramy wybranych cech liczbowych
6. Kodowanie zmiennych kategorycznych:
   - Label Encoding dla zmiennych binarnych (płeć, szkoła, internet itd.)
   - One-Hot Encoding dla zmiennych wielowartościowych (zawód matki/ojca, powód wyboru szkoły)
7. Heatmapa korelacji - najsilniejsze skorelowane z G3: `G2` (0.90), `G1` (0.80), `failures` (-0.36)
8. Podział: **60% trening / 20% walidacja / 20% test**
9. Standaryzacja (`StandardScaler`) dopasowana wyłącznie na zbiorze treningowym

## 3. Modelowanie (`02_modeling.py`) - 5 algorytmów z różnych grup

| Model | Grupa | MAE | RMSE | R² | Czas treningu [s] |
|---|---|---|---|---|---|
| **Las losowy** | Ensemble (bagging) | 1.281 | 2.129 | **0.819** | 0.427 |
| Gradient Boosting | Ensemble (boosting) | 1.392 | 2.158 | 0.814 | 0.199 |
| Regresja liniowa | Bazowy / regresyjny | 1.583 | 2.457 | 0.759 | 0.005 |
| Drzewo decyzyjne | Drzewa | 1.460 | 2.848 | 0.676 | 0.003 |
| Sieć neuronowa (MLP) | Neural network | 2.438 | 3.316 | 0.561 | 0.262 |

## 4. Wnioski
- **Las losowy** osiągnął najlepszy wynik (R²=0.82) - dobrze radzi sobie z mieszanką cech liczbowych/kategorycznych i nieliniowymi zależnościami, bez ryzyka przeuczenia jak pojedyncze drzewo.
- Gradient Boosting blisko za nim, przy krótszym czasie treningu - dobry kompromis jakość/czas.
- Regresja liniowa jako baseline wypada zaskakująco dobrze (R²=0.76) - sugeruje, że zależności są w dużej mierze liniowe (zwłaszcza dzięki silnie skorelowanym G1/G2).
- Pojedyncze drzewo decyzyjne przeucza się mocniej niż las losowy → niższy wynik.
- Sieć neuronowa (MLP) wypadła najsłabiej - przy tak małym zbiorze (316 obserwacji treningowych) prosta sieć ma za mało danych, by w pełni wykorzystać swoją elastyczność; wymagałaby więcej danych lub silniejszej regularyzacji.
- **Rekomendacja**: dla tego problemu i rozmiaru danych najlepiej sprawdza się Las losowy lub Gradient Boosting.

## 5. Pliki w projekcie
- `student-mat.csv` - oryginalny zbiór danych
- `01_preprocessing.py` - preprocessing + EDA
- `02_modeling.py` - trenowanie i porównanie modeli
- `outputs/` - wykresy (rozkład G3, histogramy, heatmapa korelacji, porównanie modeli, predykcje) oraz przetworzone dane (train/val/test) i tabela wyników
