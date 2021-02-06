# ROAmbulatori

Premessa:

Il programma gestisce il seguente problema:

Lo scenario si compone di un poliambulatorio, composto da tre ambulatori medici identici e cinque medici, ognuno specializzato in un esame medico diverso. In tutto, gli ambulatori possono fornire un totale di cinque esami diversi.
Nel poliambulatorio entrano alcuni pazienti (numero variabile), ognuno può scegliere a quali esami sottoporsi, da  un minimo di uno, ad un massimo di cinque. Quando un paziente occupa un ambulatorio, deve rimanerci dentro fino alla completa risoluzione di tutti i suoi esami, inoltre egli preclude ad altri la possibilità di utilizzare l'ambulatorio occupato.
Siccome ogni tipologia di esame può essere eseguita solo da un medico in particolare, nello stesso istante non possono essere in esecuzione esami della stessa natura in ambulatori diversi.
L'obiettivo del problema è fornire tutte le prestazioni mediche richiete dai pazienti, avendo un makespan minimo.

Caratteristiche:

Il programma permette all'utente di creare un nuovo problema da risolvere, partendo da una configurazione estesa personalizzabile.
Successivamente è possibile creare soluzioni utilizzando diversi algoritmi:

- Greedy: soluzione di partenza in cui è possibile sceglierne la tipologia (LPT, SPT, FIFO) e se utilizzare la randomicità durante la creazione.
- Simulated Annealing: ricerca locale utilizzata per migliorare una soluzione.
- Path Relinking: ricerca nello spazio ristretto alle soluzioni simili a quelle di input della procedura

All'utente viene fornita la possibilità di gestire manualmente la creazione delle soluzioni, oppure di avvalersi di una procedura automatica che, partendo dalla creazione di una nuova istanza del problema e arrivando all'applicazione di Path Relinking, genera una soluzione ottima al problema attuale.
L'interfaccia grafica prevede una semplice visualizzazione delle soluzioni generate, utile per il confronto manuale da parte dell'utente.