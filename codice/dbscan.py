import pandas as pd  # libreria per lavorare con dati tabellari: tabelle, colonne, righe, CSV, ecc.
from sklearn.preprocessing import StandardScaler  # porta ogni colonna a media 0 e deviazione standard 1
from sklearn.decomposition import PCA  # modulo con metodi di decomposizione / riduzione dimensionale.
from sklearn.cluster import DBSCAN  # prendo l'algoritmo e lo uso automaticamente
from collections import Counter  # serve per contare quanti punti ci sono in ogni cluster
import matplotlib.pyplot as plt  # serve per la visualizzazione

# ==========================================================
# 1. CARICAMENTO DEL DATASET
# ==========================================================

print("\n" + "=" * 70)
print("1) CARICAMENTO DEL DATASET")
print("=" * 70)

file_path = "sales_transactions.csv"
df = pd.read_csv(file_path, sep=",")

print("\nPrime righe del dataset:")
print(df.head())
print("\nColonne del dataset:")
print(df.columns)

# ==========================================================
# 2. SELEZIONE DELLE FEATURES: LE COLONNE SETTIMANALI
# ==========================================================

print("\n" + "=" * 70)
print("2) SELEZIONE DELLE FEATURES (COLONNE SETTIMANALI)")
print("=" * 70)

# Qui prendo tutte le colonne che iniziano con 'W'
weekly_cols = [c for c in df.columns if c.upper().startswith("W")]

if not weekly_cols:
    raise ValueError(
        "Non sono state trovate colonne settimanali che iniziano con 'W'.\n"
        "Controlla i nomi delle colonne nel dataset e modifica il filtro."
    )

X = df[weekly_cols].copy()

print(f"\nNumero di prodotti (righe): {X.shape[0]}")
print(f"Numero di settimane (colonne): {X.shape[1]}")

# Gestione eventuali valori mancanti: li sostituiamo con 0
X = X.fillna(0.0)

# ==========================================================
# 3. STANDARDIZZAZIONE
# ==========================================================

print("\n" + "=" * 70)
print("3) STANDARDIZZAZIONE DELLE FEATURES")
print("=" * 70)

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

print("\nStandardizzazione completata (media ~0, varianza ~1 per ogni colonna).")

# ==========================================================
# 4. RIDUZIONE DIMENSIONALE CON PCA
# ==========================================================

print("\n" + "=" * 70)
print("4) RIDUZIONE DIMENSIONALE CON PCA")
print("=" * 70)

# Qui scelgo 3 componenti principali
pca = PCA(n_components=3)
X_pca = pca.fit_transform(X_scaled)

explained = pca.explained_variance_ratio_.sum()
print(f"\nVarianza spiegata totale dalle 3 componenti PCA: {explained:.2%}")

# ==========================================================
# 5. APPLICAZIONE DI DBSCAN, Obiettivo: trovare gruppi di prodotti con pattern # di vendita settimanale simili e rilevare prodotti outlier.
# ==========================================================

print("\n" + "=" * 70)
print("5) APPLICAZIONE DI DBSCAN")
print("=" * 70)

dbscan = DBSCAN(
    eps=0.8,       # raggio di vicinanza
    min_samples=5, # numero minimo di vicini per formare un cluster
    metric="euclidean"
)

labels = dbscan.fit_predict(X_pca)  # alleno il modello e mi ritorna array di etichette (es. 0, 1, -1)

df["cluster_dbscan"] = labels  # aggiungo una colonna con le etichette

print("\nDistribuzione dei cluster trovati (label = -1 significa outlier):")
print(Counter(labels))  # conta come una mappa chiave->valore

# ==========================================================
# 6. PICCOLA INTERPRETAZIONE DEI CLUSTER (TESTO)
# ==========================================================

print("\n" + "=" * 70)
print("6) INTERPRETAZIONE DEI CLUSTER (PROFILI MEDI + CONTEGGI)")
print("=" * 70)

# Filtriamo i record che NON sono rumore
mask_valid = df["cluster_dbscan"] != -1
df_clusters = df[mask_valid].copy()  # faccio una copia per evitare warning

if df_clusters.empty:
    print("\nDBSCAN ha classificato tutti i prodotti come rumore (-1).")
else:
    # Raggruppo le righe per cluster e calcolo la media delle colonne settimanali
    cluster_profiles = df_clusters.groupby("cluster_dbscan")[weekly_cols].mean()

    print("\nProfilo medio di vendita per cluster (prime 5 settimane mostrate):")
    # Mostro solo le prime 5 colonne (settimane)
    print(cluster_profiles[weekly_cols[:5]])

    # Conto quanti prodotti ci sono in ogni cluster
    counts = df_clusters["cluster_dbscan"].value_counts().sort_index()
    print("\nNumero di prodotti per cluster (escludendo il rumore):")
    print(counts)

# ==========================================================
# 7. ESEMPIO DI USO: prodotti OUTLIER (TESTO)
# ==========================================================

print("\n" + "=" * 70)
print("7) OUTLIER TROVATI DA DBSCAN (LABEL = -1)")
print("=" * 70)

outliers = df[df["cluster_dbscan"] == -1]

print(f"\nNumero di prodotti identificati come outlier: {len(outliers)}")

if len(outliers) > 0:
    # Mostriamo qualche riga di esempio (mostro prime 5 settimane)
    cols_to_show = [c for c in df.columns if c not in weekly_cols] + weekly_cols[:5]
    print("\nEsempi di prodotti outlier (prime 5 righe):")
    print(outliers[cols_to_show].head())

# ==========================================================
# 8. VISUALIZZAZIONE GRAFICA DEI CLUSTER (PCA 2D - SCATTER)
# ==========================================================

print("\n" + "=" * 70)
print("8) GRAFICO SCATTER PCA 2D DEI CLUSTER (VISUALIZZAZIONE BASE)")
print("=" * 70)

# Usiamo solo le prime 2 componenti PCA per lo scatter plot
x_1 = X_pca[:, 0]
x_2 = X_pca[:, 1]

plt.figure(figsize=(10, 8))

unique_labels = sorted(set(labels))
for lab in unique_labels:
    mask = (labels == lab)
    if lab == -1:
        # Rumore / outlier
        plt.scatter(
            x_1[mask],
            x_2[mask],
            marker="x",
            s=40,
            label="Rumore (-1)"
        )
    else:
        # Cluster normali
        plt.scatter(
            x_1[mask],
            x_2[mask],
            s=60,
            alpha=0.7,
            label=f"Cluster {lab}"
        )

plt.xlabel("PCA 1")
plt.ylabel("PCA 2")
plt.title("DBSCAN sui prodotti (prime 2 componenti PCA)")
plt.legend()
plt.tight_layout()
plt.show()

# ==========================================================
# 9. GRAFICO A BARRE: NUMERO DI PRODOTTI PER CLUSTER
# ==========================================================

print("\n" + "=" * 70)
print("9) GRAFICO A BARRE: NUMERO DI PRODOTTI PER CLUSTER (INCLUSO RUMORE)")
print("=" * 70)

cluster_counts = df["cluster_dbscan"].value_counts().sort_index()

plt.figure(figsize=(8, 5))
cluster_counts.plot(kind="bar")

plt.xlabel("Cluster (label DBSCAN)")
plt.ylabel("Numero di prodotti")
plt.title("Numero di prodotti per cluster (incluso rumore -1)")
plt.tight_layout()
plt.show()

# ==========================================================
# 10. GRAFICO A BARRE: NUMERO DI PRODOTTI PER CLUSTER (SENZA RUMORE)
# ==========================================================

print("\n" + "=" * 70)
print("10) GRAFICO A BARRE: NUMERO DI PRODOTTI PER CLUSTER (SENZA RUMORE)")
print("=" * 70)

cluster_counts_no_noise = df[df["cluster_dbscan"] != -1]["cluster_dbscan"].value_counts().sort_index()

if cluster_counts_no_noise.empty:
    print("\nTutti i punti sono rumore: impossibile mostrare grafico senza rumore.")
else:
    plt.figure(figsize=(8, 5))
    cluster_counts_no_noise.plot(kind="bar")

    plt.xlabel("Cluster (label DBSCAN)")
    plt.ylabel("Numero di prodotti")
    plt.title("Numero di prodotti per cluster (escludendo il rumore)")
    plt.tight_layout()
    plt.show()

# ==========================================================
# 11. LINE PLOT: PROFILO MEDIO DELLE VENDITE PER CLUSTER
# ==========================================================

print("\n" + "=" * 70)
print("11) LINE PLOT: PROFILO MEDIO DELLE VENDITE PER CLUSTER")
print("=" * 70)

if df_clusters.empty:
    print("\nNessun cluster valido (tutti rumore), impossibile plottare i profili medi.")
else:
    plt.figure(figsize=(10, 6))

    for cluster_label, row in cluster_profiles.iterrows():
        plt.plot(
            range(len(weekly_cols)),
            row[weekly_cols],
            marker="o",
            label=f"Cluster {cluster_label}"
        )

    plt.xticks(range(len(weekly_cols)), weekly_cols, rotation=90)
    plt.xlabel("Settimana")
    plt.ylabel("Vendite medie")
    plt.title("Profilo medio delle vendite per cluster")
    plt.legend()
    plt.tight_layout()
    plt.show()

# ==========================================================
# 12. BOXPLOT: DISTRIBUZIONE DELLE VENDITE IN UNA SETTIMANA PER CLUSTER
# ==========================================================

print("\n" + "=" * 70)
print("12) BOXPLOT: DISTRIBUZIONE DELLE VENDITE (UNA SETTIMANA) PER CLUSTER")
print("=" * 70)

if df_clusters.empty:
    print("\nNessun cluster valido (tutti rumore), impossibile creare boxplot.")
else:
    # scelgo ad esempio la prima settimana
    week_col = weekly_cols[0]

    data_boxplot = []
    labels_boxplot = []

    for cl in sorted(df_clusters["cluster_dbscan"].unique()):
        vals = df_clusters[df_clusters["cluster_dbscan"] == cl][week_col]
        data_boxplot.append(vals.values)
        labels_boxplot.append(f"Cluster {cl}")

    plt.figure(figsize=(8, 6))
    plt.boxplot(data_boxplot, labels=labels_boxplot, showfliers=True)
    plt.xlabel("Cluster")
    plt.ylabel(f"Vendite ({week_col})")
    plt.title(f"Distribuzione delle vendite per cluster nella settimana {week_col}")
    plt.tight_layout()
    plt.show()

# ==========================================================
# 13. HEATMAP: VENDITE MEDIE PER CLUSTER E SETTIMANA
# ==========================================================

print("\n" + "=" * 70)
print("13) HEATMAP: VENDITE MEDIE PER CLUSTER E SETTIMANA")
print("=" * 70)

if df_clusters.empty:
    print("\nNessun cluster valido (tutti rumore), impossibile creare heatmap.")
else:
    # Se ci sono tante settimane, limito la visualizzazione (es. prime 10)
    max_weeks_to_show = 10
    weeks_to_show = weekly_cols[:max_weeks_to_show]

    heatmap_data = cluster_profiles[weeks_to_show].values

    plt.figure(figsize=(10, 6))
    plt.imshow(heatmap_data, aspect="auto")
    plt.colorbar(label="Vendite medie")

    plt.yticks(
        range(len(cluster_profiles.index)),
        [f"Cluster {cl}" for cl in cluster_profiles.index]
    )
    plt.xticks(range(len(weeks_to_show)), weeks_to_show, rotation=90)

    plt.xlabel("Settimana")
    plt.ylabel("Cluster")
    plt.title("Heatmap vendite medie per cluster e settimana")
    plt.tight_layout()
    plt.show()

# ==========================================================
# 14. STATISTICHE RIASSUNTIVE PER CLUSTER (TESTO)
# ==========================================================

print("\n" + "=" * 70)
print("14) STATISTICHE RIASSUNTIVE PER CLUSTER (VENDITE TOTALI)")
print("=" * 70)

if df_clusters.empty:
    print("\nNessun cluster valido, impossibile calcolare statistiche.")
else:
    # Somma totale vendite per prodotto (sommando tutte le settimane)
    df_clusters["total_sales"] = df_clusters[weekly_cols].sum(axis=1)

    stats = df_clusters.groupby("cluster_dbscan")["total_sales"].agg(
        num_prodotti="count",
        media_vendite="mean",
        std_vendite="std"
    )

    print("\nStatistiche riassuntive per cluster (vendite totali):")
    print(stats)

print("\n" + "=" * 70)
print("FINE SCRIPT – TUTTE LE STAMPE E LE VISUALIZZAZIONI SONO STATE ESEGUITE")
print("=" * 70 + "\n")