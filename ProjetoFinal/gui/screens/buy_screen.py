"""
buy_screen.py

Tela responsável pela compra de ingressos.

Responsabilidades:
- Coletar dados do usuário
- Validar entrada básica
- Solicitar compra via ClientCore
- Exibir resultado
"""

import customtkinter as ctk


class BuyScreen:

    def __init__(self, parent, core):

        self.core = core

        self.frame = ctk.CTkFrame(parent)
        self.frame.pack(fill="both", expand=True)

        ctk.CTkLabel(
            self.frame,
            text="Comprar Ingressos",
            font=("Arial", 20)
        ).pack(pady=20)

        # Campos de entrada
        self.name_entry = ctk.CTkEntry(self.frame, placeholder_text="Nome")
        self.name_entry.pack(pady=5)

        self.email_entry = ctk.CTkEntry(self.frame, placeholder_text="Email")
        self.email_entry.pack(pady=5)

        self.session_entry = ctk.CTkEntry(self.frame, placeholder_text="ID da Sessão")
        self.session_entry.pack(pady=5)

        self.quantity_entry = ctk.CTkEntry(self.frame, placeholder_text="Quantidade")
        self.quantity_entry.pack(pady=5)

        # Botão de compra
        ctk.CTkButton(
            self.frame,
            text="Comprar",
            command=self.buy
        ).pack(pady=10)

        self.result_label = ctk.CTkLabel(self.frame, text="")
        self.result_label.pack()

    def buy(self):
        """
        Executa compra via ClientCore.
        """

        result = self.core.buy_tickets(
            self.name_entry.get(),
            self.email_entry.get(),
            int(self.session_entry.get()),
            int(self.quantity_entry.get())
        )

        if result["status"] == "success":
            self.result_label.configure(
                text=f"Compra realizada! Restante: {result['data']['restante']}"
            )
        else:
            self.result_label.configure(text=result["message"])