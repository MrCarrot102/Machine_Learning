"""
KROK 1: DATA PREPROCESSING
Dataset: Student Performance (Math) - UCI / Kaggle "Student Alcohol Consumption"
Zadanie: regresja - przewidywanie końcowej oceny ucznia (G3, skala 0-20)

Ten skrypt realizuje punkt I projektu:
- wczytanie danych
- sprawdzenie duplikatów i braków danych
- analiza rozkładu zmiennej wynikowej (G3)
- korelacja (heatmapa)
- rozkład cech (histogramy)
- kodowanie zmiennych kategorycznych
- skalowanie (StandardScaler)
- podział na zbiór treningowy / walidacyjny / testowy
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
import os

OUT = "outputs"
os.makedirs(OUT, exist_ok=True)
sns.set_style("whitegrid")

# ----------------------------------------------------------------------
# 1. WCZYTANIE DANYCH
# ----------------------------------------------------------------------
df = pd.read_csv("student-mat.csv", sep=";")
print(f"Wczytano dane: {df.shape[0]} wierszy, {df.shape[1]} kolumn")
print(df.head())

# Ograniczamy zbiór do 30 kolumn (mieści się w wymaganym zakresie 10-30).
# Usuwamy kolumny o najmniejszej wartości analitycznej / silnie skorelowane
# z innymi cechami (guardian dubluje informacje z Pstatus/famsize,
# nursery i romantic mają marginalny wpływ na ocenę końcową).
df = df.drop(columns=["guardian", "nursery", "romantic"])
print(f"\nPo redukcji kolumn: {df.shape[1]} kolumn")
print(df.columns.tolist())

# ----------------------------------------------------------------------
# 2. DUPLIKATY I BRAKI DANYCH
# ----------------------------------------------------------------------
n_dupl = df.duplicated().sum()
print(f"\nLiczba duplikatów: {n_dupl}")
if n_dupl > 0:
    df = df.drop_duplicates()
    print(f"Usunięto duplikaty. Nowy rozmiar: {df.shape}")

missing = df.isna().sum()
missing = missing[missing > 0]
print(f"\nBraki danych (kolumny z brakami):\n{missing if len(missing) else 'BRAK BRAKÓW DANYCH'}")

if len(missing) > 0:
    for col in missing.index:
        frac_missing = df[col].isna().mean()
        if frac_missing < 0.05:
            # mało braków -> usuwamy wiersze
            df = df.dropna(subset=[col])
        else:
            # dużo braków -> uzupełniamy (mediana dla liczb, moda dla kategorii)
            if df[col].dtype in [np.float64, np.int64]:
                df[col] = df[col].fillna(df[col].median())
            else:
                df[col] = df[col].fillna(df[col].mode()[0])
    print(f"Po obsłudze braków: {df.shape}")
else:
    print("Zbiór nie zawiera braków danych - krok pominięty (ale kod gotowy na wypadek innych danych).")

# ----------------------------------------------------------------------
# 3. ANALIZA ROZKŁADU ZMIENNEJ WYNIKOWEJ (G3)
# ----------------------------------------------------------------------
plt.figure(figsize=(7, 5))
sns.histplot(df["G3"], bins=21, kde=True, color="#4C72B0")
plt.title("Rozkład zmiennej wynikowej G3 (ocena końcowa, 0-20)")
plt.xlabel("G3")
plt.ylabel("Liczba uczniów")
plt.tight_layout()
plt.savefig(f"{OUT}/01_target_distribution.png", dpi=120)
plt.close()
print(f"\nStatystyki G3:\n{df['G3'].describe()}")
print(f"Liczba uczniów z G3 = 0 (brak zdania / wypadnięcie): {(df['G3']==0).sum()}")

# ----------------------------------------------------------------------
# 4. HISTOGRAMY WYBRANYCH CECH LICZBOWYCH
# ----------------------------------------------------------------------
num_cols_preview = ["age", "absences", "studytime", "failures", "G1", "G2", "G3"]
fig, axes = plt.subplots(2, 4, figsize=(18, 8))
for ax, col in zip(axes.flat, num_cols_preview):
    sns.histplot(df[col], bins=15, ax=ax, color="#55A868")
    ax.set_title(col)
axes.flat[-1].axis("off")
plt.tight_layout()
plt.savefig(f"{OUT}/02_feature_histograms.png", dpi=120)
plt.close()

# ----------------------------------------------------------------------
# 5. KODOWANIE ZMIENNYCH KATEGORYCZNYCH
# ----------------------------------------------------------------------
binary_cols = ["school", "sex", "address", "famsize", "Pstatus",
                "schoolsup", "famsup", "paid", "activities", "higher", "internet"]
multi_cat_cols = ["Mjob", "Fjob", "reason"]

df_enc = df.copy()

# Label encoding dla zmiennych binarnych (2 kategorie -> 0/1)
le = LabelEncoder()
for col in binary_cols:
    df_enc[col] = le.fit_transform(df_enc[col])

# One-hot encoding dla zmiennych wielowartościowych
df_enc = pd.get_dummies(df_enc, columns=multi_cat_cols, drop_first=True)

print(f"\nPo kodowaniu zmiennych kategorycznych: {df_enc.shape[1]} kolumn")

# ----------------------------------------------------------------------
# 6. KORELACJA - HEATMAPA
# ----------------------------------------------------------------------
plt.figure(figsize=(16, 13))
corr = df_enc.corr(numeric_only=True)
sns.heatmap(corr, cmap="coolwarm", center=0, annot=False, linewidths=0.3)
plt.title("Macierz korelacji cech (po kodowaniu)")
plt.tight_layout()
plt.savefig(f"{OUT}/03_correlation_heatmap.png", dpi=120)
plt.close()

print("\nNajsilniejsze korelacje z G3:")
print(corr["G3"].sort_values(ascending=False).head(8))
print(corr["G3"].sort_values().head(5))

# ----------------------------------------------------------------------
# 7. PODZIAŁ NA X / y ORAZ TRAIN / VAL / TEST
# ----------------------------------------------------------------------
X = df_enc.drop(columns=["G3"])
y = df_enc["G3"]

# 60% trening / 20% walidacja / 20% test
X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.4, random_state=42)
X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)

print(f"\nPodział zbioru:")
print(f"  treningowy: {X_train.shape[0]} ({X_train.shape[0]/len(X):.0%})")
print(f"  walidacyjny: {X_val.shape[0]} ({X_val.shape[0]/len(X):.0%})")
print(f"  testowy: {X_test.shape[0]} ({X_test.shape[0]/len(X):.0%})")

# ----------------------------------------------------------------------
# 8. SKALOWANIE (StandardScaler) - dopasowany TYLKO na zbiorze treningowym
# ----------------------------------------------------------------------
scaler = StandardScaler()
X_train_scaled = pd.DataFrame(scaler.fit_transform(X_train), columns=X_train.columns, index=X_train.index)
X_val_scaled = pd.DataFrame(scaler.transform(X_val), columns=X_val.columns, index=X_val.index)
X_test_scaled = pd.DataFrame(scaler.transform(X_test), columns=X_test.columns, index=X_test.index)

# ----------------------------------------------------------------------
# 9. ZAPIS PRZETWORZONYCH DANYCH
# ----------------------------------------------------------------------
X_train_scaled.to_csv(f"{OUT}/X_train.csv", index=False)
X_val_scaled.to_csv(f"{OUT}/X_val.csv", index=False)
X_test_scaled.to_csv(f"{OUT}/X_test.csv", index=False)
y_train.to_csv(f"{OUT}/y_train.csv", index=False)
y_val.to_csv(f"{OUT}/y_val.csv", index=False)
y_test.to_csv(f"{OUT}/y_test.csv", index=False)

print(f"\nPreprocessing zakończony. Pliki wynikowe zapisano w '{OUT}/'.")
