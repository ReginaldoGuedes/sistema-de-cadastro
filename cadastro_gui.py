import tkinter as tk
from tkinter import messagebox
from ttkbootstrap import Style
from datetime import datetime
import pandas as pd
import os
import json

# Nome do arquivo Excel e do arquivo de senhas
excel_file = "cadastros.xlsx"
senha_file = "senhas.json"

# Lista para armazenar os cadastros
cadastros = []

# Carregar senhas de um arquivo JSON
def load_senhas():
    if os.path.exists(senha_file):
        with open(senha_file, 'r') as f:
            return json.load(f)
    return {"admin": "admin123", "usuario": "usuario123"}

# Salvar senhas em um arquivo JSON
def save_senhas(senhas):
    with open(senha_file, 'w') as f:
        json.dump(senhas, f)

class CadastroApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Sistema de Cadastro")
        
        # Estilo Bootstrap
        self.style = Style()
        
        # Variável para determinar se o usuário é admin
        self.is_admin = False
        
        # Carregar senhas
        self.senhas = load_senhas()
        
        # Tela de login
        self.create_login_screen()

    def create_login_screen(self):
        self.clear_widgets()
        
        tk.Label(self.master, text="Usuário").pack(padx=10, pady=5)
        self.usuario_entry = tk.Entry(self.master)
        self.usuario_entry.pack(padx=10, pady=5)
        
        tk.Label(self.master, text="Senha").pack(padx=10, pady=5)
        self.senha_entry = tk.Entry(self.master, show="*")
        self.senha_entry.pack(padx=10, pady=5)
        
        login_button = tk.Button(self.master, text="Entrar", command=self.login)
        login_button.pack(pady=10)

    def login(self):
        usuario = self.usuario_entry.get()
        senha = self.senha_entry.get()

        if usuario in self.senhas and self.senhas[usuario] == senha:
            self.is_admin = usuario == "admin"
            self.create_main_interface()
        else:
            messagebox.showerror("Erro", "Usuário ou senha incorretos.")

    def create_main_interface(self):
        self.clear_widgets()
        
        # Configuração do layout
        self.create_widgets()

        # Carregar cadastros existentes, se houver
        self.load_cadastros()

    def clear_widgets(self):
        for widget in self.master.winfo_children():
            widget.destroy()

    def create_widgets(self):
        tk.Label(self.master, text="Nome").grid(row=0, column=0, padx=10, pady=5, sticky="ew")
        self.nome_entry = tk.Entry(self.master)
        self.nome_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        tk.Label(self.master, text="CPF/CNPJ").grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        self.cpf_cnpj_entry = tk.Entry(self.master)
        self.cpf_cnpj_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        tk.Label(self.master, text="Telefone").grid(row=2, column=0, padx=10, pady=5, sticky="ew")
        self.telefone_entry = tk.Entry(self.master)
        self.telefone_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        tk.Label(self.master, text="Endereço").grid(row=3, column=0, padx=10, pady=5, sticky="ew")
        self.endereco_entry = tk.Entry(self.master)
        self.endereco_entry.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

        # Botão de Cadastrar
        self.cadastrar_button = tk.Button(self.master, text="Cadastrar", command=self.cadastrar)
        self.cadastrar_button.grid(row=4, column=0, columnspan=2, pady=10)

        # Busca por contato
        tk.Label(self.master, text="Buscar por Nome ou CPF/CNPJ").grid(row=5, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
        self.buscar_entry = tk.Entry(self.master)
        self.buscar_entry.grid(row=6, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

        # Botões de Listar
        self.listar_button = tk.Button(self.master, text="Listar Contato", command=self.listar_contato)
        self.listar_button.grid(row=7, column=0, padx=10, pady=5, sticky="ew")

        self.listar_todos_button = tk.Button(self.master, text="Listar Todos os Cadastros", command=self.listar_cadastros)
        self.listar_todos_button.grid(row=7, column=1, padx=10, pady=5, sticky="ew")

        # Botões de gerenciamento de usuários (apenas para admin)
        if self.is_admin:
            self.criar_usuario_button = tk.Button(self.master, text="Criar Usuário", command=self.criar_usuario)
            self.criar_usuario_button.grid(row=8, column=0, padx=10, pady=5)

            self.excluir_usuario_button = tk.Button(self.master, text="Excluir Usuário", command=self.excluir_usuario)
            self.excluir_usuario_button.grid(row=8, column=1, padx=10, pady=5)

            self.listar_usuarios_button = tk.Button(self.master, text="Listar Usuários", command=self.listar_usuarios)
            self.listar_usuarios_button.grid(row=9, column=0, columnspan=2, pady=5)

            self.trocar_senha_button = tk.Button(self.master, text="Trocar Senha", command=self.trocar_senha)
            self.trocar_senha_button.grid(row=10, column=0, columnspan=2, pady=10)

    def trocar_senha(self):
        senha_window = tk.Toplevel(self.master)
        senha_window.title("Trocar Senha")
        self.center_window(senha_window)

        tk.Label(senha_window, text="Usuário").grid(row=0, column=0, padx=10, pady=5)
        usuario_entry = tk.Entry(senha_window)
        usuario_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(senha_window, text="Senha Antiga").grid(row=1, column=0, padx=10, pady=5)
        senha_antiga_entry = tk.Entry(senha_window, show="*")
        senha_antiga_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(senha_window, text="Nova Senha").grid(row=2, column=0, padx=10, pady=5)
        nova_senha_entry = tk.Entry(senha_window, show="*")
        nova_senha_entry.grid(row=2, column=1, padx=10, pady=5)

        confirmar_button = tk.Button(senha_window, text="Confirmar", command=lambda: self.confirmar_troca(usuario_entry.get(), senha_antiga_entry.get(), nova_senha_entry.get(), senha_window))
        confirmar_button.grid(row=3, column=0, columnspan=2, pady=10)

    def confirmar_troca(self, usuario, senha_antiga, nova_senha, window):
        if usuario in self.senhas and self.senhas[usuario] == senha_antiga:
            self.senhas[usuario] = nova_senha
            save_senhas(self.senhas)  # Salvar as senhas atualizadas
            messagebox.showinfo("Sucesso", "Senha alterada com sucesso!")
            window.destroy()
        else:
            messagebox.showerror("Erro", "Senha antiga incorreta ou usuário não encontrado.")

    def cadastrar(self):
        nome = self.nome_entry.get()
        cpf_cnpj = self.cpf_cnpj_entry.get()
        telefone = self.telefone_entry.get()
        endereco = self.endereco_entry.get()
        data_cadastro = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cadastro = {
            'Nome': nome,
            'CPF/CNPJ': cpf_cnpj,
            'Telefone': telefone,
            'Endereço': endereco,
            'Data de Cadastro': data_cadastro
        }

        cadastros.append(cadastro)
        self.save_to_excel()

        messagebox.showinfo("Sucesso", "Cadastro realizado com sucesso!")

        # Limpar entradas
        self.limpar_entries()

    def listar_cadastros(self):
        if not cadastros:
            messagebox.showinfo("Lista de Cadastros", "Nenhum cadastro encontrado.")
            return
        
        lista = "\n".join([f"{i+1}. {c['Nome']} - {c['CPF/CNPJ']}" for i, c in enumerate(cadastros)])
        messagebox.showinfo("Lista de Cadastros", lista)

    def listar_contato(self):
        busca = self.buscar_entry.get().strip().lower()
        resultados = [
            c for c in cadastros 
            if busca in c['Nome'].lower() or busca in str(c['CPF/CNPJ']).replace('/', '').replace('-', '').lower()
    ]

        if not resultados:
            messagebox.showinfo("Resultado da Busca", "Nenhum contato encontrado.")
            return

        self.exibir_resultados(resultados)



    def exibir_resultados(self, resultados):
        detalhes_window = tk.Toplevel(self.master)
        detalhes_window.title("Resultados da Busca")
        self.center_window(detalhes_window)

        for idx, contato in enumerate(resultados):
            tk.Label(detalhes_window, text=f"Contato {idx + 1}").grid(row=idx * 6, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

            tk.Label(detalhes_window, text="Nome").grid(row=idx * 6 + 1, column=0, padx=10, sticky="ew")
            tk.Label(detalhes_window, text=contato['Nome']).grid(row=idx * 6 + 1, column=1, padx=10, sticky="ew")

            tk.Label(detalhes_window, text="CPF/CNPJ").grid(row=idx * 6 + 2, column=0, padx=10, sticky="ew")
            tk.Label(detalhes_window, text=contato['CPF/CNPJ']).grid(row=idx * 6 + 2, column=1, padx=10, sticky="ew")

            tk.Label(detalhes_window, text="Telefone").grid(row=idx * 6 + 3, column=0, padx=10, sticky="ew")
            tk.Label(detalhes_window, text=contato['Telefone']).grid(row=idx * 6 + 3, column=1, padx=10, sticky="ew")

            tk.Label(detalhes_window, text="Endereço").grid(row=idx * 6 + 4, column=0, padx=10, sticky="ew")
            tk.Label(detalhes_window, text=contato['Endereço']).grid(row=idx * 6 + 4, column=1, padx=10, sticky="ew")

            # Apenas o admin pode ver os botões de edição e exclusão
            if self.is_admin:
                excluir_button = tk.Button(detalhes_window, text="Excluir", command=lambda c=contato: self.excluir_contato(c, detalhes_window))
                excluir_button.grid(row=idx * 6 + 5, column=0, padx=10, pady=5)

    def excluir_contato(self, contato, window):
        cadastros.remove(contato)
        self.save_to_excel()
        messagebox.showinfo("Sucesso", "Contato excluído com sucesso!")
        window.destroy()

    def listar_usuarios(self):
        usuarios = "\n".join([f"{usuario}" for usuario in self.senhas.keys()])
        messagebox.showinfo("Lista de Usuários", usuarios)

    def limpar_entries(self):
        self.nome_entry.delete(0, tk.END)
        self.cpf_cnpj_entry.delete(0, tk.END)
        self.telefone_entry.delete(0, tk.END)
        self.endereco_entry.delete(0, tk.END)

    def save_to_excel(self):
        df = pd.DataFrame(cadastros)
        df.to_excel(excel_file, index=False)

    def load_cadastros(self):
        if os.path.exists(excel_file):
            df = pd.read_excel(excel_file)
            for _, row in df.iterrows():
                cadastros.append(row.to_dict())

    def center_window(self, window):
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x = (self.master.winfo_width() // 2) - (width // 2)
        y = (self.master.winfo_height() // 2) - (height // 2)
        window.geometry(f"{width}x{height}+{x}+{y}")

    def criar_usuario(self):
        usuario_window = tk.Toplevel(self.master)
        usuario_window.title("Criar Usuário")
        self.center_window(usuario_window)

        tk.Label(usuario_window, text="Novo Usuário").grid(row=0, column=0, padx=10, pady=5)
        novo_usuario_entry = tk.Entry(usuario_window)
        novo_usuario_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(usuario_window, text="Nova Senha").grid(row=1, column=0, padx=10, pady=5)
        nova_senha_entry = tk.Entry(usuario_window, show="*")
        nova_senha_entry.grid(row=1, column=1, padx=10, pady=5)

        criar_button = tk.Button(usuario_window, text="Criar", command=lambda: self.adicionar_usuario(novo_usuario_entry.get(), nova_senha_entry.get(), usuario_window))
        criar_button.grid(row=2, column=0, columnspan=2, pady=10)

    def adicionar_usuario(self, usuario, senha, window):
        if usuario in self.senhas:
            messagebox.showerror("Erro", "Usuário já existe.")
        else:
            self.senhas[usuario] = senha
            save_senhas(self.senhas)
            messagebox.showinfo("Sucesso", "Usuário criado com sucesso!")
            window.destroy()

    def excluir_usuario(self):
        usuario_window = tk.Toplevel(self.master)
        usuario_window.title("Excluir Usuário")
        self.center_window(usuario_window)

        tk.Label(usuario_window, text="Usuário").grid(row=0, column=0, padx=10, pady=5)
        usuario_entry = tk.Entry(usuario_window)
        usuario_entry.grid(row=0, column=1, padx=10, pady=5)

        excluir_button = tk.Button(usuario_window, text="Excluir", command=lambda: self.remover_usuario(usuario_entry.get(), usuario_window))
        excluir_button.grid(row=1, column=0, columnspan=2, pady=10)

    def remover_usuario(self, usuario, window):
        if usuario in self.senhas and usuario != "admin":
            del self.senhas[usuario]
            save_senhas(self.senhas)
            messagebox.showinfo("Sucesso", "Usuário excluído com sucesso!")
            window.destroy()
        else:
            messagebox.showerror("Erro", "Usuário não encontrado ou não é possível excluir o admin.")

if __name__ == "__main__":
    root = tk.Tk()
    app = CadastroApp(root)
    root.geometry("400x400")
    root.eval('tk::PlaceWindow . center')
    root.mainloop()
