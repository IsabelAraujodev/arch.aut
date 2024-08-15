import os
import shutil
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, messagebox, Listbox, Scrollbar

# Função para criar pastas organizacionais com base em critérios estabelecidos
def criar_pastas_organizacionais(base_path, categorias):
    for categoria in categorias:
        caminho = os.path.join(base_path, categoria)
        if not os.path.exists(caminho):
            os.makedirs(caminho)

# Função para movimentar e renomear arquivos com base em critérios estabelecidos
def mover_renomear_arquivos(base_path, criterios):
    for arquivo in os.listdir(base_path):
        caminho_completo = os.path.join(base_path, arquivo)
        if os.path.isfile(caminho_completo):
            extensao = os.path.splitext(arquivo)[1].lower()

            if extensao in criterios:
                nova_pasta = criterios[extensao]["pasta"]
                novo_nome = criterios[extensao]["nome"]
                
                nova_pasta_completa = os.path.join(base_path, nova_pasta)
                novo_caminho_completo = os.path.join(nova_pasta_completa, novo_nome + extensao)
                
                shutil.move(caminho_completo, novo_caminho_completo)

# Função para listar e filtrar arquivos com base em critérios estabelecidos
def listar_filtrar_arquivos(base_path, filtro_extensao=None, filtro_data=None):
    arquivos_filtrados = []
    
    for arquivo in os.listdir(base_path):
        caminho_completo = os.path.join(base_path, arquivo)
        if os.path.isfile(caminho_completo):
            extensao = os.path.splitext(arquivo)[1].lower()
            data_modificacao = datetime.fromtimestamp(os.path.getmtime(caminho_completo))
            
            if filtro_extensao and extensao != filtro_extensao:
                continue
            if filtro_data and data_modificacao.date() != filtro_data:
                continue
            
            arquivos_filtrados.append(arquivo)
    
    return arquivos_filtrados

# Função para escolher o diretório e executar as funções de organização
def organizar_arquivos():
    diretorio_base = filedialog.askdirectory()
    if not diretorio_base:
        messagebox.showwarning("Aviso", "Nenhum diretório selecionado.")
        return

    categorias = ['Imagens', 'Documentos', 'Audios']
    criterios = {
        '.jpg': {'pasta': 'Imagens', 'nome': 'Imagem_Renomeada'},
        '.png': {'pasta': 'Imagens', 'nome': 'Imagem_Renomeada'},
        '.pdf': {'pasta': 'Documentos', 'nome': 'Documento_Renomeado'},
        '.mp3': {'pasta': 'Audios', 'nome': 'Audio_Renomeado'},
    }

    criar_pastas_organizacionais(diretorio_base, categorias)
    mover_renomear_arquivos(diretorio_base, criterios)

    arquivos_filtrados = listar_filtrar_arquivos(diretorio_base)

    listbox.delete(0, tk.END)  # Limpa a lista antes de adicionar novos arquivos
    for arquivo in arquivos_filtrados:
        listbox.insert(tk.END, arquivo)

    messagebox.showinfo("Sucesso", "Arquivos organizados com sucesso!")

# Configuração da interface gráfica
root = tk.Tk()
root.title("Organizador de Arquivos")

frame = tk.Frame(root)
frame.pack(pady=10, padx=10)

# Botão para selecionar diretório e organizar arquivos
botao_organizar = tk.Button(frame, text="Organizar Arquivos", command=organizar_arquivos)
botao_organizar.pack(pady=5)

# Listbox para exibir arquivos filtrados
listbox_frame = tk.Frame(root)
listbox_frame.pack(pady=10, padx=10, fill="both", expand=True)

scrollbar = Scrollbar(listbox_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

listbox = Listbox(listbox_frame, yscrollcommand=scrollbar.set, width=50, height=15)
listbox.pack(fill="both", expand=True)
scrollbar.config(command=listbox.yview)

root.mainloop()
