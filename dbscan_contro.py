import numpy as np
import matplotlib.pyplot as plt

from sklearn.datasets import load_svmlight_file
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import DBSCAN
from collections import Counter

# ================================================================
# 1. CARICAMENTO DEL FILE TXT IN FORMATO SPARSE (libsvm-like)
# ================================================================

file_path = r"C:\Users\Sofia\Downloads\percezioni\audio_volume_stream.txt"

print("Carico il file sparse:", file_path)

# X_sparse: matrice sparse (n_istanze x n_feature)
# y: etichette di classe (i numeri prima dei "1:0.0024 ...")
X_sparse, y = load_svmlight_file(file_path)

print("Shape completa (righe, feature):", X_sparse.shape)

# ================================================================
# 2. CAMPIONAMENTO: usiamo solo un sottoinsieme di righe
#    per non far esplodere il PC
# ================================================================

N_ROWS = 2000

n_samples = X_sparse.shape[0]
if n_samples > N_ROWS:
    rng = np.random.default_rng(42)  # per riproducibilità
    idx = rng.choice(n_samples, size=N_ROWS, replace=False)
    X_sparse_sample = X_sparse[idx]
    y_sample = y[idx]
else:
    X_sparse_sample = X_sparse
    y_sample = y

print("Shape campione (righe, feature):", X_sparse_sample.shape)

# Convertiamo il campione da sparse → denso
X = X_sparse_sample.toarray()

# ================================================================
# 3. STANDARDIZZAZIONE
# ================================================================

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# ================================================================
# 4. PCA: riduciamo a 3 componenti per visualizzare + DBSCAN
# ================================================================

pca = PCA(n_components=3)
X_pca = pca.fit_transform(X_scaled)

var_spiegata = pca.explained_variance_ratio_.sum()
print(f"Varianza spiegata dalle 3 componenti PCA: {var_spiegata:.2%}")

# ================================================================
# 5. DBSCAN (qui vogliamo far vedere che NON è l’algoritmo ideale)
# ================================================================

dbscan = DBSCAN(
    eps=0.5,
    min_samples=10,
    metric="euclidean",
    n_jobs=-1
)

labels = dbscan.fit_predict(X_pca)

print("\nDistribuzione cluster trovati (label -1 = rumore):")
print(Counter(labels))

# ================================================================
# 6A. ISTOGRAMMA / GRAFICO A BARRE DEI CLUSTER TROVATI
# ================================================================

# Conteggio delle label (incluso rumore -1)
label_counts = Counter(labels)
print("\nConteggio label (per istogramma):", label_counts)

# Ordino le label per asse X
unique_labels = sorted(label_counts.keys())
counts = [label_counts[lab] for lab in unique_labels]

plt.figure(figsize=(8, 5))
plt.bar([str(lab) for lab in unique_labels], counts)
plt.xlabel("Label cluster (DBSCAN) - (-1 = rumore)")
plt.ylabel("Numero di punti")
plt.title("Istogramma dei cluster trovati da DBSCAN")
plt.tight_layout()
plt.show()

# ================================================================
# 6B. SCATTER 2D (prime 2 componenti PCA)
# ================================================================

x1 = X_pca[:, 0]
x2 = X_pca[:, 1]

plt.figure(figsize=(10, 8))

for lab in unique_labels:
    mask = (labels == lab)
    if lab == -1:
        plt.scatter(
            x1[mask], x2[mask],
            marker="x", s=30,
            label="Rumore (-1)"
        )
    else:
        plt.scatter(
            x1[mask], x2[mask],
            s=40, alpha=0.7,
            label=f"Cluster {lab}"
        )

plt.xlabel("PCA 1")
plt.ylabel("PCA 2")
plt.title("DBSCAN su file audio_volume_stream (PCA 2D)")
plt.legend()
plt.tight_layout()
plt.show()