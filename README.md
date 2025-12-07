<h1>📊 DBSCAN – Clustering di prodotti basato sulla densità</h1>
<h5>Progetto per il corso “Principi e Modelli della Percezione” – A.A. 2025/2026</h5>
<h6>DBSCAN (Density-Based Spatial Clustering of Applications with Noise) è stato scelto perché:</h6>
<h6>non richiede di specificare il numero di cluster;</h6>
<h6>gestisce cluster di forma arbitraria;</h6>
<h6>identifica naturalmente il rumore (etichette = -1);</h6>
<h6>è robusto agli outlier.</h6>

<h5>Due parametri fondamentali utilizzati:</h5>
<h6>eps: raggio di vicinanza tra punti;</h6>
<h6>minPts: minimo numero di punti per definire una zona densa.</h6>

<h2>📁 Dataset</h2>
<h6>Il dataset contiene 800 prodotti, ciascuno monitorato per 52 settimane. Ogni riga rappresenta un prodotto e ogni colonna il volume di vendita settimanale.

<h2>🎯 Obiettivo</h2>
<h6>L’obiettivo del progetto è:</h6>
<h6>individuare cluster di prodotti che condividono pattern di vendita simili;</h6>
<h6>identificare outlier con comportamenti anomali;</h6>
<h6>supportare strategie di riassortimento e analisi delle performance.</h6>

<h2>📈 Risultati principali</h2>
<h6>Sono state realizzate diverse visualizzazioni per interpretare i cluster:</h6>
<h6>Scatter Plot: visualizza i prodotti nel nuovo spazio PCA, distinguendo chiaramente i cluster e gli outlier.</h6>
<h6>Istogramma: mostra la distribuzione numerica dei prodotti per cluster.</h6>
<h6>Lineplot: illustra il profilo medio delle vendite durante l’anno per ogni cluster.</h6>
<h6>Boxplot (W0): rappresenta la distribuzione delle vendite nella prima settimana per ciascun gruppo.</h6>
<h6>Heatmap: evidenzia le vendite medie dei cluster nel tempo.</h6>



