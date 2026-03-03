"""
movies_screen.py

Tela responsável por exibir os filmes disponíveis.

Esta classe:
- Não contém lógica de negócio
- Apenas solicita dados ao ClientCore
- Renderiza informações na interface
"""

import customtkinter as ctk


class MoviesScreen:
    
    def __init__(self, parent, core):
        """
        parent: frame principal da aplicação
        core: instância de ClientCore
        """
        
        self.core = core
        
        # Frame da tela
        self.frame = ctk.CTkFrame(parent)
        self.frame.pack(fill="both", expand=True)
        
        # Título
        title = ctk.CTkLabel(
            self.frame,
            text="Filmes Disponíveis",
            font=("Arial", 2)
        )
        title.pack(pady=20)

        # Carrega dados
        self.load_movies()


    def load_movies(self):
        """
        Solicita filmes ao servidor e renderiza na tela.
        """

        result = self.core.list_movies()

        if result["status"] == "success":

            for movie in result["data"]:
                text = f"{movie[0]} - {movie[1]} ({movie[2]})"
                ctk.CTkLabel(self.frame, text=text).pack(anchor="w", padx=20)

        else:
            ctk.CTkLabel(
                self.frame,
                text=result["message"]
            ).pack()