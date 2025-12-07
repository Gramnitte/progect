<h1>📊 DBSCAN – Clustering di prodotti basato sulla densità<h1>
Progetto per il corso “Principi e Modelli della Percezione” – A.A. 2025/2026
###DBSCAN (Density-Based Spatial Clustering of Applications with Noise) è stato scelto perché:
non richiede di specificare il numero di cluster;
gestisce cluster di forma arbitraria;
identifica naturalmente il rumore (etichette = -1);
è robusto agli outlier.

###Due parametri fondamentali utilizzati:
eps: raggio di vicinanza tra punti;
minPts: minimo numero di punti per definire una zona densa.

##📁 Dataset
Il dataset contiene 800 prodotti, ciascuno monitorato per 52 settimane. Ogni riga rappresenta un prodotto e ogni colonna il volume di vendita settimanale.

##🎯 Obiettivo
L’obiettivo del progetto è:
individuare cluster di prodotti che condividono pattern di vendita simili;
identificare outlier con comportamenti anomali;
supportare strategie di riassortimento e analisi delle performance.

##📈 Risultati principali
Sono state realizzate diverse visualizzazioni per interpretare i cluster:
Scatter Plot: visualizza i prodotti nel nuovo spazio PCA, distinguendo chiaramente i cluster e gli outlier.
Istogramma: mostra la distribuzione numerica dei prodotti per cluster.
Lineplot: illustra il profilo medio delle vendite durante l’anno per ogni cluster.
Boxplot (W0): rappresenta la distribuzione delle vendite nella prima settimana per ciascun gruppo.
Heatmap: evidenzia le vendite medie dei cluster nel tempo.



