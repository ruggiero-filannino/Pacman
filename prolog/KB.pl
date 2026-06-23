/* =========================================================
   PAC-MAN - Alla conquista del Labirinto
   Versione: Griglia 12x12 con fantasmi avanzati, ricerca e ragionamento
   Linguaggio: Prolog (SWI-Prolog)

   Descrizione:
   Questo file rappresenta la Knowledge Base logica del progetto.
   Include la generazione della mappa, la definizione degli ostacoli,
   e l'implementazione degli algoritmi di ricerca:
     - DFS (Depth-First Search)
     - BFS (Breadth-First Search)
     - A* (A-Star)
     - Ricerca Bidirezionale

   Output supportato per GUI Python via pyswip.

   Come eseguire:
   1. Carica in SWI-Prolog
   2. Esegui uno dei seguenti comandi:
       ?- storia.
       ?- pacman_dfs.
       ?- pacman_bfs.
       ?- pacman_astar.
       ?- pacman_bd.
       ?- confronta_algoritmi.
========================================================= */


/* =========================================================
   WRAPPER PER LA GUI
   ---------------------------------------------------------
   Ciascun wrapper esegue l'algoritmo originale ma
   re-indirizza tutto il testo che normalmente finirebbe
   sulla console dentro all'atomo Output.
   ========================================================= */

:- meta_predicate capture_output(0, -).

capture_output(Goal, Output) :-
    with_output_to(atom(Output), Goal).

pacman_bfs_gui(Output)  :- capture_output(pacman_bfs,  Output).
pacman_dfs_gui(Output)  :- capture_output(pacman_dfs,  Output).
pacman_astar_gui(Output):- capture_output(pacman_astar, Output).
pacman_bd_gui(Output)   :- capture_output(pacman_bd,   Output).

% --- Pulizia e dichiarazioni dinamiche ---
:- retractall(dimensione(_, _)).
:- retractall(pacman(_, _)).
:- retractall(goal(_, _)).
:- retractall(muro(_, _)).
:- retractall(lava(_, _)).
:- retractall(blinky(_, _)).
:- retractall(pinky(_, _)).
:- retractall(inky(_, _)).
:- retractall(clyde(_, _)).

% =========================================================
% Fatti dinamici: mappa, Pacman e fantasmi
% =========================================================


:- dynamic dimensione/2.
:- dynamic pacman/2.
:- dynamic goal/2.
:- dynamic muro/2.
:- dynamic lava/2.
:- dynamic blinky/2.
:- dynamic pinky/2.
:- dynamic inky/2.
:- dynamic clyde/2.

% --- CONFIGURAZIONE FISSA ---
% Mappa ora 12x12
:- asserta(dimensione(12, 12)).

% =========================================================
% Narrazione iniziale: contesto e descrizione fantasmi
% =========================================================

% --- PREDICATO PER LA STORIA ---
storia :-
    nl,
    write('*** La Leggenda del Grande Labirinto ***'), nl, nl,
    write('Il Labirinto si è popolato di pericoli e fantasmi!'), nl,
    write('I fantasmi hanno invaso ogni angolo del labirinto:'), nl,
    write('- Blinky: il fantasma rosso, insegue direttamente (costo attraversamento: 2)'), nl,
    write('- Pinky: il fantasma rosa, tenta agguati (costo: 4)'), nl,
    write('- Inky: il fantasma ciano, imprevedibile (costo: 5)'), nl,
    write('- Clyde: il fantasma arancione, timido ma ostinato (costo: 8)'), nl,
    write('- Lava: pozze di magma incandescente (costo: 6)'), nl, nl,
    write('La Super Pillola attende nell\'angolo più remoto del labirinto 12x12.'), nl,
    write('Solo Pacman, con la sua astuzia e velocità, può attraversare questo labirinto mortale!'), nl, nl,
    write('Il punteggio più alto dipende dalla strategia di Pacman...'), nl.

% --- PREDICATI PER LA STAMPA DELLA MAPPA ---
stampa_legenda :-
    nl,
    write('--- Legenda Completa ---'), nl,
    write('P: Pacman (Partenza)'), nl,
    write('G: Goal / Super Pillola (Arrivo)'), nl,
    write('*: Percorso di Pacman'), nl,
    write('#: Muro (Invalicabile)'), nl,
    write('R: Blinky - Fantasma Rosso (Costo: 2)'), nl,
    write('K: Pinky - Fantasma Rosa (Costo: 4)'), nl,
    write('I: Inky - Fantasma Ciano (Costo: 5)'), nl,
    write('C: Clyde - Fantasma Arancione (Costo: 8)'), nl,
    write('L: Lava (Costo: 6)'), nl,
    write('.: Casella Vuota (Costo: 1)'), nl.

stampa_mappa(Percorso) :-
    dimensione(Righe, Colonne), nl,
    scrivi_intestazione_colonne(Colonne),
    scrivi_bordo_superiore(Colonne),
    stampa_righe(0, Righe, Colonne, Percorso),
    scrivi_bordo_superiore(Colonne), nl.

scrivi_intestazione_colonne(Colonne) :-
    UltimaCol is Colonne - 1,
    write('     '),
    between(0, UltimaCol, C),
    (C < 10 -> write(C), write('  ') ; write(C), write(' ')),
    fail.
scrivi_intestazione_colonne(_) :- nl.

scrivi_bordo_superiore(Colonne) :-
    UltimaCol is Colonne - 1,
    write('   +-'),
    between(0, UltimaCol, _),
    write('---'),
    fail.
scrivi_bordo_superiore(_) :- write('-+'), nl.

stampa_righe(Riga, Righe, _, _) :- Riga >= Righe, !.
stampa_righe(Riga, Righe, Colonne, Percorso) :-
    format('~2d |', [Riga]),
    stampa_colonne(0, Colonne, Riga, Percorso),
    write('|'), nl,
    RigaSucc is Riga + 1,
    stampa_righe(RigaSucc, Righe, Colonne, Percorso).

stampa_colonne(Col, Colonne, _, _) :- Col >= Colonne, !.
stampa_colonne(Col, Colonne, Riga, Percorso) :-
    stampa_simbolo(Riga, Col, Percorso),
    write('  '),
    ColSucc is Col + 1,
    stampa_colonne(ColSucc, Colonne, Riga, Percorso).

% =========================================================
% Generazione, stampa e gestione simboli mappa
% =========================================================

% --- Mappatura Simboli Aggiornata ---
stampa_simbolo(R, C, Percorso) :- 
    member([R, C], Percorso), pacman(R,C), !, write('P').
stampa_simbolo(R, C, Percorso) :- 
    member([R, C], Percorso), goal(R,C), !, write('G').
stampa_simbolo(R, C, Percorso) :- 
    member([R, C], Percorso), !, write('*').
stampa_simbolo(R, C, _) :- pacman(R, C), !, write('P').
stampa_simbolo(R, C, _) :- goal(R, C), !, write('G').
stampa_simbolo(R, C, _) :- muro(R, C), !, write('#').
stampa_simbolo(R, C, _) :- lava(R, C), !, write('L').
stampa_simbolo(R, C, _) :- blinky(R, C), !, write('R').
stampa_simbolo(R, C, _) :- pinky(R, C), !, write('K').
stampa_simbolo(R, C, _) :- inky(R, C), !, write('I').
stampa_simbolo(R, C, _) :- clyde(R, C), !, write('C').
stampa_simbolo(_, _, _) :- write('.').

% --- GENERAZIONE INTELLIGENTE DELLA MAPPA 12x12 ---

% Posiziona Pacman e Goal in posizioni fisse per griglia 12x12
piazza_personaggi :-
    asserta(pacman(11, 0)),    % Pacman in basso a sinistra

    asserta(goal(0, 11)).    % Goal in alto a destra
% Genera una mappa garantendo sempre la risolvibilità
genera_mappa :-
    % Pulisci tutto
 % Pulisci tutto
    retractall(pacman(_, _)), retractall(goal(_, _)),
    retractall(muro(_, _)), retractall(lava(_, _)), 
    retractall(blinky(_, _)), retractall(pinky(_, _)), 
    retractall(inky(_, _)), retractall(clyde(_, _)),

    % Piazza i personaggi
    piazza_personaggi,
    
    % Genera ostacoli in modo intelligente
    genera_ostacoli_sicuri,
    
    % Verifica che sia risolvibile, altrimenti rigenera
    (verifica_risolvibilita -> 
        true 
    ; 
        genera_mappa
    ).

% Genera ostacoli in posizioni che non bloccano completamente il percorso
genera_ostacoli_sicuri :-
    findall([R, C],
        (between(0, 11, R), between(0, 11, C),
         \+ pacman(R, C), \+ goal(R, C)),
        PosizCandidati),
    
    % Seleziona 20-30 posizioni casuali per i muri (più muri per griglia più grande)
    random(20, 31, NumMuri),
    seleziona_posizioni_casuali(PosizCandidati, NumMuri, PosizioniMuri),
    piazza_muri_lista(PosizioniMuri),
    
    % Piazza fantasmi variati in posizioni libere
    trova_posizioni_libere(15, PosizioniLibere),
    distribuisci_fantasmi(PosizioniLibere).

% Distribuisce i diversi tipi di fantasmi
distribuisci_fantasmi(Posizioni) :-
    length(Posizioni, NumPos),
    (NumPos >= 15 ->
        Posizioni = [P1,P2,P3,P4,P5,P6,P7,P8,P9,P10,P11,P12,P13,P14,P15|_],
        % 5 Blinky
        piazza_fantasma(P1, blinky), piazza_fantasma(P2, blinky),
        piazza_fantasma(P3, blinky), piazza_fantasma(P4, blinky),piazza_fantasma(P5, blinky),
        % 4 Pinky
        piazza_fantasma(P8, pinky), piazza_fantasma(P9, pinky), piazza_fantasma(P10, pinky),piazza_fantasma(P6, pinky),
        % 3 Inky
        piazza_fantasma(P11, inky), piazza_fantasma(P12, inky),piazza_fantasma(P7, inky),
        % 1 Clyde
        piazza_fantasma(P13, clyde),
        % 2 Lava
        piazza_fantasma(P14, lava), piazza_fantasma(P15, lava)
        
    ;
        % Se non ci sono abbastanza posizioni, distribuisci quelli che puoi
        distribuisci_fantasmi_limitati(Posizioni)
    ).

distribuisci_fantasmi_limitati([]).
distribuisci_fantasmi_limitati([Pos|Resto]) :-
    length([Pos|Resto], N),
    (N >= 8 -> Tipo = blinky
    ; N >= 4 -> Tipo = pinky
    ; N >= 2 -> Tipo = inky
    ; Tipo = lava
    ),
    piazza_fantasma(Pos, Tipo),
    distribuisci_fantasmi_limitati(Resto).

% Piazza un fantasma di un tipo specifico
piazza_fantasma([R,C], blinky) :- asserta(blinky(R, C)).
piazza_fantasma([R,C], pinky) :- asserta(pinky(R, C)).
piazza_fantasma([R,C], inky) :- asserta(inky(R, C)).
piazza_fantasma([R,C], clyde) :- asserta(clyde(R, C)).
piazza_fantasma([R,C], lava) :- asserta(lava(R, C)).

% Seleziona N posizioni casuali da una lista
seleziona_posizioni_casuali(_, 0, []) :- !.
seleziona_posizioni_casuali(Lista, N, [Pos|Resto]) :-
    N > 0,
    length(Lista, Len),
    Len > 0,
    random(0, Len, Indice),
    nth0(Indice, Lista, Pos),
    select(Pos, Lista, NuovaLista),
    N1 is N - 1,
    seleziona_posizioni_casuali(NuovaLista, N1, Resto).

% Piazza muri da una lista di posizioni
piazza_muri_lista([]).
piazza_muri_lista([[R,C]|Resto]) :-
    asserta(muro(R, C)),
    piazza_muri_lista(Resto).

% Trova N posizioni libere nella mappa
trova_posizioni_libere(N, Posizioni) :-
    findall([R,C], 
            (between(0, 11, R), between(0, 11, C),
             \+ pacman(R,C), \+ goal(R,C), \+ muro(R,C)), 
            TutteLibere),
    length(TutteLibere, NumLibere),
    NEffettivo is min(N, NumLibere),
    seleziona_posizioni_casuali(TutteLibere, NEffettivo, Posizioni).

% Verifica che esista un percorso da Pacman a Goal
verifica_risolvibilita :-
    pacman(R1, C1), goal(R2, C2),
    risolvi_astar_semplice([R1, C1], [R2, C2], _).

% --- ALGORITMO A* SEMPLIFICATO ---

% Predicato principale per A*
risolvi_astar_semplice(Partenza, Arrivo, Soluzione) :-
    distanza_manhattan(Partenza, Arrivo, H),
    NodoIniziale = nodo(Partenza, [Partenza], 0, H, H),
    astar([NodoIniziale], Arrivo, [], SoluzioneInvertita),
    reverse(SoluzioneInvertita, Soluzione).

% Caso base: il nodo corrente è lobiettivo
astar([nodo(Arrivo, Percorso, _, _, _)|_], Arrivo, _, Percorso) :- !.

% Passo ricorsivo di A*
astar([NodoCorrente|AltriNodi], Arrivo, Visitati, Soluzione) :-
    NodoCorrente = nodo(Posizione, _, _, _, _),
    NuoviVisitati = [Posizione|Visitati],
    espandi_successori(NodoCorrente, Arrivo, NuoviVisitati, Successori),
    append(AltriNodi, Successori, TuttiNodi),
    ordina_per_f(TuttiNodi, NodiOrdinati),
    astar(NodiOrdinati, Arrivo, NuoviVisitati, Soluzione).

% Se la lista è vuota, non cè soluzione
astar([], _, _, _) :- fail.

% Espansione dei successori per A*
espandi_successori(nodo(Posizione, Percorso, G, _, _), Arrivo, Visitati, Successori) :-
    findall(nodo(NuovaPosizione, NuovoPercorso, NuovoG, H, F),
            (adiacente(Posizione, NuovaPosizione),
             casella_valida_semplice(NuovaPosizione),
             \+ member(NuovaPosizione, Visitati),
             \+ member(NuovaPosizione, Percorso),
             NuovoPercorso = [NuovaPosizione|Percorso],
             calcola_costo_semplice(NuovaPosizione, CostoMossa),
             NuovoG is G + CostoMossa,
             distanza_manhattan(NuovaPosizione, Arrivo, H),
             F is NuovoG + H),
            Successori).

% Movimenti adiacenti (4 direzioni) - usa dimensione dinamica
adiacente([X,Y], [X1,Y]) :- X1 is X - 1, X1 >= 0.     % su
adiacente([X,Y], [X1,Y]) :- dimensione(MaxR, _), X1 is X + 1, X1 < MaxR.  % giù
adiacente([X,Y], [X,Y1]) :- Y1 is Y - 1, Y1 >= 0.     % sinistra
adiacente([X,Y], [X,Y1]) :- dimensione(_, MaxC), Y1 is Y + 1, Y1 < MaxC.  % destra

% Una casella è valida se è dentro la mappa e non è un muro
casella_valida_semplice([X,Y]) :-
    dimensione(MaxR, MaxC),
    X >= 0, X < MaxR, Y >= 0, Y < MaxC,
    \+ muro(X,Y).

% Calcola il costo di movimento (aggiornato con tutti i fantasmi)
calcola_costo_semplice([X,Y], Costo) :-
    (clyde(X,Y) -> Costo = 8
    ; lava(X,Y) -> Costo = 6
    ; inky(X,Y) -> Costo = 5
    ; pinky(X,Y) -> Costo = 4
    ; blinky(X,Y) -> Costo = 2
    ; Costo = 1
    ).

% Calcola la distanza di Manhattan
distanza_manhattan([X1,Y1], [X2,Y2], Distanza) :-
    DeltaX is abs(X2 - X1),
    DeltaY is abs(Y2 - Y1),
    Distanza is DeltaX + DeltaY.

% Ordina i nodi per f-score
ordina_per_f(Nodi, NodiOrdinati) :-
    predsort(confronta_f, Nodi, NodiOrdinati).

% Predicato di confronto per lordinamento
confronta_f(Ordine, nodo(_, _, _, _, F1), nodo(_, _, _, _, F2)) :-
    (F1 < F2 -> Ordine = '<'
    ; F1 > F2 -> Ordine = '>'
    ; Ordine = '='
    ).

% --- ALGORITMO DFS (DEPTH-FIRST SEARCH) ---

% Predicato principale per DFS
risolvi_dfs(Partenza, Arrivo, Percorso) :-
    risolvi_percorso_dfs(Partenza, Arrivo, [Partenza], PercorsoInvertito),
    reverse(PercorsoInvertito, Percorso).

% Caso base: siamo arrivati a destinazione
risolvi_percorso_dfs(Arrivo, Arrivo, PercorsoVisitato, PercorsoVisitato) :- !.

% Passo ricorsivo DFS
risolvi_percorso_dfs(Corrente, Arrivo, Visitati, Percorso) :-
    adiacente(Corrente, Prossima),
    casella_valida_semplice(Prossima),
    \+ member(Prossima, Visitati),
    risolvi_percorso_dfs(Prossima, Arrivo, [Prossima|Visitati], Percorso).

% --- ALGORITMO BFS (BREADTH-FIRST SEARCH) ---

% Predicato principale per BFS
risolvi_bfs(Partenza, Arrivo, Soluzione) :-
    bfs([[Partenza]], Arrivo, PercorsoInvertito),
    reverse(PercorsoInvertito, Soluzione).

% Caso base: il primo percorso nella coda raggiunge lobiettivo
bfs([[Arrivo|Percorso]|_], Arrivo, [Arrivo|Percorso]) :- !.

% Passo ricorsivo: estende il primo percorso e lo aggiunge in fondo alla coda
bfs([PercorsoAttuale|AltriPercorsi], Arrivo, Soluzione) :-
    estendi_bfs(PercorsoAttuale, NuoviPercorsi),
    append(AltriPercorsi, NuoviPercorsi, CodaAggiornata),
    bfs(CodaAggiornata, Arrivo, Soluzione).

% Se la coda è vuota, non cesoluzione
bfs([], _, _) :- fail.

% Estende un percorso con tutte le mosse valide
estendi_bfs([Nodo|Percorso], NuoviPercorsi) :-
    findall([NuovoNodo, Nodo|Percorso],
            (adiacente(Nodo, NuovoNodo),
             casella_valida_semplice(NuovoNodo),
             \+ member(NuovoNodo, [Nodo|Percorso])),
            NuoviPercorsi).

% --- ALGORITMO RICERCA BIDIREZIONALE ---
% Due BFS simultanee: una da Pacman, una dalla Super Pillola.
% bd_loop(CodaF, TuttiF, VisitatiF, CodaB, TuttiB, VisitatiB, Soluzione)
%   - CodaF/B: frontiera corrente (paths)
%   - TuttiF/B: TUTTI i paths generati finora (per ricostruzione)
%   - VisitatiF/B: nodi già espansi da ciascun lato

risolvi_bd(Partenza, Arrivo, Soluzione) :-
    bd_loop([[Partenza]], [[Partenza]], [Partenza],
            [[Arrivo]],   [[Arrivo]],   [Arrivo],
            Soluzione).

% Coda vuota → fallimento
bd_loop([], _, _, _, _, _, _) :- !, fail.
bd_loop(_, _, _, [], _, _, _) :- !, fail.

% Espandi forward, controlla intersezione, poi espandi backward
bd_loop(CodaF, TuttiF, VisitatiF, CodaB, TuttiB, VisitatiB, Soluzione) :-
    espandi_frontiera_bd(CodaF, NuovaCodaF),
    append(TuttiF, NuovaCodaF, NuoviTuttiF),
    aggiorna_visitati_bd(NuovaCodaF, VisitatiF, NuoviVisitatiF),
    (   trova_intersezione_bd(NuovaCodaF, VisitatiB, TuttiB, PF, PB)
    ->  ricostruisci_bd(PF, PB, Soluzione)
    ;   bd_loop_backward(NuovaCodaF, NuoviTuttiF, NuoviVisitatiF,
                          CodaB, TuttiB, VisitatiB, Soluzione)
    ).

% Espandi backward, controlla intersezione, poi torna a forward
bd_loop_backward(CodaF, TuttiF, VisitatiF, CodaB, TuttiB, VisitatiB, Soluzione) :-
    espandi_frontiera_bd(CodaB, NuovaCodaB),
    append(TuttiB, NuovaCodaB, NuoviTuttiB),
    aggiorna_visitati_bd(NuovaCodaB, VisitatiB, NuoviVisitatiB),
    (   trova_intersezione_bd(NuovaCodaB, VisitatiF, TuttiF, PB, PF)
    ->  reverse(PB, PBRaw),
        reverse(PF, PFNorm),
        append(PFNorm, PBRaw, Soluzione)
    ;   bd_loop(CodaF, TuttiF, VisitatiF,
                NuovaCodaB, NuoviTuttiB, NuoviVisitatiB, Soluzione)
    ).

% Espande un livello: ogni path in coda genera tutti i successori validi
espandi_frontiera_bd([], []).
espandi_frontiera_bd([Percorso|Code], NuovaCoda) :-
    Percorso = [Nodo|Resto],
    findall([NuovoNodo, Nodo|Resto],
            (adiacente(Nodo, NuovoNodo),
             casella_valida_semplice(NuovoNodo),
             \+ member(NuovoNodo, Percorso)),
            Estesi),
    espandi_frontiera_bd(Code, RestoCoda),
    append(Estesi, RestoCoda, NuovaCoda).

% Aggiunge i nodi testa dei nuovi paths alla lista visitati
aggiorna_visitati_bd([], V, V).
aggiorna_visitati_bd([[Nodo|_]|Code], Visitati, NuoviVisitati) :-
    (member(Nodo, Visitati) -> NV = Visitati ; NV = [Nodo|Visitati]),
    aggiorna_visitati_bd(Code, NV, NuoviVisitati).

% Cerca un path nella nuova coda il cui nodo testa è stato visitato dall'altra ricerca
% e trova il percorso corrispondente in Tutti (tutti i paths dell'altra ricerca)
trova_intersezione_bd([Percorso|_], VisitatiAltro, TuttiAltro, Percorso, PercorsoAltro) :-
    Percorso = [Nodo|_],
    member(Nodo, VisitatiAltro),
    !,
    member(PercorsoAltro, TuttiAltro),
    PercorsoAltro = [Nodo|_].
trova_intersezione_bd([_|Code], VisitatiAltro, TuttiAltro, PF, PB) :-
    trova_intersezione_bd(Code, VisitatiAltro, TuttiAltro, PF, PB).

% Ricostruisce il percorso completo: [Start, ..., Nodo, ..., Goal]
ricostruisci_bd(PercorsoF, PercorsoB, Soluzione) :-
    reverse(PercorsoF, PFNorm),
    PercorsoB = [_|Tail],
    append(PFNorm, Tail, Soluzione).

% --- PREDICATI PRINCIPALI ---

% Avvia la risoluzione con DFS
pacman_dfs :-
    write('Generando mappa 12x12 con fantasmi avanzati...'), nl,
    genera_mappa,
    write('--- Mappa Generata ---'), nl,
    stampa_mappa([]),
    nl,
    pacman(R1, C1), goal(R2, C2),
    write('Cercando percorso con DFS (Depth-First Search)...'), nl,
    time(risolvi_dfs([R1, C1], [R2, C2], Percorso)),
    write('--- Soluzione DFS Trovata! ---'), nl,
    stampa_mappa(Percorso),
    memorizza_percorso(Percorso),
    stampa_legenda,
    length(Percorso, Lunghezza),
    write('Lunghezza percorso: '), write(Lunghezza), nl,
    calcola_costo_totale(Percorso, CostoTotale),
    write('Costo totale: '), write(CostoTotale), nl, !.

pacman_dfs :-
    write('Errore: Nessun percorso trovato con DFS.'), nl.

% Avvia la risoluzione con BFS
pacman_bfs :-
    write('Generando mappa 12x12 con fantasmi avanzati...'), nl,
    genera_mappa,
    write('--- Mappa Generata ---'), nl,
    stampa_mappa([]),
    nl,
    pacman(R1, C1), goal(R2, C2),
    write('Cercando percorso con BFS (Breadth-First Search)...'), nl,
    time(risolvi_bfs([R1, C1], [R2, C2], Percorso)),
    memorizza_percorso(Percorso),
    write('--- Soluzione BFS Trovata! ---'), nl,
    stampa_mappa(Percorso),
    stampa_legenda,
    length(Percorso, Lunghezza),
    write('Lunghezza percorso: '), write(Lunghezza), nl,
    calcola_costo_totale(Percorso, CostoTotale),
    write('Costo totale: '), write(CostoTotale), nl, !.

pacman_bfs :-
    write('Errore: Nessun percorso trovato con BFS.'), nl.

% Avvia la risoluzione con A*
pacman_astar :-
    write('Generando mappa 12x12 con fantasmi avanzati...'), nl,
    genera_mappa,
    write('--- Mappa Generata ---'), nl,
    stampa_mappa([]),
    nl,
    pacman(R1, C1), goal(R2, C2),
    write('Cercando percorso ottimale con A*...'), nl,
    time(risolvi_astar_semplice([R1, C1], [R2, C2], Percorso)),
    memorizza_percorso(Percorso),
    write('--- Soluzione A* Trovata! ---'), nl,
    stampa_mappa(Percorso),
    stampa_legenda,
    length(Percorso, Lunghezza),
    write('Lunghezza percorso: '), write(Lunghezza), nl,
    calcola_costo_totale(Percorso, CostoTotale),
    write('Costo totale: '), write(CostoTotale), nl, !.

pacman_astar :-
    write('Errore: Nessun percorso trovato con A*.'), nl.

% Avvia la risoluzione con Ricerca Bidirezionale
pacman_bd :-
    write('Generando mappa 12x12 con fantasmi avanzati...'), nl,
    genera_mappa,
    write('--- Mappa Generata ---'), nl,
    stampa_mappa([]),
    nl,
    pacman(R1, C1), goal(R2, C2),
    write('Cercando percorso con Ricerca Bidirezionale...'), nl,
    time(risolvi_bd([R1, C1], [R2, C2], Percorso)),
    memorizza_percorso(Percorso),
    write('--- Soluzione Ricerca Bidirezionale Trovata! ---'), nl,
    stampa_mappa(Percorso),
    stampa_legenda,
    length(Percorso, Lunghezza),
    write('Lunghezza percorso: '), write(Lunghezza), nl,
    calcola_costo_totale(Percorso, CostoTotale),
    write('Costo totale: '), write(CostoTotale), nl, !.

pacman_bd :-
    write('Errore: Nessun percorso trovato con Ricerca Bidirezionale.'), nl.

% Calcola il costo totale del percorso
calcola_costo_totale([], 0).
calcola_costo_totale([Pos], Costo) :-
    calcola_costo_semplice(Pos, Costo).
calcola_costo_totale([Pos|Resto], CostoTotale) :-
    calcola_costo_semplice(Pos, Costo),
    calcola_costo_totale(Resto, CostoResto),
    CostoTotale is Costo + CostoResto.

% --- CONFRONTO TRA TUTTI GLI ALGORITMI ---
confronta_algoritmi :-
    write('=== CONFRONTO TRA TUTTI GLI ALGORITMI ==='), nl,
    write('Generando mappa 12x12 con fantasmi avanzati...'), nl,
    genera_mappa,
    write('--- Mappa Generata ---'), nl,
    stampa_mappa([]),
    nl,
    pacman(R1, C1), goal(R2, C2),
    
    % Test DFS
    write('>>> TESTING DFS <<<'), nl,
    (time(risolvi_dfs([R1, C1], [R2, C2], PercorsoDFS)) ->
        (length(PercorsoDFS, LunghezzaDFS),
         calcola_costo_totale(PercorsoDFS, CostoDFS),
         format('DFS - Lunghezza: ~w, Costo: ~w~n', [LunghezzaDFS, CostoDFS]))
    ;   write('DFS: Nessuna soluzione trovata'), nl
    ),

    % Test BFS
    write('>>> TESTING BFS <<<'), nl,
    (time(risolvi_bfs([R1, C1], [R2, C2], PercorsoBFS)) ->
        (length(PercorsoBFS, LunghezzaBFS),
         calcola_costo_totale(PercorsoBFS, CostoBFS),
         format('BFS - Lunghezza: ~w, Costo: ~w~n', [LunghezzaBFS, CostoBFS]))
    ;   write('BFS: Nessuna soluzione trovata'), nl
    ),

    % Test A*
    write('>>> TESTING A* <<<'), nl,
    (time(risolvi_astar_semplice([R1, C1], [R2, C2], PercorsoASTAR)) ->
        (length(PercorsoASTAR, LunghezzaASTAR),
         calcola_costo_totale(PercorsoASTAR, CostoASTAR),
         format('A* - Lunghezza: ~w, Costo: ~w~n', [LunghezzaASTAR, CostoASTAR]))
    ;   write('A*: Nessuna soluzione trovata'), nl
    ),
    
    % Test Ricerca Bidirezionale
    write('>>> TESTING RICERCA BIDIREZIONALE <<<'), nl,
    (time(risolvi_bd([R1, C1], [R2, C2], PercorsoBD)) ->
        (length(PercorsoBD, LunghezzaBD),
         calcola_costo_totale(PercorsoBD, CostoBD),
         format('Ricerca Bidirezionale - Lunghezza: ~w, Costo: ~w~n', [LunghezzaBD, CostoBD]))
    ;   write('Ricerca Bidirezionale: Nessuna soluzione trovata'), nl
    ),
    
    nl, write('=== CONFRONTO COMPLETATO ==='), nl.

% --- PREDICATO ESPORTABILE PER LA GUI PYTHON ---
get_mappa(Mappa) :-
    findall((R, C, Simbolo), cella(R, C, Simbolo), Mappa).

% Determina il simbolo per ogni cella
cella(R, C, 'P') :- pacman(R, C), !.
cella(R, C, 'G') :- goal(R, C), !.
cella(R, C, '*') :- percorso_memorizzato(PL), member([R, C], PL), !.
cella(R, C, '#') :- muro(R, C), !.
cella(R, C, 'L') :- lava(R, C), !.
cella(R, C, 'R') :- blinky(R, C), !.
cella(R, C, 'K') :- pinky(R, C), !.
cella(R, C, 'I') :- inky(R, C), !.
cella(R, C, 'C') :- clyde(R, C), !.
cella(_, _, '.').

% Per memorizzare il percorso trovato
:- dynamic percorso_memorizzato/1.
memorizza_percorso(P) :- 
    retractall(percorso_memorizzato(_)), 
    assertz(percorso_memorizzato(P)).