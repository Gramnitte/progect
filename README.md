<h1>📊 DBSCAN – Clustering di prodotti basato sulla densità</h1>
<h3>Progetto per il corso “Principi e Modelli della Percezione” – A.A. 2025/2026</h3>
<h5>DBSCAN (Density-Based Spatial Clustering of Applications with Noise) è stato scelto perché:</h5>
<h5>non richiede di specificare il numero di cluster;</h5>
<h5>gestisce cluster di forma arbitraria;</h5>
<h5>identifica naturalmente il rumore (etichette = -1);</h5>
<h5>è robusto agli outlier.</h5>
<h4></h4>
<h4>Due parametri fondamentali utilizzati:</h4>
<h5>eps: raggio di vicinanza tra punti;</h5>
<h5>minPts: minimo numero di punti per definire una zona densa.</h5>

<h2>📁 Dataset</h2>
<h5>Il dataset contiene 800 prodotti, ciascuno monitorato per 52 settimane. Ogni riga rappresenta un prodotto e ogni colonna il volume di vendita settimanale.</h5>

<h2>🎯 Obiettivo</h2>
<h5>L’obiettivo del progetto è:</h5>
<h5>individuare cluster di prodotti che condividono pattern di vendita simili;</h5>
<h5>identificare outlier con comportamenti anomali;</h5>
<h5>supportare strategie di riassortimento e analisi delle performance.</h5>

<h2>📈 Risultati principali</h2>
<h5>Sono state realizzate diverse visualizzazioni per interpretare i cluster:</h5>
<h5>Scatter Plot: visualizza i prodotti nel nuovo spazio PCA, distinguendo chiaramente i cluster e gli outlier.</h5>
<h5>Istogramma: mostra la distribuzione numerica dei prodotti per cluster.</h5>
<h5>Lineplot: illustra il profilo medio delle vendite durante l’anno per ogni cluster.</h5>
<h5>Boxplot (W0): rappresenta la distribuzione delle vendite nella prima settimana per ciascun gruppo.</h5>
<h5>Heatmap: evidenzia le vendite medie dei cluster nel tempo.</h5>



