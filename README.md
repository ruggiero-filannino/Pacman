
# Pacman – Alla ricerca del Frutto Perduto

Questo progetto è stato realizzato per il **corso di laurea triennale in Informatica** (a.a. 2025-2026) presso l'**Università degli Studi di Bari Aldo Moro**, per l'insegnamento di **Ingegneria della Conoscenza** tenuto dal **Prof. Nicola Fanizzi**.

---

## 🎯 Finalità del progetto

Il progetto propone un ambiente simulato ispirato al mondo di Pacman, in cui l'utente guida Pacman attraverso un **labirinto 12x12** ricco di ostacoli e fantasmi, con l'obiettivo di raggiungere la Super Pillola e completare il livello.

L'obiettivo didattico è applicare i concetti fondamentali dell'**Ingegneria della Conoscenza**, combinando:

- La **rappresentazione della conoscenza** tramite fatti e regole logiche
- La **ricerca di soluzioni** in spazi di stato complessi
- Il **ragionamento simbolico** su costi, percorsi e vincoli
- L'integrazione con interfacce interattive e strumenti di visualizzazione

---

## 📚 Contenuti e metodi

Il progetto affronta un problema di pianificazione del percorso all'interno di un dominio strutturato, tenendo conto di:
- **ostacoli invalicabili** (muri),
- **ostacoli con costo di attraversamento** (fantasmi),
- **strategie differenti di esplorazione** (algoritmi di ricerca).

L'utente può scegliere il metodo di esplorazione da utilizzare e osservare le differenze tra le strategie adottate.

---

## ⚙️ Componenti del progetto

| Componente     | Descrizione                                                                 |
|----------------|------------------------------------------------------------------------------|
| `prolog/KB.pl` | Base di conoscenza logica scritta in Prolog. Contiene lo stato del mondo e gli algoritmi di ricerca. |
| `gui/gui.py`   | Interfaccia grafica scritta in Python, consente la navigazione e la visualizzazione della mappa. |
| `test/test.py` | Script per lanciare test multipli e raccogliere statistiche su costi e lunghezze dei percorsi. |
| `docs/`        | Documentazione tecnica realizzata in LaTeX.                                  |
| `requirements.txt` | Elenco delle librerie Python necessarie all'esecuzione.                |
| `.gitignore`   | File per evitare il tracciamento di cartelle e file temporanei come `venv/`. |

---

## 🔍 Algoritmi di ricerca implementati

Nella base di conoscenza logica sono stati implementati e confrontati i seguenti algoritmi classici:

- **DFS** – Ricerca in profondità
- **A\*** – Ricerca informata con funzione euristica di tipo Manhattan
- **Ricerca Bidirezionale**

Ciascun algoritmo valuta percorsi alternativi in una mappa dinamica e restituisce soluzioni con lunghezza e costo totali differenti.

---

## 📦 Tecnologie utilizzate

- **Prolog (SWI-Prolog)** – per la modellazione logica e la definizione delle regole
- **Python 3** – per la GUI e la parte procedurale
- **pyswip** – per l'interfacciamento tra Python e Prolog
- **Tkinter** – per lo sviluppo dell'interfaccia grafica
- **Pandas, Matplotlib, Seaborn** – per la raccolta e visualizzazione delle statistiche

---

## 🛠️ Istruzioni per l'installazione

### 1. Prerequisiti

- Python 3.9 o superiore
- SWI-Prolog installato e accessibile da terminale
- pip installato per la gestione dei pacchetti

### 2. Creazione ambiente virtuale (opzionale ma consigliata)

```bash
python -m venv venv
source venv/bin/activate       # Linux/macOS
venv\Scripts\activate.bat    # Windows
```

### 3. Installazione delle dipendenze Python

```bash
pip install -r requirements.txt
```

Contenuto di `requirements.txt`:

```
pyswip
pandas
matplotlib
seaborn
```

---

## ▶️ Esecuzione del progetto

### Interfaccia grafica

```bash
python gui/gui.py
```

### Esecuzione dei test comparativi

```bash
python test/test.py
```



---

## 📊 Output del sistema

- Mappa visuale con rappresentazione degli elementi di gioco
- Animazione del percorso calcolato
- Output testuale della soluzione trovata
- Report di test multipli con confronto tra algoritmi
- Esportazione dei risultati in formato CSV


