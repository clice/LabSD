"""
purchases_screen.py

Tela responsável por permitir que o cliente visualize
todas as suas compras anteriores.

- Coleta o e-mail do usuário
- Solicita os dados ao ClientCore
- Renderiza os resultados na interface
"""

import customtkinter as ctk


class PurchasesScreen:
    """
    Tela que exibe histórico de compras do cliente.

    Recebe:
        parent: frame principal onde será renderizada
        core: instância de ClientCore (camada intermediária)
    """

    def __init__(self, parent, core):

        self.core = core

        # Frame principal da tela
        self.frame = ctk.CTkFrame(parent)
        self.frame.pack(fill="both", expand=True)

        ctk.CTkLabel(
            self.frame,
            text="Minhas Compras",
            font=("Arial", 20)
        ).pack(pady=20)

        # Campo para o usuário inserir o e-mail
        self.email_entry = ctk.CTkEntry(
            self.frame,
            placeholder_text="Digite seu email"
        )
        self.email_entry.pack(pady=5)

        # Botão para buscar compras
        ctk.CTkButton(
            self.frame,
            text="Buscar",
            command=self.load_purchases
        ).pack(pady=10)

        self.result_frame = ctk.CTkFrame(self.frame)
        self.result_frame.pack(fill="both", expand=True)


    # ======================================================
    # Carregamento das Compras
    # ======================================================
    
    def load_purchases(self):
        """
        Executa consulta ao servidor para recuperar
        compras associadas ao e-mail informado.

        Fluxo:
        1) Limpa resultados anteriores
        2) Solicita dados ao ClientCore
        3) Renderiza dados retornados
        """

        for widget in self.result_frame.winfo_children():
            widget.destroy()

        result = self.core.get_purchases_by_email(self.email_entry.get())

        # Tratamento da resposta
        if result["status"] == "success":

            purchases = result["data"]

            # Caso não existam compras
            if not purchases:
                ctk.CTkLabel(
                    self.result_frame,
                    text="Nenhuma compra encontrada."
                ).pack(pady=10)
                return
            
            # Renderizar cada compra
            for purchase in purchases:
                """
                purchase contém:
                    purchase[0] → título do filme
                    purchase[1] → horário da sessão
                    purchase[2] → quantidade
                    purchase[3] → timestamp da compra
                """

                text = (
                    f"Filme: {purchase[0]} | "
                    f"Horário: {purchase[1]} | "
                    f"Quantidade: {purchase[2]} | "
                    f"Data: {purchase[3]}"
                )

                ctk.CTkLabel(
                    self.result_frame,
                    text=text,
                    anchor="w",
                    justify="left"
                ).pack(anchor="w", padx=10, pady=2)

        else:
            # Caso ocorra erro no servidor
            ctk.CTkLabel(
                self.result_frame,
                text=result["message"]
            ).pack()