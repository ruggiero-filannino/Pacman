import os
import sys
import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk
import time
import re
from pyswip import Prolog

"""---------------------------------------------------------------
PAC-MAN – Alla conquista del Labirinto

gui.py – Interfaccia Grafica del progetto "Pacman - Alla conquista del Labirinto"

Questa GUI sviluppata con Tkinter permette all'utente di:
- navigare tra menu, storia e selezione degli algoritmi AI
- avviare l'esecuzione degli algoritmi (DFS, A*, Ricerca Bidirezionale) su una mappa 12x12
- visualizzare graficamente il labirinto, il percorso ottimale calcolato dall'AI
- animare il percorso di Pacman e mostrare statistiche dettagliate

Integrazione logica: la GUI comunica con la KB Prolog tramite pyswip (SWI-Prolog embedded).
Autore: Ruggiero Filannino - Matricola 797150

---------------------------------------------------------------

"""

# ------------------------------------------------------------------
#  CONFIGURAZIONE GRAFICA SWAG
# ------------------------------------------------------------------
CELL_SIZE = 45
BORDER_WIDTH = 2
SHADOW_OFFSET = 3

# Palette Pacman autentica
COLORS = {
    ".": {"bg": "#000000", "border": "#1a1a2e", "shadow": "#0a0a14"},   # Black maze bg
    "#": {"bg": "#2121DE", "border": "#0000FF", "shadow": "#14148B"},   # Pacman blue walls
    "L": {"bg": "#FF4500", "border": "#FF6347", "shadow": "#DC143C"},   # Lava
    "R": {"bg": "#FF0000", "border": "#DC143C", "shadow": "#B22222"},   # Blinky red ghost (R)
    "*": {"bg": "#FFD700", "border": "#FFA500", "shadow": "#FF8C00"},   # Golden path
    "P": {"bg": "#FFD700", "border": "#FFA500", "shadow": "#B8860B"},   # Pacman yellow (P)
    "G": {"bg": "#FF69B4", "border": "#FF1493", "shadow": "#DC143C"},   # Goal / fruit pink (G)
    "K": {"bg": "#FFB6C1", "border": "#FF69B4", "shadow": "#C71585"},   # Pinky pink ghost (K)
    "I": {"bg": "#00FFFF", "border": "#00CED1", "shadow": "#008B8B"},   # Inky cyan ghost (I)
    "C": {"bg": "#FF8C00", "border": "#FFA500", "shadow": "#CC7000"}    # Clyde orange ghost (C)
}

# Colori tema Pacman
PACMAN_YELLOW = "#FFD700"
PACMAN_BLACK = "#000000"
PACMAN_BLUE = "#2121DE"
PACMAN_GREEN = "#00FF00"
DARK_BG = "#0a0a14"
CARD_BG = "#111122"

# ------------------------------------------------------------------
class PacmanSwagGUI(tk.Tk):
    """Costruisce la finestra principale e inizializza tutti i componenti GUI"""
    def __init__(self):
        super().__init__()
        self.title("👾 Pacman AI Quest - Labirinto Edition 👾")
        self.geometry("1600x1000")
        self.configure(bg=DARK_BG)
        self.resizable(True, True)
        
        # Game state
        self.current_screen = "menu"
        self.animation_running = False
        self.path_points = []
        self.current_step = 0
        self.current_map = []
        self.stats_data = {}
        
        # Setup Prolog
        self.prolog = Prolog()
        self._setup_prolog()
        
        # Build screens
        self._setup_styles()
        self._build_screens()
        self._show_menu()

    def _setup_prolog(self):
        kb_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "prolog", "KB.pl").replace("\\", "/")
        try:
            list(self.prolog.query(f"consult('{kb_path}')"))
        except Exception as e:
            messagebox.showerror("Errore Prolog", f"Impossibile consultare KB.pl:\n{e}")
            sys.exit(1)

    def _setup_styles(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        
        # Custom styles
        style.configure("Title.TLabel", 
                       font=("Impact", 32, "bold"), 
                       foreground=PACMAN_YELLOW, 
                       background=DARK_BG)
        
        style.configure("Story.TLabel", 
                       font=("Arial", 14), 
                       foreground="white", 
                       background=CARD_BG,
                       wraplength=600)

    def _build_screens(self):
        # Menu principale
        self.menu_frame = tk.Frame(self, bg=DARK_BG)
        self._build_menu_screen()
        
        # Schermata storia
        self.story_frame = tk.Frame(self, bg=DARK_BG)
        self._build_story_screen()
        
        # Schermata algoritmi
        self.algorithm_frame = tk.Frame(self, bg=DARK_BG)
        self._build_algorithm_screen()
        
        # Schermata gioco
        self.game_frame = tk.Frame(self, bg=DARK_BG)
        self._build_game_screen()

    def _build_menu_screen(self):
        # Background gradient effect
        self._create_gradient_bg(self.menu_frame)
        
        # Main container
        main_container = tk.Frame(self.menu_frame, bg=DARK_BG)
        main_container.pack(expand=True, fill=tk.BOTH)
        
        # Title section with 3D effect
        title_frame = tk.Frame(main_container, bg=DARK_BG)
        title_frame.pack(expand=True, fill=tk.BOTH)
        
        # 3D Title effect
        shadow_label = tk.Label(title_frame, text="👾 PAC-MAN 👾", 
                               font=("Impact", 48, "bold"), 
                               fg="#8B0000", bg=DARK_BG)
        shadow_label.place(relx=0.502, rely=0.252, anchor="center")
        
        main_title = tk.Label(title_frame, text="👾 PAC-MAN 👾", 
                             font=("Impact", 48, "bold"), 
                             fg=PACMAN_YELLOW, bg=DARK_BG)
        main_title.place(relx=0.5, rely=0.25, anchor="center")
        
        subtitle = tk.Label(title_frame, text="A.I. PATHFINDING LABIRINTO", 
                           font=("Arial", 18, "bold"), 
                           fg="#FF0000", bg=DARK_BG)
        subtitle.place(relx=0.5, rely=0.32, anchor="center")
        
        # Animated pellets
        self._create_floating_pellets(title_frame)
        
        # Button panel
        button_panel = tk.Frame(main_container, bg=CARD_BG, relief="raised", bd=5)
        button_panel.pack(pady=50)
        
        # Play button - Pacman style
        play_btn = tk.Button(button_panel, text="👾 PLAY GAME", 
                            font=("Arial", 20, "bold"),
                            bg=PACMAN_YELLOW, fg="black", 
                            relief="raised", bd=8,
                            padx=40, pady=15,
                            cursor="hand2",
                            command=self._show_story)
        play_btn.pack(pady=20, padx=30)
        
        # Exit button
        exit_btn = tk.Button(button_panel, text="❌ EXIT", 
                            font=("Arial", 16, "bold"),
            bg="#FF0000", fg="white", 
                            relief="raised", bd=6,
                            padx=30, pady=10,
                            cursor="hand2",
                            command=self.destroy)
        exit_btn.pack(pady=10, padx=30)
        
        # Add hover effects
        self._add_button_effects(play_btn)
        self._add_button_effects(exit_btn)

    def _build_story_screen(self):
        # Background
        self._create_gradient_bg(self.story_frame)
        
        # Story container
        story_container = tk.Frame(self.story_frame, bg=CARD_BG, relief="raised", bd=10)
        story_container.pack(expand=True, fill=tk.BOTH, padx=50, pady=50)
        
        # Title
        story_title = tk.Label(story_container, text="📜 LA STORIA INIZIA... 📜", 
                            font=("Impact", 24, "bold"), 
                            fg=PACMAN_YELLOW, bg=CARD_BG)
        story_title.pack(pady=20)
        
        # Story text with scrolling - FIXED: Added height limit and scrollbar
        story_text_frame = tk.Frame(story_container, bg=CARD_BG)
        story_text_frame.pack(expand=True, fill=tk.BOTH, padx=30, pady=20)
        
        story_content = """
    👾 C'era una volta un grande labirinto...

Nel profondo del regno dei videogiochi, un labirinto oscuro è stato popolato da quattro fantasmi malefici:

💀 BLINKY, PINKY, INKY e CLYDE! 💀

Questi fantasmi pattugliano i corridoi del labirinto, pronti a catturare chiunque osi entrare.
Ma nel labirinto si nasconde anche la potente SUPER PILLOLA, una sfera luminosa in grado di donare un potere immenso a chi la raggiunge!

• 🧱 Muri blu che delimitano i corridoi  
• 🔥 Pozze di lava mortale  
• 🔴 Blinky - Il fantasma rosso che insegue direttamente
• 🩷 Pinky - Il fantasma rosa che tenta agguati
• 🩵 Inky - Il fantasma ciano dall'imprevedibilità totale
• 🟠 Clyde - Il fantasma arancione timido ma ostinato

🟡 Ma niente paura! PAC-MAN è qui per affrontare la sfida!

Il nostro eroe giallo dovrà attraversare questo labirinto insidioso per raggiungere la Super Pillola.
Ma questa non è una semplice corsa – Pacman userà il potere dell'INTELLIGENZA ARTIFICIALE!

Devi scegliere quale algoritmo guiderà Pacman nel labirinto:

🔍 RICERCA IN PROFONDITÀ – Audace ma talvolta imprudente  
🌊 RICERCA BIDIREZIONALE – Attenta e metodica  
⭐ ALGORITMO A* – Intelligente ed efficiente

Il punteggio più alto è nelle tue mani!

Aiuterai Pacman a scegliere il percorso migliore verso la vittoria? 🏆
        """
        
        # Use ScrolledText instead of Label to handle long text properly
        from tkinter import scrolledtext
        
        story_text = scrolledtext.ScrolledText(
            story_text_frame, 
            wrap=tk.WORD,
            height=15,  # Fixed height to ensure buttons are visible
            font=("Arial", 12), 
            fg="white", 
            bg=CARD_BG,
            relief="flat",
            bd=0,
            highlightthickness=0
        )
        story_text.pack(expand=True, fill=tk.BOTH, pady=10)
        story_text.insert("1.0", story_content.strip())
        story_text.config(state=tk.DISABLED)  # Make it read-only
        
        # Continue button - This will now be visible!
        continue_btn = tk.Button(story_container, text="🚀 CONTINUA LA MISSIONE", 
                                font=("Arial", 16, "bold"),
                                bg=PACMAN_BLUE, fg="white", 
                                relief="raised", bd=6,
                                padx=30, pady=15,
                                cursor="hand2",
                                command=self._show_algorithm_selection)
        continue_btn.pack(pady=20)
        
        # Back button
        back_btn = tk.Button(story_container, text="← Torna al MENU", 
                            font=("Arial", 12),
                            bg="#666666", fg="white", 
                            relief="raised", bd=4,
                            padx=20, pady=8,
                            cursor="hand2",
                            command=self._show_menu)
        back_btn.pack(pady=10)
        
        self._add_button_effects(continue_btn)
        self._add_button_effects(back_btn)

    def _build_algorithm_screen(self):
        # Background
        self._create_gradient_bg(self.algorithm_frame)
        
        # Main container
        main_container = tk.Frame(self.algorithm_frame, bg=CARD_BG, relief="raised", bd=10)
        main_container.pack(expand=True, fill=tk.BOTH, padx=30, pady=30)
        
        # Title
        title = tk.Label(main_container, text="🧠 Scegli il tuo algoritmo 🧠", 
                        font=("Impact", 24, "bold"), 
                        fg=PACMAN_YELLOW, bg=CARD_BG)
        title.pack(pady=30)
        
        # Subtitle
        subtitle = tk.Label(main_container, text="Scegli l'algoritmo che guiderà Pacman alla vittoria!", 
                           font=("Arial", 14), 
                           fg="white", bg=CARD_BG)
        subtitle.pack(pady=10)
        
        # Algorithm cards container
        cards_container = tk.Frame(main_container, bg=CARD_BG)
        cards_container.pack(expand=True, fill=tk.BOTH, pady=30)
        
        # Dati degli algoritmi
        algorithms = [
            {
                "name": "🔍 RICERCA IN\nPROFONDITÀ",
                "description": "Esplora prima i percorsi più profondi.\nVeloce ma non sempre ottimale.\nIdeale per labirinti con pochi vicoli ciechi.",
                "query": "pacman_dfs_gui(Output)",
                "color": "#FF0000",
                "icon": "🔍"
            },
            {
                "name": "🌊 RICERCA\nBIDIREZIONALE", 
                "description": "Parte sia dalla partenza che dall'arrivo.\nRiduce lo spazio di ricerca.\nEfficace nei labirinti di grandi dimensioni.",
                "query": "pacman_bd_gui(Output)",
                "color": "#2121DE",
                "icon": "🌊"
            },
            {
                "name": "⭐ ALGORITMO A*",
                "description": "Utilizza euristiche intelligenti.\nEquilibrio tra velocità e ottimalità.\nLa scelta più intelligente!",
                "query": "pacman_astar_gui(Output)",
                "color": "#00FF00",
                "icon": "⭐"
            }
        ]

        # Create algorithm cards
        for i, algo in enumerate(algorithms):
            card = self._create_algorithm_card(cards_container, algo)
            card.grid(row=0, column=i, padx=20, pady=20, sticky="nsew")
        
        # Configure grid
        cards_container.grid_columnconfigure(0, weight=1)
        cards_container.grid_columnconfigure(1, weight=1)
        cards_container.grid_columnconfigure(2, weight=1)
        
        # Back button
        back_btn = tk.Button(main_container, text="← Torna alla STORIA", 
                            font=("Arial", 12),
                            bg="#666666", fg="white", 
                            relief="raised", bd=4,
                            padx=20, pady=8,
                            cursor="hand2",
                            command=self._show_story)
        back_btn.pack(pady=20)
        
        self._add_button_effects(back_btn)

    def _create_algorithm_card(self, parent, algo_data):
        # Card frame
        card = tk.Frame(parent, bg=algo_data["color"], relief="raised", bd=8)
        
        # Icon
        icon_label = tk.Label(card, text=algo_data["icon"], 
                             font=("Arial", 48), 
                             fg="white", bg=algo_data["color"])
        icon_label.pack(pady=15)
        
        # Name
        name_label = tk.Label(card, text=algo_data["name"], 
                             font=("Arial", 14, "bold"), 
                             fg="white", bg=algo_data["color"],
                             justify="center")
        name_label.pack(pady=10)
        
        # Description
        desc_label = tk.Label(card, text=algo_data["description"], 
                             font=("Arial", 10), 
                             fg="white", bg=algo_data["color"],
                             justify="center", wraplength=200)
        desc_label.pack(pady=15, padx=15)
        
        # Select button
        select_btn = tk.Button(card, text="SELEZIONA!", 
                              font=("Arial", 12, "bold"),
                              bg="white", fg=algo_data["color"], 
                              relief="raised", bd=4,
                              padx=20, pady=8,
                              cursor="hand2",
                              command=lambda: self._run_algorithm(algo_data["query"]))
        select_btn.pack(pady=15)
        
        self._add_button_effects(select_btn)
        
        # Card hover effect
        def on_enter(e):
            card.config(relief="sunken", bd=6)
        
        def on_leave(e):
            card.config(relief="raised", bd=8)
        
        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)
        
        return card

    def _build_game_screen(self):
        # Header
        header = tk.Frame(self.game_frame, bg=CARD_BG, height=80)
        header.pack(fill=tk.X, padx=10, pady=5)
        header.pack_propagate(False)
        
        # Back button
        back_btn = tk.Button(header, text="← Torna agli algoritmi", 
                            font=("Arial", 12),
                            bg="#666666", fg="white", 
                            relief="raised", bd=4,
                            padx=15, pady=5,
                            cursor="hand2",
                            command=self._show_algorithm_selection)
        back_btn.pack(side=tk.LEFT, padx=10, pady=15)
        
        # Mission status
        mission_label = tk.Label(header, text="🎯 Missione: Raggiungere la Super Pillola", 
                                font=("Arial", 18, "bold"), 
                                fg=PACMAN_YELLOW, bg=CARD_BG)
        mission_label.pack(pady=20)
        
        # Main content
        main_content = tk.Frame(self.game_frame, bg=DARK_BG)
        main_content.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        
        # Canvas for maze (keeping your beautiful maze!)
        canvas_frame = tk.Frame(main_content, bg=CARD_BG, relief="raised", bd=5)
        canvas_frame.pack(side=tk.LEFT, padx=10, pady=10)
        
        self.canvas = tk.Canvas(canvas_frame, bg="#000000", highlightthickness=0)
        self.canvas.pack(padx=5, pady=5)
        
        # Info panel
        info_frame = tk.Frame(main_content, bg=CARD_BG, width=350, relief="raised", bd=5)
        info_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)
        info_frame.pack_propagate(False)
        
        # Legend
        legend_label = tk.Label(info_frame, text="🗺️ LEGENDA LABIRINTO", 
                               font=("Arial", 16, "bold"), 
                               fg=PACMAN_YELLOW, bg=CARD_BG)
        legend_label.pack(pady=15)
        
        self._create_legend(info_frame)
        
        # Stats
        self.stats_frame = tk.Frame(info_frame, bg=CARD_BG)
        self.stats_frame.pack(pady=20, fill=tk.X, padx=10)
        
        # Console
        console_frame = tk.Frame(self.game_frame, bg=DARK_BG)
        console_frame.pack(fill=tk.X, padx=10, pady=5)
        
        console_label = tk.Label(console_frame, text="🖥️ Log:", 
                                font=("Arial", 12, "bold"), 
                                fg=PACMAN_GREEN, bg=DARK_BG)
        console_label.pack(anchor="w")
        
        self.console = scrolledtext.ScrolledText(
            console_frame, height=8, font=("Consolas", 9), 
            bg="#001100", fg="#00ff00", insertbackground="#00ff00",
            relief="sunken", bd=3)
        self.console.pack(fill=tk.X)
        
        self._add_button_effects(back_btn)

    def _create_legend(self, parent):
        legend_items = [
            ("🟡 Pacman", "P", PACMAN_YELLOW),
            ("🍒 Super Pillola", "G", "#FF69B4"),
            ("⭐ Percorso AI", "*", PACMAN_YELLOW),
            ("🔵 Muro Labirinto", "#", "#2121DE"),
            ("🔥 Lava", "L", "#FF4500"),
            ("🔴 Blinky (Rosso)", "R", "#FF0000"),
            ("🩷 Pinky (Rosa)", "K", "#FFB6C1"),
            ("🩵 Inky (Ciano)", "I", "#00FFFF"),
            ("🟠 Clyde (Arancione)", "C", "#FF8C00"),
            ("⬛ Casella Vuota", ".", "#000000")
        ]

        
        for text, symbol, color in legend_items:
            item_frame = tk.Frame(parent, bg=CARD_BG)
            item_frame.pack(fill=tk.X, padx=15, pady=3)
            
            # Color indicator
            color_box = tk.Label(item_frame, text="  ", bg=color, width=3, relief="raised", bd=2)
            color_box.pack(side=tk.LEFT, padx=8)
            
            # Text
            tk.Label(item_frame, text=text, font=("Arial", 10), 
                    fg="white", bg=CARD_BG).pack(side=tk.LEFT, padx=8)

    def _create_gradient_bg(self, parent):
        # Create a simple gradient effect using overlapping frames
        for i in range(10):
            alpha = i / 10.0
            color_val = int(26 + (42 - 26) * alpha)  # Gradient from dark to slightly lighter
            color = f"#{color_val:02x}{color_val:02x}{color_val + 20:02x}"
            
            gradient_frame = tk.Frame(parent, bg=color, height=100)
            gradient_frame.place(relx=0, rely=i/10.0, relwidth=1, relheight=0.1)

    def _create_floating_pellets(self, parent):
        # Add some decorative pellets
        pellet_positions = [(0.2, 0.4), (0.8, 0.4), (0.15, 0.6), (0.85, 0.6)]
        
        for x, y in pellet_positions:
            pellet = tk.Label(parent, text="⚪", font=("Arial", 18), fg=PACMAN_YELLOW, bg=DARK_BG)
            pellet.place(relx=x, rely=y, anchor="center")
            
            # Simple animation
            self._animate_pellet(pellet)

    def _animate_pellet(self, pellet):
        def float_up():
            current_y = pellet.winfo_y()
            pellet.place(y=current_y - 2)
            self.after(100, float_down)
        
        def float_down():
            current_y = pellet.winfo_y()
            pellet.place(y=current_y + 2)
            self.after(100, float_up)
        
        self.after(1000, float_up)

    def _add_button_effects(self, button):
        original_bg = button.cget("bg")
        
        def on_enter(e):
            button.config(relief="sunken", bd=button.cget("bd") - 2)
        
        def on_leave(e):
            button.config(relief="raised", bd=button.cget("bd") + 2)
        
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)

    # Screen navigation methods
    def _show_menu(self):
        self._hide_all_screens()
        self.menu_frame.pack(expand=True, fill=tk.BOTH)
        self.current_screen = "menu"

    def _show_story(self):
        self._hide_all_screens()
        self.story_frame.pack(expand=True, fill=tk.BOTH)
        self.current_screen = "story"

    def _show_algorithm_selection(self):
        self._hide_all_screens()
        self.algorithm_frame.pack(expand=True, fill=tk.BOTH)
        self.current_screen = "algorithm"

    def _show_game(self):
        self._hide_all_screens()
        self.game_frame.pack(expand=True, fill=tk.BOTH)
        self.current_screen = "game"

    def _hide_all_screens(self):
        self.menu_frame.pack_forget()
        self.story_frame.pack_forget()
        self.algorithm_frame.pack_forget()
        self.game_frame.pack_forget()

    # Algorithm execution methods (keeping your original logic)
    def _run_algorithm(self, query):
        self._show_game()
        
        self.console.delete("1.0", tk.END)
        self.canvas.delete("all")
        self._clear_stats()
        
        # Reset state
        self.animation_running = False
        self.path_points = []
        self.current_map = []
        
        # Reset Prolog state
        list(self.prolog.query("retractall(percorso_memorizzato(_))"))
        
        self.console.insert(tk.END, f"🚀 Pacman si prepara...\n")
        self.console.insert(tk.END, f"🧠 Eseguendo: {query}\n")
        self.console.insert(tk.END, "⏳ Cercando il percorso ottimale...\n")
        self.update()
        
        try:
            start_time = time.time()
            result = next(self.prolog.query(query))
            end_time = time.time()
            
            self.console.insert(tk.END, f"✅ Missione completata in {end_time-start_time:.3f}s\n")
            self.console.insert(tk.END, f"🎯 Pacman ha trovato un percorso per la Super Pillola\n")
            
            # Extract path in correct order from Prolog
            path_result = list(self.prolog.query("percorso_memorizzato(Path)"))
            if path_result:
                path = path_result[0]['Path']
                self.path_points = []
                for step in path:
                    r, c = step
                    x = c * CELL_SIZE + CELL_SIZE // 2 + 10
                    y = r * CELL_SIZE + CELL_SIZE // 2 + 10
                    self.path_points.append((x, y))
            
            # Parse and draw map (keeping your original logic)
            output_text = str(result['Output'])
            self.console.insert(tk.END, f"📊 A.I. Analysis:\n{output_text}\n")
            
            success = self._parse_and_draw_map(output_text)
            if success:
                self._update_stats(end_time - start_time, output_text)
                self.console.insert(tk.END, f"🏆 SUCCESS! Super Pillola raggiunta!\n")
            else:
                self.console.insert(tk.END, "⚠️ Could not parse maze from A.I. output\n")
            
        except StopIteration:
            self.console.insert(tk.END, "❌ No solution found! La Super Pillola è irraggiungibile!\n")
            messagebox.showinfo("Mission Failed", "The A.I. could not find a path to the Super Pillola!")
        except Exception as e:
            self.console.insert(tk.END, f"💥 A.I. System Error: {str(e)}\n")
            messagebox.showerror("System Error", f"A.I. algorithm failed:\n{e}")

    # Keep all your original maze parsing and drawing methods
    def _parse_and_draw_map(self, output_text):
        """Parsifica l'output ASCII del Prolog e disegna la mappa"""
        try:
            # Search for solution section (with asterisks for path)
            solution_pattern = r"--- Soluzione.*?Trovata! ---\s*\n.*?\n.*?\n((?:\s*\d.*?\n)+)"
            solution_match = re.search(solution_pattern, output_text, re.DOTALL)
            
            if solution_match:
                map_text = solution_match.group(1)
                self.console.insert(tk.END, "🎯 A.I. found optimal solution path!\n")
            else:
                # Fallback: use initial generated map
                initial_pattern = r"--- Mappa Generata ---\s*\n.*?\n.*?\n((?:\s*\d.*?\n)+)"
                initial_match = re.search(initial_pattern, output_text, re.DOTALL)
                if initial_match:
                    map_text = initial_match.group(1)
                    self.console.insert(tk.END, "🗺️ Using initial maze layout\n")
                else:
                    return False
            
            # Parse map lines
            map_lines = [line.strip() for line in map_text.strip().split('\n') if line.strip()]
            self.current_map = []
            
            # Only collect raster path_points if not already set from Prolog
            if not self.path_points:
                self.path_points = []
            
            for row_idx, line in enumerate(map_lines):
                if '|' in line:
                    content = line.split('|')[1]
                    content = content.replace(' ', '')
                    
                    map_row = []
                    for col_idx, char in enumerate(content):
                        if char in COLORS:
                            map_row.append(char)
                            if char == '*' and not self.path_points:
                                x = col_idx * CELL_SIZE + CELL_SIZE // 2 + 10
                                y = row_idx * CELL_SIZE + CELL_SIZE // 2 + 10
                                self.path_points.append((x, y))
                    
                    if map_row:
                        self.current_map.append(map_row)
            
            if self.current_map:
                self._draw_parsed_map()
                return True
            
            return False
            
        except Exception as e:
            self.console.insert(tk.END, f"❌ Parse error: {str(e)}\n")
            return False

    def _draw_parsed_map(self):
        """Draw the parsed map with enhanced graphics"""
        if not self.current_map:
            return
            
        rows = len(self.current_map)
        cols = max(len(row) for row in self.current_map) if self.current_map else 8
        
        canvas_width = cols * CELL_SIZE + 20
        canvas_height = rows * CELL_SIZE + 20
        self.canvas.config(width=canvas_width, height=canvas_height)
        
        # Draw background
        self.canvas.create_rectangle(0, 0, canvas_width, canvas_height, 
                                   fill="#0F0F23", outline="")
        
        # Draw grid
        grid_color = "#2F4F4F"
        for i in range(cols + 1):
            x = i * CELL_SIZE + 10
            self.canvas.create_line(x, 10, x, canvas_height - 10, 
                                  fill=grid_color, width=1)
        
        for i in range(rows + 1):
            y = i * CELL_SIZE + 10
            self.canvas.create_line(10, y, canvas_width - 10, y, 
                                  fill=grid_color, width=1)
        
        # Draw cells
        for row_idx, row in enumerate(self.current_map):
            for col_idx, symbol in enumerate(row):
                x = col_idx * CELL_SIZE + 10
                y = row_idx * CELL_SIZE + 10
                self._draw_enhanced_cell(x, y, symbol)
        
        # Start path animation
        if self.path_points:
            self.console.insert(tk.END, f"✨ Animating Pacman's journey with {len(self.path_points)} steps\n")
            self.after(1000, self._animate_path)

    def _draw_enhanced_cell(self, x, y, symbol):
        """Draw a single cell with advanced effects"""
        colors = COLORS.get(symbol, COLORS["."])
        
        # Draw shadow
        shadow_x = x + SHADOW_OFFSET
        shadow_y = y + SHADOW_OFFSET
        self.canvas.create_rectangle(shadow_x, shadow_y, 
                                   shadow_x + CELL_SIZE, shadow_y + CELL_SIZE,
                                   fill=colors["shadow"], outline="")
        
        # Draw main cell
        self.canvas.create_rectangle(x, y, x + CELL_SIZE, y + CELL_SIZE,
                                   fill=colors["bg"], outline=colors["border"],
                                   width=BORDER_WIDTH)
        
        # Add highlight for 3D effect
        highlight_color = self._lighten_color(colors["bg"])
        self.canvas.create_line(x, y, x + CELL_SIZE, y, fill=highlight_color, width=2)
        self.canvas.create_line(x, y, x, y + CELL_SIZE, fill=highlight_color, width=2)
        
        # Add symbols/emojis
        center_x = x + CELL_SIZE // 2
        center_y = y + CELL_SIZE // 2
        
        symbols_map = {
            "P": ("🟡", "yellow"),    # Pacman
            "G": ("🍒", "pink"),      # Goal / Super Pillola
            "*": ("⭐", "white"),     # AI Path
            "#": ("🔵", "blue"),      # Wall
            "L": ("🔥", "orange"),    # Lava
            "R": ("👻", "red"),       # Blinky (red ghost)
            "K": ("👻", "pink"),      # Pinky (pink ghost)
            "I": ("👻", "cyan"),      # Inky (cyan ghost)
            "C": ("👻", "orange"),    # Clyde (orange ghost)
        }

        
        if symbol in symbols_map:
            emoji, text_color = symbols_map[symbol]
            self.canvas.create_text(center_x, center_y, 
                                  text=emoji, 
                                  font=("Arial", 18), 
                                  fill=text_color)

    def _lighten_color(self, color_hex):
        """Lighten a hex color for highlight effect"""
        try:
            color_hex = color_hex.lstrip('#')
            r, g, b = tuple(int(color_hex[i:i+2], 16) for i in (0, 2, 4))
            r = min(255, r + 40)
            g = min(255, g + 40)  
            b = min(255, b + 40)
            return f"#{r:02x}{g:02x}{b:02x}"
        except:
            return "#FFFFFF"

    def _animate_path(self):
        """Start path animation"""
        if not self.path_points:
            return
            
        self.animation_running = True
        self.current_step = 0
        self.console.insert(tk.END, "🏃‍♂️ Pacman sta correndo verso la Super Pillola!\n")
        self._animate_step()

    def _animate_step(self):
        """Animate a single step of the path"""
        if not self.animation_running or self.current_step >= len(self.path_points):
            self.animation_running = False
            if self.current_step >= len(self.path_points):
                self.console.insert(tk.END, "🎊 MISSIONE COMPLETATA! Super Pillola raggiunta!\n")
            return
            
        # Remove previous animations
        self.canvas.delete("animation")
        
        # Draw all points up to current step
        for i in range(min(self.current_step + 1, len(self.path_points))):
            x, y = self.path_points[i]
            
            # Pulsing effect for current point
            if i == self.current_step:
                for radius in [15, 12, 9, 6]:
                    alpha = 1.0 - ((15 - radius) * 0.2)
                    color = f"#{'%02x' % int(255 * alpha)}{'%02x' % int(215 * alpha)}00"
                    
                    self.canvas.create_oval(x - radius, y - radius, 
                                          x + radius, y + radius,
                                          fill=color, outline="", 
                                          tags="animation")
            else:
                # Already visited points
                self.canvas.create_oval(x - 4, y - 4, x + 4, y + 4,
                                      fill=PACMAN_YELLOW, outline="#FFA500", 
                                      width=2, tags="animation")
        
        self.current_step += 1
        self.after(300, self._animate_step)

    def _update_stats(self, execution_time, output_text):
        """Update displayed statistics"""
        # Clear previous stats
        for widget in self.stats_frame.winfo_children():
            widget.destroy()
            
        # Extract statistics from output
        path_length = len(self.path_points)
        
        # Search for length and cost in output
        length_match = re.search(r"Lunghezza percorso:\s*(\d+)", output_text)
        cost_match = re.search(r"Costo totale:\s*(\d+)", output_text)
        
        length_text = length_match.group(1) if length_match else str(path_length)
        cost_text = cost_match.group(1) if cost_match else "N/A"
        
        # Stats title
        tk.Label(self.stats_frame, text="📊 STATISTICHE MISSIONE", 
                font=("Arial", 14, "bold"), 
                fg=PACMAN_YELLOW, bg=CARD_BG).pack(pady=10)
        
        stats = [
            f"⏱️ Tempo AI: {execution_time:.3f}s",
            f"🎯 Passi Percorso: {path_length}",
            f"📏 Lunghezza: {length_text}",
            f"💰 Costo Totale: {cost_text}",
            f"🗺️ Dimensione Mappa: {len(self.current_map)}x{len(self.current_map[0]) if self.current_map else 0}"
        ]
        
        for stat in stats:
            tk.Label(self.stats_frame, text=stat, 
                    font=("Arial", 10), 
                    fg="white", bg=CARD_BG).pack(pady=2, anchor="w", padx=10)
        
        # Mission status
        status_frame = tk.Frame(self.stats_frame, bg=PACMAN_GREEN, relief="raised", bd=3)
        status_frame.pack(pady=15, padx=10, fill=tk.X)
        
        tk.Label(status_frame, text="🏆 STATO MISSIONE", 
                font=("Arial", 12, "bold"), 
                fg="black", bg=PACMAN_GREEN).pack(pady=5)
        
        tk.Label(status_frame, text="SUPER PILLOLA\nRAGGIUNTA!", 
                font=("Arial", 10, "bold"), 
                fg="black", bg=PACMAN_GREEN,
                justify="center").pack(pady=5)

    def _clear_stats(self):
        """Clear statistics display"""
        for widget in self.stats_frame.winfo_children():
            widget.destroy()

# ------------------------------------------------------------------
if __name__ == "__main__":
    try:
        app = PacmanSwagGUI()
        app.mainloop()
    except Exception as e:
        print(f"Application error: {e}")
        sys.exit(1)