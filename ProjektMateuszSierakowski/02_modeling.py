"""
KROK 2: MODELOWANIE I PORÓWNANIE ALGORYTMÓW
Realizuje punkt II projektu - 5 algorytmów z różnych grup:
  1. Regresja liniowa        (algorytm bazowy / regresyjny)
  2. Drzewo decyzyjne        (Decision Tree)
  3. Las losowy              (Random Forest)
  4. Gradient Boosting       (algorytm boostingowy)
  5. Prosta sieć neuronowa   (MLP - jedna warstwa ukryta)

Dla każdego modelu mierzymy: MAE, RMSE, R2 oraz czas trenowania i predykcji.
"""

import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

OUT = "outputs"
sns.set_style("whitegrid")

# ----------------------------------------------------------------------
# 1. WCZYTANIE PRZETWORZONYCH DANYCH
# ----------------------------------------------------------------------
X_train = pd.read_csv(f"{OUT}/X_train.csv")
X_val = pd.read_csv(f"{OUT}/X_val.csv")
X_test = pd.read_csv(f"{OUT}/X_test.csv")
y_train = pd.read_csv(f"{OUT}/y_train.csv").squeeze()
y_val = pd.read_csv(f"{OUT}/y_val.csv").squeeze()
y_test = pd.read_csv(f"{OUT}/y_test.csv").squeeze()

# do trenowania finalnych modeli łączymy train+val (walidacja posłużyła
# wcześniej do strojenia hiperparametrów / wyboru modelu)
X_trainval = pd.concat([X_train, X_val])
y_trainval = pd.concat([y_train, y_val])

print(f"Zbiór treningowy+walidacyjny: {X_trainval.shape}, testowy: {X_test.shape}")

# ----------------------------------------------------------------------
# 2. DEFINICJA MODELI (5 algorytmów z różnych grup)
# ----------------------------------------------------------------------
models = {
    "Regresja liniowa (bazowy)": LinearRegression(),
    "Drzewo decyzyjne": DecisionTreeRegressor(max_depth=5, random_state=42),
    "Las losowy": RandomForestRegressor(n_estimators=300, max_depth=8, random_state=42),
    "Gradient Boosting": GradientBoostingRegressor(n_estimators=300, max_depth=3,
                                                     learning_rate=0.05, random_state=42),
    "Sieć neuronowa (MLP)": MLPRegressor(hidden_layer_sizes=(32, 16), max_iter=2000,
                                           random_state=42, early_stopping=True),
}

# ----------------------------------------------------------------------
# 3. TRENOWANIE I EWALUACJA
# ----------------------------------------------------------------------
results = []
predictions = {}

for name, model in models.items():
    t0 = time.perf_counter()
    model.fit(X_trainval, y_trainval)
    train_time = time.perf_counter() - t0

    t0 = time.perf_counter()
    y_pred = model.predict(X_test)
    pred_time = time.perf_counter() - t0

    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)

    results.append({
        "Model": name,
        "MAE": round(mae, 3),
        "RMSE": round(rmse, 3),
        "R2": round(r2, 3),
        "Czas treningu [s]": round(train_time, 4),
        "Czas predykcji [s]": round(pred_time, 5),
    })
    predictions[name] = y_pred
    print(f"{name:30s} | MAE={mae:.3f}  RMSE={rmse:.3f}  R2={r2:.3f}  "
          f"czas_treningu={train_time:.3f}s")

results_df = pd.DataFrame(results).sort_values("R2", ascending=False).reset_index(drop=True)
print("\n=== TABELA WYNIKÓW (posortowana wg R2) ===")
print(results_df.to_string(index=False))
results_df.to_csv(f"{OUT}/model_comparison.csv", index=False)

best_model = results_df.iloc[0]["Model"]
print(f"\nNajlepszy model na tym zbiorze danych: {best_model}")

# ----------------------------------------------------------------------
# 4. WYKRESY PORÓWNAWCZE
# ----------------------------------------------------------------------
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

sns.barplot(data=results_df, x="R2", y="Model", ax=axes[0], color="#4C72B0")
axes[0].set_title("Porównanie modeli - R² (im wyżej tym lepiej)")

sns.barplot(data=results_df, x="RMSE", y="Model", ax=axes[1], color="#C44E52")
axes[1].set_title("Porównanie modeli - RMSE (im niżej tym lepiej)")

sns.barplot(data=results_df, x="Czas treningu [s]", y="Model", ax=axes[2], color="#55A868")
axes[2].set_title("Czas trenowania modelu [s]")
axes[2].set_xscale("log")

plt.tight_layout()
plt.savefig(f"{OUT}/04_model_comparison.png", dpi=120)
plt.close()

# wykres: predykcje vs. wartości rzeczywiste dla najlepszego modelu
plt.figure(figsize=(6, 6))
plt.scatter(y_test, predictions[best_model], alpha=0.6, color="#4C72B0")
plt.plot([0, 20], [0, 20], "r--", label="idealna predykcja")
plt.xlabel("G3 rzeczywiste")
plt.ylabel("G3 przewidziane")
plt.title(f"Predykcje vs rzeczywistość - {best_model}")
plt.legend()
plt.tight_layout()
plt.savefig(f"{OUT}/05_best_model_predictions.png", dpi=120)
plt.close()

print(f"\nWykresy i tabela wyników zapisane w '{OUT}/'.")
