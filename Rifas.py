import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import random
import json
import os

# Lista para armazenar as rifas criadas
rifas_criadas = []

# Carrega os dados das rifas do arquivo JSON
def carregar_rifas():
    global rifas_criadas
    if os.path.exists('rifas.json'):
        with open('rifas.json', 'r') as f:
            rifas_criadas = json.load(f)

# Salva os dados das rifas no arquivo JSON
def salvar_rifas():
    with open('rifas.json', 'w') as f:
        json.dump(rifas_criadas, f)

# Função para criar números aleatórios e definir a quantidade de rifas
def criar_rifa():
    try:
        valor = float(entry_valor.get())
        quantidade = int(entry_quantidade.get())
        premio = entry_premio.get()

        if quantidade <= 0 or valor <= 0:
            raise ValueError("Quantidade e valor devem ser maiores que zero.")
        
        numeros_disponiveis = list(range(1, quantidade + 1))
        random.shuffle(numeros_disponiveis)

        rifa = {
            'valor': valor,
            'quantidade': quantidade,
            'premio': premio,
            'disponiveis': numeros_disponiveis,
            'compradores': {}
        }
        rifas_criadas.append(rifa)

        messagebox.showinfo("Rifa Criada", f"Rifa criada com sucesso!\nPrêmio: {premio}\nValor: R$ {valor:.2f}")
        atualizar_lista_rifas()
        salvar_rifas()  # Salva as rifas após a criação
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira valores válidos para o valor da rifa e quantidade.")
    except Exception as e:
        messagebox.showerror("Erro", str(e))

# Função para adicionar o comprador e garantir que ele possa comprar mais de um número
def adicionar_comprador():
    try:
        nome = entry_nome.get()
        quantidade_comprada = int(entry_quantidade_comprada.get())
        rifa_selecionada = listbox_rifas.curselection()

        if nome == "":
            raise ValueError("O nome não pode estar vazio.")
        
        if not rifa_selecionada:
            raise ValueError("Nenhuma rifa selecionada.")

        rifa_idx = rifa_selecionada[0]
        rifa = rifas_criadas[rifa_idx]

        if quantidade_comprada > len(rifa['disponiveis']):
            raise ValueError("Quantidade de números indisponível.")
        
        numeros_comprados = []
        for _ in range(quantidade_comprada):
            numero = rifa['disponiveis'].pop(0)
            numeros_comprados.append(numero)
            rifa['compradores'][numero] = nome

        messagebox.showinfo("Sucesso", f"Os números {numeros_comprados} foram comprados por {nome}.")
        atualizar_lista_compradores()
        atualizar_lista_disponiveis()
        salvar_rifas()  # Salva os compradores no arquivo

        # Limpa os campos
        entry_nome.delete(0, tk.END)
        entry_quantidade_comprada.delete(0, tk.END)
    except ValueError as e:
        messagebox.showerror("Erro", str(e))

# Função para sortear um número entre os comprados
def sortear():
    rifa_selecionada = listbox_rifas.curselection()

    if not rifa_selecionada:
        messagebox.showerror("Erro", "Nenhuma rifa selecionada.")
        return

    rifa_idx = rifa_selecionada[0]
    rifa = rifas_criadas[rifa_idx]

    if rifa['compradores']:
        numero_sorteado = random.choice(list(rifa['compradores'].keys()))
        vencedor = rifa['compradores'][numero_sorteado]
        messagebox.showinfo("Sorteio", f"O número sorteado foi {numero_sorteado}, comprado por {vencedor}!")
    else:
        messagebox.showerror("Erro", "Nenhum número foi comprado ainda.")

# Função para atualizar a lista de rifas criadas
def atualizar_lista_rifas():
    listbox_rifas.delete(0, tk.END)
    for rifa in rifas_criadas:
        listbox_rifas.insert(tk.END, f"Prêmio: {rifa['premio']} | Valor: R$ {rifa['valor']} | Disponíveis: {len(rifa['disponiveis'])}")

# Função para atualizar a rifa (antigo "Editar Rifa")
def atualizar_rifa():
    rifa_selecionada = listbox_rifas.curselection()
    if not rifa_selecionada:
        messagebox.showerror("Erro", "Nenhuma rifa selecionada para atualizar.")
        return

    rifa_idx = rifa_selecionada[0]
    rifa = rifas_criadas[rifa_idx]

    novo_premio = entry_premio.get()
    novo_valor = entry_valor.get()

    if novo_premio:
        rifa['premio'] = novo_premio
    if novo_valor:
        rifa['valor'] = float(novo_valor)

    messagebox.showinfo("Sucesso", "Rifa atualizada!")
    atualizar_lista_rifas()
    salvar_rifas()  # Atualiza o arquivo rifas.json imediatamente

# Função para apagar uma rifa
def apagar_rifa():
    rifa_selecionada = listbox_rifas.curselection()
    if not rifa_selecionada:
        messagebox.showerror("Erro", "Nenhuma rifa selecionada para apagar.")
        return

    rifa_idx = rifa_selecionada[0]
    del rifas_criadas[rifa_idx]
    atualizar_lista_rifas()
    salvar_rifas()  # Atualiza o arquivo após apagar a rifa

# Função para atualizar a lista de compradores
def atualizar_lista_compradores():
    rifa_selecionada = listbox_rifas.curselection()
    if not rifa_selecionada:
        return

    rifa_idx = rifa_selecionada[0]
    rifa = rifas_criadas[rifa_idx]

    compradores_texto = "\n".join([f"Número {num}: {nome}" for num, nome in rifa['compradores'].items()])
    text_compradores.config(state=tk.NORMAL)  # Permitir edição
    text_compradores.delete(1.0, tk.END)  # Limpa o campo de texto
    text_compradores.insert(tk.END, compradores_texto)  # Adiciona compradores
    text_compradores.config(state=tk.DISABLED)  # Desabilita a edição novamente

# Função para atualizar a lista de números disponíveis
def atualizar_lista_disponiveis():
    rifa_selecionada = listbox_rifas.curselection()
    if not rifa_selecionada:
        return

    rifa_idx = rifa_selecionada[0]
    rifa = rifas_criadas[rifa_idx]
    
    lbl_disponiveis['text'] = f"Números disponíveis: {len(rifa['disponiveis'])}"

# Interface gráfica com design aprimorado
root = tk.Tk()
root.title("Sistema de Rifas")
root.geometry("600x550")
root.configure(bg='#e6e6fa')

style = ttk.Style()
style.configure("TLabel", background="#e6e6fa", font=('Arial', 12))
style.configure("TButton", font=('Arial', 10), padding=6)
style.configure("TEntry", font=('Arial', 10))

frame_top = ttk.Frame(root)
frame_top.pack(pady=10)

ttk.Label(frame_top, text="Valor da Rifa (R$):").pack(side=tk.LEFT)
entry_valor = ttk.Entry(frame_top)
entry_valor.pack(side=tk.LEFT, padx=5)

ttk.Label(frame_top, text="Quantidade:").pack(side=tk.LEFT)
entry_quantidade = ttk.Entry(frame_top)
entry_quantidade.pack(side=tk.LEFT, padx=5)

ttk.Label(frame_top, text="Prêmio:").pack(side=tk.LEFT)
entry_premio = ttk.Entry(frame_top)
entry_premio.pack(side=tk.LEFT, padx=5)

ttk.Button(frame_top, text="Criar Rifa", command=criar_rifa).pack(side=tk.LEFT, padx=5)

frame_mid = ttk.Frame(root)
frame_mid.pack(pady=10)

ttk.Label(frame_mid, text="Nome do Comprador:").pack(side=tk.LEFT)
entry_nome = ttk.Entry(frame_mid)
entry_nome.pack(side=tk.LEFT, padx=5)

ttk.Label(frame_mid, text="Quantidade Comprada:").pack(side=tk.LEFT)
entry_quantidade_comprada = ttk.Entry(frame_mid)
entry_quantidade_comprada.pack(side=tk.LEFT, padx=5)

ttk.Button(frame_mid, text="Adicionar Comprador", command=adicionar_comprador).pack(side=tk.LEFT, padx=5)

ttk.Button(frame_mid, text="Sortear", command=sortear).pack(side=tk.LEFT, padx=5)

frame_rifas = ttk.Frame(root)
frame_rifas.pack(pady=10)

ttk.Label(frame_rifas, text="Rifas Criadas:").pack()

listbox_rifas = tk.Listbox(frame_rifas, width=70, height=10)
listbox_rifas.pack()

ttk.Button(frame_rifas, text="Atualizar Rifa", command=atualizar_rifa).pack(pady=5)
ttk.Button(frame_rifas, text="Apagar Rifa", command=apagar_rifa).pack(pady=5)

# Exibe compradores e números disponíveis
frame_compradores = ttk.Frame(root)
frame_compradores.pack(pady=10)

ttk.Label(frame_compradores, text="Compradores:").pack()

# Espaço amplo para exibição dos compradores
text_compradores = tk.Text(frame_compradores, height=6, width=50, state=tk.DISABLED)
text_compradores.pack(fill=tk.BOTH, expand=True)

# Campo de rolagem para compradores
scrollbar_compradores = ttk.Scrollbar(frame_compradores, orient=tk.VERTICAL, command=text_compradores.yview)
scrollbar_compradores.pack(side=tk.RIGHT, fill=tk.Y)

text_compradores.config(yscrollcommand=scrollbar_compradores.set)

lbl_disponiveis = ttk.Label(root, text="Números disponíveis:")
lbl_disponiveis.pack(pady=10)

# Carrega as rifas ao iniciar
carregar_rifas()
atualizar_lista_rifas()

root.mainloop()
