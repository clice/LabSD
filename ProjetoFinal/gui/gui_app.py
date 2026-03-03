"""
gui_app.py

Ponto de entrada da Interface Gráfica (GUI).
Esta classe representa a Camada de Apresentação na arquitetura N-Camadas.

Responsável por:
- Criar janela principal
- Gerenciar navegação entre telas
- Integrar com ClientCore
"""

import customtkinter as ctk
from client.client_core import ClientCore


class CinemaApp(ctk.CTk):
    """
    Classe principal da aplicação gráfica.

    Herda de CTk (CustomTkinter),
    que é uma versão moderna do Tkinter.
    """
    
    def __init__(self):
        super().__init__()
        
        self.title("Sistema de Cinema Distribuído")
        self.geometry("900x600")
        
        # Inicializa cliente
        self.core = ClientCore()
        
        if not self.core.connect():
            print("Erro ao conectar ao servidor.")
            
        # Layout principal
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=200)
        self.sidebar.grid(row=0, column=0, sticky="ns")
        
        # Área principal
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=1, sticky="nsew")
        
        # Botões de navegação
        self.create_sidebar_buttons()
        
    
    # ======================================================
    # Criação dos Botões Laterais
    # ======================================================
    
    def create_sidebar_buttons(self):
        """
        Cria botões que controlam a navegação entre telas.
        """
        
        ctk.CTkButton(
            self.sidebar,
            text="Filmes",
            command=self.show_movies
        ).pack(pady=10)

        ctk.CTkButton(
            self.sidebar,
            text="Comprar",
            command=self.show_buy
        ).pack(pady=10)

        ctk.CTkButton(
            self.sidebar,
            text="Minhas Compras",
            command=self.show_purchases
        ).pack(pady=10)
        
    
    # ======================================================
    # Controle de Navegação
    # ======================================================
    
    def clear_main_frame(self):
        """
        Remove todos os widgets da área principal.

        Isso permite que uma nova tela seja carregada
        dinamicamente.
        """
        
        for widget in self.main_frame.winfo_children():
            widget.destroy()


    def show_movies(self):
        """
        Carrega tela de listagem de filmes.
        """
        
        from gui.screens.movies_screen import MoviesScreen
        self.clear_main_frame()
        MoviesScreen(self.main_frame, self.core)


    def show_buy(self):
        """
        Carrega tela de compra.
        """
        
        from gui.screens.buy_screen import BuyScreen
        self.clear_main_frame()
        BuyScreen(self.main_frame, self.core)

    def show_purchases(self):
        """
        Carrega tela de visualização de compras.
        """
        
        from gui.screens.purchases_screen import PurchasesScreen
        self.clear_main_frame()
        PurchasesScreen(self.main_frame, self.core)


if __name__ == "__main__":
    app = CinemaApp()
    app.mainloop()
        