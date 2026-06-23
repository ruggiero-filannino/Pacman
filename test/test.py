"""
test.py - Analisi comparativa degli algoritmi di ricerca in Prolog

Questo script esegue più test automatici sulla KB Prolog (KB.pl),
interrogando la clausola `confronta_algoritmi` che restituisce, per ciascun
algoritmo (DFS, A*, Ricerca Bidirezionale), la lunghezza e il costo del percorso.

I risultati vengono salvati in CSV e analizzati tramite statistiche e grafici.
"""

from pyswip import Prolog
import re
import pandas as pd
import time
import matplotlib.pyplot as plt
import seaborn as sns

print("🚀 PAC-MAN TEST - Versione Veloce")
print("=" * 50)

# === SETUP PROLOG ===
prolog = Prolog()
try:
    # Caricamento della knowledge base logica
    list(prolog.query("consult('prolog/KB.pl')"))
    print("✅ KB caricata!")
except Exception as e:
    print(f"❌ Errore KB: {e}")
    exit(1)

# === CONFIGURAZIONE TEST ===
num_tests = int(input("🎯 DISCLAIMER : PUOI ANCHE METTERE 100 TEST. Numero test (5-20 consigliato): ") or "10")

# === REGEX e STORAGE ===
# Pattern per estrarre: "Algoritmo - Lunghezza: X, Costo: Y"
pattern = re.compile(r"(DFS|BFS|A\*|Ricerca Bidirezionale) - Lunghezza: (\d+), Costo: (\d+)")
results = []

print(f"\n🏃‍♂️ Esecuzione {num_tests} test rapidi...")

# === CRONOMETRO ===
start_time = time.time()

# Esecuzione ciclica dei test
for i in range(num_tests):
    print(f"⚡ Test {i+1}/{num_tests}...", end=" ", flush=True)
    
    try:
        # Richiama confronto degli algoritmi da Prolog
        output = list(prolog.query("capture_output(confronta_algoritmi, X)."))[0]['X']
        
        # Estrazione risultati con regex
        for match in pattern.finditer(output):
            algoritmo, lunghezza, costo = match.groups()
            results.append({
                'Test': i+1,
                'Algoritmo': algoritmo.strip(),
                'Lunghezza': int(lunghezza),
                'Costo': int(costo)
            })
        
        print("✅")
        
    except Exception as e:
        print(f"❌ {str(e)[:30]}...")

# === RISULTATI TEST ===
total_time = time.time() - start_time
print(f"\n⏱️ Completato in {total_time:.1f}s ({total_time/num_tests:.2f}s per test)")

if not results:
    print("❌ Nessun dato raccolto!")
    exit(1)

# Costruzione DataFrame pandas
df = pd.DataFrame(results)
print(f"📊 Raccolti {len(df)} risultati")

# === STATISTICHE ===
print("\n" + "="*60)
print("📈 STATISTICHE RAPIDE")
print("="*60)

summary = df.groupby('Algoritmo').agg({
    'Lunghezza': ['mean', 'min', 'max', 'std'],
    'Costo': ['mean', 'min', 'max', 'std']
}).round(2)

print(summary)

# === CONFRONTO ALGORITMI MEDIA ===
print("\n🏆 CONFRONTO ALGORITMI:")
means = df.groupby('Algoritmo')[['Lunghezza', 'Costo']].mean().round(2)
for algo in means.index:
    lunghezza = means.loc[algo, 'Lunghezza']
    costo = means.loc[algo, 'Costo']
    print(f"   {algo:20} | Lunghezza: {lunghezza:6} | Costo: {costo:6}")

# === GRAFICO ===
try:
    plt.style.use('dark_background')
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Boxplot della lunghezza
    df.boxplot(column='Lunghezza', by='Algoritmo', ax=ax1)
    ax1.set_title('📏 Distribuzione Lunghezza Percorso', color='white', fontsize=14)
    ax1.set_xlabel('Algoritmo', color='white')
    ax1.set_ylabel('Lunghezza', color='white')
    
    # Boxplot del costo
    df.boxplot(column='Costo', by='Algoritmo', ax=ax2)
    ax2.set_title('💰 Distribuzione Costo', color='white', fontsize=14)
    ax2.set_xlabel('Algoritmo', color='white')
    ax2.set_ylabel('Costo', color='white')
    
    # Titolo generale
    plt.suptitle('Pacman Algorithm Performance - Quick Analysis', 
                 color='cyan', fontsize=16, y=0.98)
    
    plt.tight_layout()
    plt.savefig('quick_results.png', dpi=150, bbox_inches='tight', 
                facecolor='black', edgecolor='none')
    
    print(f"\n📊 Grafico salvato: quick_results.png")
    plt.show()
    
except Exception as e:
    print(f"⚠️ Errore grafico: {e}")

# === SALVATAGGIO SU FILE ===
try:
    df.to_csv('quick_results.csv', index=False)
    summary.to_csv('quick_summary.csv')
    print(f"💾 Dati esportati: quick_results.csv, quick_summary.csv")
except Exception as e:
    print(f"⚠️ Errore esportazione: {e}")

print(f"\n🏁 Test completato! Tempo totale: {total_time:.1f}s")
