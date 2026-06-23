# Documentazione del Progetto Pacman – Alla conquista del Labirinto

**Corso di Laurea Triennale in Informatica (a.a. 2025-2026)**
**Insegnamento:** Ingegneria della Conoscenza – Prof. Nicola Fanizzi
**Università degli Studi di Bari "Aldo Moro"**
**Autore:** Ruggiero Filannino – Matricola 797150

---

## Indice

1. Introduzione
2. Obiettivi del Progetto
3. Struttura del Progetto
4. Tecnologie Utilizzate
5. La Knowledge Base Prolog

* 5.1 Fatti della Base di Conoscenza
* 5.2 Regole della Base di Conoscenza
* 5.3 Generazione della Mappa
* 5.4 Vantaggi e Limiti della Rappresentazione

6. Ragionamento Automatico

* 6.1 Inferenza sui Costi e sugli Ostacoli
* 6.2 Verifica della Validità delle Azioni
* 6.3 Integrazione Python-Prolog

7. Ricerca nello Spazio degli Stati

* 7.1 Modellazione come Spazio di Stati
* 7.2 Algoritmi Implementati (DFS, BFS, A*, Bidirezionale)

8. Interfaccia Grafica (GUI)
9. Test e Analisi Comparativa
10. Manuale Utente
11. Conclusioni e Sviluppi Futuri

---

## 1. Introduzione

Il presente progetto propone la progettazione e lo sviluppo di un sistema basato su conoscenza finalizzato alla risoluzione automatica di un ambiente a griglia $12\times12$, fortemente ispirato alle meccaniche del celebre videogioco **Pacman**. All'interno di questa simulazione, l'utente interagisce con un sistema intelligente incaricato di guidare l'agente (Pacman) attraverso un labirinto ostile, popolato da ostacoli statici e avversari (i fantasmi). Lo scopo ultimo dell'agente è individuare il percorso globalmente ottimale per raggiungere la **Super Pillola**, strategicamente posizionata all'estremità opposta della mappa.

L'applicazione si distingue per l'integrazione sinergica di diverse branche dell'Intelligenza Artificiale: metodologie di rappresentazione della conoscenza, algoritmi di ricerca nello spazio degli stati e programmazione logica dichiarativa, il tutto fruibile attraverso un'interfaccia grafica intuitiva sviluppata in Python. La topologia del mondo di gioco è interamente demandata a una base di conoscenza (Knowledge Base) scritta in Prolog. Questa base descrive lo stato dell'ambiente istante per istante, modellando ogni cella transitabile come un nodo all'interno di un grafo implicito e i movimenti cardinali consentiti come archi orientati.

Le regole logiche implementate non si limitano a descrivere la fisica del mondo, ma codificano in modo rigoroso la validità delle azioni intraprese dall'agente e i costi di attraversamento specifici per ogni tipologia di terreno o nemico. A supporto del ragionamento, il sistema implementa un ventaglio di strategie di ricerca (sia informate che non informate) per esplorare lo spazio delle soluzioni, valutando dinamicamente le opzioni per determinare il cammino più efficiente in termini di dispendio energetico (costo) e numero di passi (lunghezza).

---

## 2. Obiettivi del Progetto

La realizzazione di questo sistema è stata guidata da molteplici obiettivi formativi e architetturali:

* **Modellazione rigorosa della conoscenza di dominio:** Utilizzare la logica del primo ordine tramite Prolog (clausole di Horn) per creare una base di conoscenza solida. L'obiettivo è separare chiaramente la rappresentazione dell'ambiente (dove si trovano i muri, i fantasmi, la pillola) dai meccanismi di risoluzione.
* **Sfruttamento del ragionamento automatico:** Delegare al motore di inferenza Prolog il compito di dedurre la validità dei percorsi e calcolare i costi cumulativi. Il sistema deve "capire" autonomamente se un ostacolo è insormontabile o se richiede un sacrificio in termini di costo per essere superato.
* **Implementazione e studio di algoritmi di ricerca:** Sviluppare e applicare ai grafi generati diverse strategie classiche di Intelligenza Artificiale (DFS, BFS, A*, Ricerca Bidirezionale). Questo permette di valutare l'efficacia di esplorazioni non informate (cieche) rispetto a quelle guidate da euristiche.
* **Analisi e confronto sperimentale:** Raccogliere metriche oggettive per confrontare le prestazioni dei vari algoritmi. L'attenzione è posta sulla lunghezza del percorso trovato, sul costo totale dell'attraversamento e sull'efficienza computazionale (tempi di esecuzione e nodi espansi).
* **Realizzazione di un'interfaccia utente (GUI) interattiva:** Creare un ponte tra l'astrattezza del ragionamento logico e la fruibilità visiva, permettendo all'utente di configurare la mappa, scegliere l'algoritmo risolutore e osservare l'evoluzione della ricerca e del percorso in tempo reale.

---

## 3. Struttura del Progetto

L'architettura del software segue un approccio modulare, separando nettamente la logica di business e di inferenza dalla presentazione grafica e dai test.

```text
Pacman--main/
├── prolog/
│   └── KB.pl                  # Base di Conoscenza: regole d'inferenza, definizioni e dinamiche spaziali
├── gui/
│   └── gui.py                 # Modulo di presentazione: gestione finestre, input utente e renderizzazione (Tkinter)
├── test/
│   └── test.py                # Modulo di benchmark: script per l'esecuzione batch degli algoritmi e raccolta dati
├── docs/
│   └── Documentazione_Pacman.md # Documentazione tecnica e teorica del progetto
├── README.md                  # Introduzione rapida e istruzioni basilari
└── requirements.txt           # Elenco delle dipendenze per l'ambiente virtuale Python

```

Questa netta divisione facilita la manutenzione del codice e permette, ad esempio, di modificare le regole in Prolog senza dover alterare in alcun modo l'interfaccia in Python.

---

## 4. Tecnologie Utilizzate

La scelta dello stack tecnologico è stata dettata dalla necessità di combinare paradigmi di programmazione differenti:

* **SWI-Prolog:** Rappresenta il cuore pensante dell'applicativo. Selezionato per la sua eccellenza nella manipolazione di strutture simboliche, il backtracking automatico e la facilità con cui modella problemi di constraint satisfaction tramite inferenza logica.
* **Python 3 & Tkinter:** Se Prolog fornisce l'intelligenza, Python gestisce l'orchestrazione procedurale. Tkinter, essendo incluso nella standard library di Python, garantisce una creazione rapida ed efficiente della GUI senza richiedere dipendenze pesanti.
* **PySwip:** Un componente cruciale (un bridge) che abilita la comunicazione bidirezionale. Permette allo script Python di interrogare la Knowledge Base, iniettare nuovi fatti o regole a runtime e recuperare le liste unificate restituite da Prolog.
* **Pandas, Matplotlib e Seaborn:** Una suite dedicata all'analisi dati. Questi strumenti sono stati impiegati per processare i log generati durante l'esecuzione del modulo di test, aggregare i risultati e produrre grafici esplicativi per il confronto prestazionale.

---

## 5. La Knowledge Base Prolog

In un sistema esperto o basato su conoscenza, la modalità con cui si rappresentano i dati è altrettanto importante quanto gli algoritmi che li elaborano. La Knowledge Base (KB) di questo progetto codifica l'ontologia del gioco: ogni informazione utile è tradotta in predicati logici, permettendo la rigenerazione dinamica dei livelli e supportando il motore decisionale.

### 5.1 Fatti della Base di Conoscenza

I fatti rappresentano lo stato istantaneo e inequivocabile del mondo. Poiché le mappe del labirinto sono procedurali e variano a ogni nuova partita, è essenziale che le asserzioni Prolog possano essere aggiunte o rimosse durante l'esecuzione. Per questo motivo, i principali predicati spaziali sono dichiarati come `dynamic`.

```prolog
:- dynamic pacman/2.     % Coordinate (X,Y) della posizione di partenza
:- dynamic goal/2.       % Coordinate (X,Y) dell'obiettivo finale (Super Pillola)
:- dynamic muro/2.       % Coordinate delle celle ostruite, totalmente precluse al passaggio
:- dynamic lava/2.       % Coordinate di zone "hazard": attraversabili ma con forte penalità sul costo
:- dynamic blinky/2, pinky/2, inky/2, clyde/2. % Posizionamento dei quattro antagonisti, ciascuno con un proprio "peso"

```

Le dimensioni del campo di gioco, diversamente dagli oggetti al suo interno, sono invece considerate un vincolo statico esplicitato dal predicato `dimensione(12, 12)`.

### 5.2 Regole della Base di Conoscenza

Le regole costituiscono il motore inferenziale: elaborano i fatti statici per dedurre nuove verità, definendo cosa l'agente può o non può fare.

**Regole di Adiacenza:**
Fondamentali per la creazione del grafo implicito, queste regole stabiliscono le relazioni di vicinanza spaziale, assicurandosi parallelamente che i confini della mappa non vengano mai superati.

```prolog
adiacente([X,Y], [X1,Y]) :- X1 is X - 1, X1 >= 0. % Movimento verso l'alto
adiacente([X,Y], [X1,Y]) :- X1 is X + 1, X1 < 12. % Movimento verso il basso
adiacente([X,Y], [X,Y1]) :- Y1 is Y - 1, Y1 >= 0. % Movimento verso sinistra
adiacente([X,Y], [X,Y1]) :- Y1 is Y + 1, Y1 < 12. % Movimento verso destra

```

È interessante notare come l'ordine di dichiarazione di queste direzioni sia ininfluente ai fini della correttezza globale: sarà compito delle euristiche o della coda dell'algoritmo di ricerca stabilire l'effettiva priorità di espansione dei nodi.

**Validità delle celle:**
Questa regola funge da filtro vitale per prevenire percorsi illeciti. Affinché una transizione avvenga, la cella target deve appartenere allo spazio $12\times12$ e, contemporaneamente, l'interprete deve dimostrare (tramite la negazione per fallimento `\+`) l'assenza di un muro in tali coordinate:

```prolog
casella_valida_semplice([X,Y]) :-
    X >= 0, X < 12,
    Y >= 0, Y < 12,
    \+ muro(X,Y).

```

### 5.3 Generazione della Mappa

Il sistema gestisce autonomamente la creazione del terreno di scontro. Attraverso procedure specifiche, la mappa viene bonificata da partite precedenti utilizzando istruzioni come `retractall/1`, per poi essere popolata mediante asserzioni (`asserta/1`).
La generazione prevede:

* **Generazione dei Muri:** Disposti pseudo-casualmente per plasmare la forma e i corridoi del labirinto.
* **Posizionamento degli Ostacoli e Fantasmi:** Gli avversari classici (Blinky, Pinky, Inky, Clyde) e pozze di Lava vengono distribuiti nell'ambiente. Ognuno rappresenta un tipo di penalità differente per Pacman.
* **Controllo Preventivo di Risolvibilità:** Un aspetto critico dell'implementazione è la validazione della mappa. Il sistema avvia una ricerca esplorativa silente; se non esiste alcun percorso matematicamente valido che colleghi lo start al goal (a causa ad esempio di muri che bloccano ogni passaggio), la mappa viene scartata e rigenerata prima di essere mostrata all'utente.

### 5.4 Vantaggi e Limiti della Rappresentazione

* **Vantaggi:** La principale forza dell'uso di Prolog risiede nella trasparenza e modularità. Separare i "dati del mondo" (la mappa) dalle "leggi fisiche" (validità dei movimenti e regole di navigazione) permette di scrivere algoritmi di intelligenza artificiale del tutto agnostici rispetto al design specifico del livello. Le logiche complesse vengono derivate con poche righe di codice dichiarativo.
* **Limiti:** L'inferenza Prolog tradizionale lavora in modo rigidamente deterministico (Vero o Falso). Non si adatta in modo naturale a scenari con incertezza o informazioni parziali, che richiederebbero modelli probabilistici (es. Reti Bayesiane). Inoltre, in labirinti dalle proporzioni considerevolmente superiori al $12\times12$, il backtracking puro potrebbe incorrere in colli di bottiglia prestazionali se non adeguatamente mitigato da euristiche.

---

## 6. Ragionamento Automatico

Il ragionamento automatico è il processo che permette al programma di estrarre percorsi logici combinando i fatti con le regole. In questo progetto, il ragionamento è impiegato principalmente per la valutazione del rischio e dell'efficienza.

### 6.1 Inferenza sui Costi e sugli Ostacoli

Non tutte le celle transitabili hanno la medesima convenienza. Sebbene Pacman possa virtualmente sopportare il contatto con un fantasma o la lava (immaginando che consumi molta "energia" o tempo), l'agente razionale deve cercare di evitarlo se esiste un'alternativa più economica. Le celle vuote, di default, hanno un costo unitario pari a 1.

```prolog
calcola_costo_semplice([X,Y], Costo) :-
    (clyde(X,Y) -> Costo = 8;
     lava(X,Y)  -> Costo = 6;
     inky(X,Y)  -> Costo = 5;
     pinky(X,Y) -> Costo = 4;
     blinky(X,Y)-> Costo = 2;
     Costo = 1).

```

Attraverso costrutti if-then-else (`-> ;`), Prolog valuta immediatamente l'entità che occupa una data cella assegnando il peso corrispondente all'arco del grafo. Questo permette ai calcolatori di percorsi di accumulare iterativamente il costo globale durante l'espansione.

### 6.2 Verifica della Validità delle Azioni

Legando il controllo di adiacenza spaziale (`adiacente/2`) al controllo delle collisioni (`casella_valida_semplice/1`), il motore di ricerca non esamina mai mosse impossibili. Il ragionamento pota in anticipo interi rami dell'albero di ricerca che porterebbero a schiantarsi contro i muri, ottimizzando i tempi.

### 6.3 Integrazione Python-Prolog

L'orchestrazione delle esecuzioni richiede che i complessi output derivanti dalle ricerche Prolog (spesso formattati come lunghe liste di coordinate e costi) siano fruibili dall'interfaccia. La soluzione architetturale adottata è l'uso di predicati wrapper che catturano lo standard output:

```prolog
capture_output(Goal, Output) :-
    with_output_to(atom(Output), Goal).

```

Questa tecnica "imbusta" i risultati della deduzione in stringhe monolitiche, che vengono inviate a Python per essere processate e trasformate negli eventi di animazione visibili all'utente sulla scacchiera.

---

## 7. Ricerca nello Spazio degli Stati

La risoluzione del labirinto non è altro che un classico problema di ricerca in uno Spazio degli Stati, in cui un agente esploratore deve determinare una sequenza di transizioni per evolvere da una configurazione iniziale a una desiderata. L'obiettivo primario del motore AI è ottimizzare tale sequenza minimizzandone il costo.

### 7.1 Modellazione come Spazio di Stati

Per formalizzare matematicamente il problema, l'ambiente è stato tradotto in un grafo orientato pesato:

* **Stati (Nodi):** Ogni cella della griglia $12\times12$ che non contenga un muro.
* **Operatori (Archi):** Le azioni legali di movimento direzionale (Su, Giù, Destra, Sinistra).
* **Pesi degli archi:** Il parametro di attrito derivato dal predicato dei costi (es. attraversare la Lava aggiunge 6 al contatore del costo di percorso).
* **Stato Iniziale:** La cella definita come punto di spawn di Pacman, fissata a `(11, 0)`.
* **Stato Obiettivo:** La cella contenente la Super Pillola, fissata a `(0, 11)`.

### 7.2 Algoritmi Implementati

Il sistema correda la ricerca con un pannello di algoritmi, consentendo confronti didattici:

* **Depth-First Search (DFS):** Strategia "cieca" che si spinge in profondità lungo un singolo ramo di possibilità fino a incontrare un vicolo cieco, ricorrendo poi al backtracking. Non tenendo conto dei pesi, genera frequentemente percorsi inutilmente lunghi, tortuosi e ben lontani dall'ottimalità, risultando vulnerabile a esplorazioni esaustive inefficaci.
* **Breadth-First Search (BFS):** Algoritmo non informato che espande l'albero di ricerca "a macchia d'olio", livello per livello. Benché garantisca l'individuazione del percorso con il *minor numero di passi* assoluti, non computa i costi di attraversamento, portando spesso Pacman a scontrarsi direttamente con gli ostacoli più penalizzanti pur di risparmiare una singola mossa.
* **A* (A-Star):** Il fulcro dell'esplorazione informata intelligente. A* minimizza in ogni istante la funzione $f(n) = g(n) + h(n)$, combinando il costo reale del percorso parziale $g(n)$ con un'euristica ottimistica $h(n)$. Utilizzando la "Distanza di Manhattan" come euristica ammissibile, A* bilancia perfettamente l'esplorazione, evitando le zone costose della mappa e puntando dritto verso l'obiettivo in tempi rapidi.
* **Ricerca Bidirezionale:** Una tecnica evoluta che avvia contemporaneamente due processi di ricerca: uno dall'agente e uno dall'obiettivo (a ritroso). Non appena i due fronti di ricerca si intersecano, l'algoritmo si ferma. Questa strategia abbatte in maniera drastica il fattore di ramificazione dell'albero esplorato, anche se l'onere computazionale per verificare continuamente il "punto di incontro" richiede un'implementazione attenta.

---

## 8. Interfaccia Grafica (GUI)

Nonostante la logica formale risieda nel livello Prolog, la realizzazione dell'interfaccia grafica tramite il toolkit Tkinter è ciò che rende il progetto concretamente apprezzabile. La GUI non è un semplice orpello estetico, ma assolve a tre funzioni primarie:

* **Supporto Didattico:** Visualizza in maniera cristallina il comportamento divergente degli algoritmi. Vedere le tracce lasciate da una DFS rispetto a quelle dirette di un A* aiuta a consolidare la teoria appresa.
* **Feedback e Validazione:** Permette di confermare a colpo d'occhio che i percorsi calcolati rispettino le leggi spaziali del mondo, non compenetrando i muri e reagendo correttamente al posizionamento degli ostacoli.
* **User Experience (UX):** Il progetto è strutturato come un'applicazione stand-alone completa, dotata di un "Main Menu" per la navigazione, una "Story Screen" che fornisce il background narrativo e l'area centrale "Mission Stats", che aggiorna in tempo reale le informazioni su tempi di esecuzione, costi cumulati e lunghezza in passi.

---

## 9. Test e Analisi Comparativa

Per valutare la robustezza e la qualità degli algoritmi proposti, è stata condotta una sessione di testing intensiva basata su decine di generazioni casuali del labirinto. I risultati ottenuti sono stati mediati e aggregati.

| Algoritmo | Lunghezza Media del percorso (passi) | Costo Medio totale dell'attraversamento |
| --- | --- | --- |
| **A*** | 24.6 | 30.5 |
| **DFS** | 60.5 | 82.9 |
| **Ricerca Bidirezionale** | 23.0 | 30.1 |

**Discussione dei Risultati:**
I dati emersi dalla tabella evidenziano scenari molto chiari. La **Ricerca Bidirezionale** primeggia tecnicamente restituendo le lunghezze di percorso inferiori, confermando la bontà della sua concezione topologica. Tuttavia, **A*** si dimostra il risolutore ideale per questo genere di problemi: la sua implementazione risulta estremamente coerente e competitiva, fornendo un cammino ottimale e abbattendo sensibilmente i costi energetici grazie al calcolo ponderato dei pesi.
Di contro, la **DFS** conferma tutti i limiti teorici delle ricerche non informate applicate a problemi con pesi asimmetrici, producendo percorsi irragionevolmente dispendiosi (con costi medi superiori di quasi il 170% rispetto ad A*) ed esplorando inutilmente gran parte del labirinto senza alcun senso logico o finalistico.

---

## 10. Manuale Utente

Per replicare i risultati ed eseguire l'applicativo, seguire questi semplici passi operativi:

**Prerequisiti di Sistema:**

* Ambiente Python aggiornato alla versione 3.9 (o superiore).
* Interprete SWI-Prolog installato e correttamente aggiunto alle variabili d'ambiente (PATH) del sistema operativo.

**Installazione e Avvio Rapido:**

1. Clonare in locale il repository del progetto.
2. Aprire il terminale nella root del progetto e procedere all'installazione delle librerie necessarie eseguendo:
   `pip install -r requirements.txt` (il pacchetto installerà le dipendenze fondamentali quali *pyswip*, *pandas*, *matplotlib*, ecc.).
3. Lanciare il modulo principale dell'interfaccia grafica:
   `python gui/gui.py`
4. Per chi volesse ricreare il dataset di test ed effettuare autonomamente il run esplorativo sui vari algoritmi:
   `python test/test.py`

---

## 11. Conclusioni e Sviluppi Futuri

Questo lavoro di fine corso si configura come un'eccellente e concreta applicazione pratica delle nozioni fondamentali di Intelligenza Artificiale simbolica. Il progetto certifica in maniera tangibile come un sistema multi-linguaggio possa fondere l'eleganza di un ragionatore dichiarativo (capace di valutare vincoli e ostacoli in maniera autonoma) e la flessibilità procedurale di un motore grafico.

L'accoppiata SWI-Prolog e Python ha dimostrato di essere un'architettura estremamente scalabile. Alla luce dei risultati ottenuti, il prototipo si presta in modo eccellente a sviluppi successivi che potrebbero aumentarne drasticamente il livello di sfida e complessità:

* **Ambiente Dinamico e Avversariale:** Trasformare i fantasmi in entità attive in grado di muoversi autonomamente sulla mappa a ogni turno, richiedendo un passaggio da logiche di pathfinding classiche ad algoritmi per giochi a somma zero (come il Minimax o Expectimax).
* **Ottimizzazioni Avanzate:** Implementare strategie come l'Iterative Deepening A* (IDA*) per minimizzare l'utilizzo di memoria in mappe notevolmente più estese.
* **Meccaniche Accessorie:** Introdurre eventi temporanei (i classici "power-up" di Pacman) che permettano di alterare i fatti nella Base di Conoscenza a runtime, mutando, ad esempio, i costi di attraversamento dei fantasmi da un malus a un bonus per un tempo limitato.