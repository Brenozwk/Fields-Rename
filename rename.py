import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

pasta_escolhida = ""
def escolher_pasta():
    global pasta_escolhida
    pasta = tk.filedialog.askdirectory(title = "Selecione a pasta com as imagens")
    if pasta:
        pasta_escolhida = pasta
        texto_exibir = f"...{pasta[-30:]}" if len(pasta) > 30 else pasta
        lbl_pasta_escolhida.config(text = texto_exibir, foreground = "blue")

def renomear_arquivos():
    global pasta_escolhida
    if not pasta_escolhida:
        messagebox.showinfo(title="Atenção", message = "Por favor, selecione uma pasta", icon = "warning")
        return

    raio_input = entry_raio.get().strip()
    if not raio_input.isdigit():
        messagebox.showerror(title = "Erro", message= "O raio deve ser um número inteiro", icon = "error")
        return
    raio = raio_input + "nm"

    try:
        comprimento_onda = int(entry_onda.get().strip()) 
    except ValueError:
        messagebox.showerror(title="Erro", message = "O comprimento de onda deve ser um número inteiro")
        return

    select_field = combo_campo.get()
    if select_field == "EF":
        prefixo = 'NanoCilindro_EF'
    elif select_field == "MF":
        prefixo = 'Nanodisco_MF'
    else:
        messagebox.showwarning("Atenção", "Seleção de campo inválida. Selecione [EF] ou [MF].")
        return

    try:
        arquivos = os.listdir(pasta_escolhida)
        arquivos_filtrados = [f for f in arquivos if f.startswith("Untitled") and f.endswith(".png")]
        arquivos_filtrados.sort()

        if not arquivos_filtrados:
            messagebox.showerror("Erro", "Não há nenhum arquivo começando com 'Untitled' no formato '.png'")
            return
        
        onda_atual = comprimento_onda
        for arquivo_antigo in arquivos_filtrados:
            novo_nome = f"{prefixo}_{raio}_{onda_atual}nm.png"
            caminho_antigo = os.path.join(pasta_escolhida, arquivo_antigo)
            caminho_novo = os.path.join(pasta_escolhida, novo_nome)

            os.rename(caminho_antigo, caminho_novo)
            onda_atual += 4
        
        messagebox.showinfo("Sucesso", "Arquivos renomeados com sucesso")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro inesperado\n{str(e)}")





root = tk.Tk()
root.title("Renomeador COMSOL")
root.geometry("600x450") # Janela um pouco mais alta para caber os novos botões
root.resizable(False, False)

frame = ttk.Frame(root, padding="20")
frame.pack(expand=True)

# Título
titulo = ttk.Label(frame, text="Renomear imagens:\nCampo Elétrico e Campo Magnético", font=("Arial", 12, "bold"))
titulo.grid(row=0, column=0, columnspan=2, pady=(0, 20))

# Campo: Raio
ttk.Label(frame, text="Raio da nanoestrutura (sem 'nm'):").grid(row=1, column=0,sticky=tk.W, pady=5)
entry_raio = ttk.Entry(frame, width=15)
entry_raio.grid(row=1, column=1,sticky=tk.E,pady=5)

# Campo: Comprimento de Onda
ttk.Label(frame, text="Comprimento de onda inicial:").grid(row=2, column=0, sticky=tk.W, pady=5)
entry_onda = ttk.Entry(frame, width=15)
entry_onda.grid(row=2, column=1, sticky=tk.E, pady=5)

# Campo: Seleção EF / MF
ttk.Label(frame, text="Selecione o Campo:").grid(row=3, column=0, sticky=tk.W, pady=5)
combo_campo = ttk.Combobox(frame, values=["EF", "MF"], state="readonly", width=12)
combo_campo.current(0) 
combo_campo.grid(row=3, column=1, sticky=tk.E,pady=5)

# Linha divisória visual
ttk.Separator(frame, orient='horizontal').grid(row=4, column=0, columnspan=2, pady=15)

# Área de Seleção de Pasta
btn_pasta = ttk.Button(frame, text="📁 Escolher Pasta", command=escolher_pasta)
btn_pasta.grid(row=5, column=0, columnspan=2, pady=5)

lbl_pasta_escolhida = ttk.Label(frame, text="Nenhuma pasta selecionada", foreground="gray")
lbl_pasta_escolhida.grid(row=6, column=0, columnspan=2, pady=5)

# Botão de Execução
btn_executar = ttk.Button(frame, text="Renomear Arquivos", command=renomear_arquivos)
btn_executar.grid(row=7, column=0, columnspan=2, pady=(25, 0), ipadx=10, ipady=5)

root.mainloop()