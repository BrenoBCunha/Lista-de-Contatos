from lista_contatos.agenda import Agenda
import customtkinter as ctk

class Interface(ctk.CTk):
    def __init__(self, agenda: Agenda):
        super().__init__()
        self._agenda = agenda
        self._configurar_janela_principal()
        self._criar_widgets()


    def _configurar_janela_principal(self):
        self.title("Lista de Contatos")
        self.geometry("500x600")
        ctk.set_appearance_mode("Dark")
        self.resizable(width=False, height=False)

        #Configuração do Grid principal
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)


    def _criar_widgets(self):
        # ==== Frame pincipal (pesquisa e lista) ====
        self.frame_principal = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_principal.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.frame_principal.grid_columnconfigure(0, weight=1)
        self.frame_principal.grid_rowconfigure(1, weight=1) # Permite que a lista expanda

        # 1. Sub-frame da Barra de Pesquisa
        self.frame_pesquisa = ctk.CTkFrame(self.frame_principal, fg_color="transparent")
        self.frame_pesquisa.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        self.frame_pesquisa.grid_columnconfigure(0, weight=1)

        self.entry_pesquisa = ctk.CTkEntry(self.frame_pesquisa, placeholder_text="Pesquisar por nome ou número...")
        self.entry_pesquisa.grid(row=0, column=0, sticky="ew", padx=(0, 10))

        self.btn_pesquisar = ctk.CTkButton(self.frame_pesquisa, text="Pesquisar", width=100, command= self._pesquisar)
        self.btn_pesquisar.grid(row=0, column=1)

        # 2. Área da Lista de Contatos (Frame com Scroll)
        self.frame_lista = ctk.CTkScrollableFrame(self.frame_principal, label_text="Meus Contatos")
        self.frame_lista.grid(row=1, column=0, sticky="nsew")

        self.btn_adicionar = ctk.CTkButton(self.frame_principal, text='+', font=('Arial', 40), width = 50, command=self._abrir_novo_contato)
        self.btn_adicionar.place(x = 390, y = 490)

        # 3. Inicia a Listagem
        self._atualizar_lista()


    def _atualizar_lista(self):
        for widget in self.frame_lista.winfo_children():
            if isinstance(widget, ctk.CTkButton):
                widget.destroy()
        
        for contato in self._agenda.listar():
            btn_contato = ctk.CTkButton(self.frame_lista, text = contato.nome, fg_color="#414141", hover_color="#666666", width=450, anchor= 'w', command=lambda id_contato = contato.id: self._abrir_detalhes(id_contato))
            btn_contato.pack(side='top', fill='x', padx=10, pady=5)

        self.update_idletasks()


    def _pesquisar(self):
        busca = self.entry_pesquisa.get()
        resultados = self._agenda.buscar_por_nome(busca)

        for widget in self.frame_lista.winfo_children():
            if isinstance(widget, ctk.CTkButton):
                widget.destroy()
        
        for contato in resultados:
            btn_contato = ctk.CTkButton(self.frame_lista, text = contato.nome, fg_color="#414141", hover_color="#666666", width=450, anchor= 'w', command=lambda id_contato = contato.id: self._abrir_detalhes(id_contato))
            btn_contato.pack(side='top', fill='x', padx=10, pady=5)

        self.update_idletasks()


    def _abrir_novo_contato(self):
        self.janela_contato = ctk.CTkToplevel()
        self.janela_contato.title("Novo Contato")
        w = 350
        h = 260
        self.update_idletasks()

        x_frame = self.winfo_x()
        y_frame = self.winfo_y()
        w_frame = self.winfo_width()
        h_frame = self.winfo_height()

        pos_x = x_frame + w_frame // 2 - w // 2
        pos_y = y_frame + h_frame // 2 - h // 2

        self.janela_contato.geometry(f'{w}x{h}+{pos_x}+{pos_y}')
        
        self.janela_contato.grab_set()
        self.janela_contato.focus_force()

        lbl_nome = ctk.CTkLabel(self.janela_contato, text = 'Nome: ', font=('Arial', 14))
        lbl_nome.place(x = 20, y = 20)

        self.etr_nome = ctk.CTkEntry(self.janela_contato, width=230)
        self.etr_nome.place(x = 90, y = 20)

        lbl_numero = ctk.CTkLabel(self.janela_contato, text='Telefone: ', font=('Arial', 14))
        lbl_numero.place(x = 20, y = 60)

        self.etr_telefone = ctk.CTkEntry(self.janela_contato, width=230)
        self.etr_telefone.place(x = 90, y = 60)

        lbl_email = ctk.CTkLabel(self.janela_contato, text='E-mail: ', font=('Arial', 14))
        lbl_email.place(x = 20, y = 100)

        self.etr_email = ctk.CTkEntry(self.janela_contato, width = 230)
        self.etr_email.place(x = 90, y = 100)

        lbl_endereco = ctk.CTkLabel(self.janela_contato, text='Endereço: ', font=('Arial', 14))
        lbl_endereco.place(x = 20, y = 140)

        self.etr_endereco = ctk.CTkEntry(self.janela_contato, width=230)
        self.etr_endereco.place(x=90, y = 140)

        # Botão Adicionar e Cancelar

        self.btn_add = ctk.CTkButton(self.janela_contato, text='Adicionar', command=self._adicionar_contato)
        self.btn_add.place(x = 180, y=200)

        self.btn_cancel = ctk.CTkButton(self.janela_contato, text='Cancelar', fg_color="#F33939", command= self.janela_contato.destroy)
        self.btn_cancel.place(x=20, y=200)


    def _adicionar_contato(self):
        agenda = self._agenda

        nome = self.etr_nome.get().strip()
        telefone = self.etr_telefone.get().strip()
        email = self.etr_email.get().strip()
        endereco = self.etr_endereco.get().strip()

        agenda.adicionar(nome, telefone, email, endereco)
        self._atualizar_lista()
        self.janela_contato.destroy()


    def _abrir_detalhes(self, id_contato):
        contato = self._agenda.buscar_por_id(id_contato)
        self._abrir_novo_contato()

        self.etr_nome.insert(0, contato.nome)
        self.etr_telefone.insert(0, contato.telefone)
        if contato.email is not None:
            self.etr_email.insert(0, contato.email)
        if contato.endereco is not None:
            self.etr_endereco.insert(0, contato.endereco)

        # Configuração da janela
        self.janela_contato.configure(title="Editar Contato")

        self.btn_add.configure(text='Editar', command= lambda: self._editar_contato(id_contato))
        self.btn_cancel.configure(text='Excluir', command= lambda: self._excluir_contato(id_contato))

        self.janela_contato.update_idletasks()


    def _editar_contato(self, id_contato) -> None:
        nome = self.etr_nome.get()
        telefone = self.etr_telefone.get()
        email = self.etr_email.get()
        endereco = self.etr_endereco.get()

        self._agenda.editar(id_contato, nome, telefone, email, endereco)
        self._atualizar_lista()
        self.janela_contato.destroy()


    def _excluir_contato(self, id_contato) -> None:
        self._agenda.remover(id_contato)
        self._atualizar_lista()
        self.janela_contato.destroy()

        












    



