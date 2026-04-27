import os
import tkinter as tk
from tkinter import ttk, messagebox

def renomear_arquivos():
    raio_input = entry_raio.get().strip()
    if not raio_input:
        messagebox.showwarning("Aviso", "Insira o valor do raio")
        return
    raio = raio_input + "nm"
    try:
        lambda0 = int(entry_onda.get().strip())
    except ValueError:
        messagebox.showwarning("Erro", "o valor do comprimento inicial deve ser um número inteiro")
        return
    
    select_field = combo_campo.get().strip()
    
    if select_field == "EF":
        pasta = rf"C:\Users\LPDS.DESKTOP-6BJ3NG6\Documents\Simulações COMSOL\Cilindros\Cilindros - Eduarda\Electric Field\{raio}"
        prefixo = "Nanocilindro_EF"
        msg_sucesso = "Imagens do campo elétrico renomeadas com sucesso!"
    elif select_field == "MF":
        pasta = rf"C:\Users\LPDS.DESKTOP-6BJ3NG6\Documents\Simulações COMSOL\Cilindros\Cilindros - Eduarda\Magnetic Field\{raio}"
        prefixo = "Nanocilindro_MF"
        msg_sucesso = "Imagens do campo magnético renomeadas com sucesso!"
    else:
        messagebox.showwarning("Erro", "Selecione um campo válido (EF/MF)")
        return
    if not os.path.exists(pasta):
        messagebox.showerror("Erro de diretório", f"A pasta não foi encontrada:\n{pasta}")
        return
    arquivos = os.listdir(pasta)
    arquivos_filtrados = [f for f in arquivos if f.startswith("Untitled") and f.endswith(".png")]
    arquivos_filtrados.sort()

    if not arquivos_filtrados:
        messagebox.showinfo("Aviso", "Nenhum arquivo começado com 'Untitled' e no formato '.png' foram encontrados")
        return
    onda_atual = lambda0

    for arquivo_antigo in arquivos_filtrados:
        novo_nome = f"{prefixo}_{raio}_{onda_atual}nm.png"
        caminho_antigo = os.path.join(pasta, arquivo_antigo)
        caminho_novo = os.path.join(pasta, novo_nome)

        os.rename(caminho_antigo, caminho_novo)
        onda_atual += 4
    
    messagebox.showinfo("Sucesso", msg_sucesso)




root = tk.Tk()
root.title("Renomeador COMSOL")
root.geometry("500x350")
root.resizable(False, False)


frame = ttk.Frame(root, padding="20")
frame.pack(fill=tk.BOTH, expand=True)


titulo = ttk.Label(frame, text="Renomear Imagens de Simulações", font=("Arial", 12, "bold"))
titulo.grid(row=0, column=0, columnspan=2, pady=(0, 20))


ttk.Label(frame, text="Raio da nanoestrutura (sem 'nm'):").grid(row=1, column=0, sticky=tk.W, pady=5)
entry_raio = ttk.Entry(frame, width=15)
entry_raio.grid(row=1, column=1, sticky=tk.E, pady=5)


ttk.Label(frame, text="Comprimento de onda inicial:").grid(row=2, column=0, sticky=tk.W, pady=5)
entry_onda = ttk.Entry(frame, width=15)
entry_onda.grid(row=2, column=1, sticky=tk.E, pady=5)


ttk.Label(frame, text="Selecione o Campo:").grid(row=3, column=0, sticky=tk.W, pady=5)
combo_campo = ttk.Combobox(frame, values=["EF", "MF"], state="readonly", width=12)
combo_campo.current(0) # Define "EF" como padrão
combo_campo.grid(row=3, column=1, sticky=tk.E, pady=5)


btn_executar = ttk.Button(frame, text="Renomear Arquivos", command=renomear_arquivos)
btn_executar.grid(row=4, column=0, columnspan=2, pady=(25, 0), ipadx=10, ipady=5)

root.mainloop()        