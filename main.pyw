import sqlite3
import tkinter as tk
from tkinter import messagebox


def configurar_banco():
    conn = sqlite3.connect("funcionarios.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS funcionarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_do_funcionario TEXT NOT NULL,
            numero_do_contrato TEXT NOT NULL
        );
    """)
    conn.commit()

    funcionarios = [
        ("JOÃO SILVA", "12345"),
        ("MARIA OLIVEIRA", "67890"),
        ("CARLOS SOUZA", "11223"),
        ("MARIA CLARA", "55432")
    ]
    cursor.executemany("""
        INSERT INTO funcionarios (nome_do_funcionario, numero_do_contrato)
        SELECT ?, ?
        WHERE NOT EXISTS (
            SELECT 1 FROM funcionarios WHERE nome_do_funcionario = ? AND numero_do_contrato = ?
        );
    """, [(f[0], f[1], f[0], f[1]) for f in funcionarios])
    conn.commit()
    conn.close()

def buscar_funcionario():
    nome = entrada_nome.get().upper()  
    if not nome:
        messagebox.showwarning("Aviso", "Por favor, insira o nome do funcionário.")
        return
    conn = sqlite3.connect("funcionarios.db")
    cursor = conn.cursor()
    cursor.execute("SELECT nome_do_funcionario, numero_do_contrato FROM funcionarios WHERE nome_do_funcionario LIKE ?", (f"%{nome}%",))
    resultados = cursor.fetchall()
    conn.close()
    if resultados:
        if len(resultados) == 1:
            mensagem.set(f"Contrato encontrado: {resultados[0][1]}")
        else:
            abrir_janela_resultados(resultados)
    else:
        mensagem.set("Funcionário não encontrado.")


def abrir_janela_resultados(resultados):
    janela_resultados = tk.Toplevel()
    janela_resultados.title("Resultados da Busca")
    janela_resultados.geometry("400x300")


    frame_scroll = tk.Frame(janela_resultados)
    frame_scroll.pack(fill=tk.BOTH, expand=True)


    canvas = tk.Canvas(frame_scroll)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)


    scrollbar = tk.Scrollbar(frame_scroll, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    canvas.configure(yscrollcommand=scrollbar.set)


    frame_interno = tk.Frame(canvas)
    canvas.create_window((0, 0), window=frame_interno, anchor="nw")


    tk.Label(frame_interno, text="Resultados encontrados:", font=("Arial", 12, "bold")).pack(pady=10)
    for nome, contrato in resultados:
        tk.Label(frame_interno, text=f"Nome: {nome}, Contrato: {contrato}").pack()


    frame_interno.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))


    canvas.bind_all("<MouseWheel>", lambda event: canvas.yview_scroll(-1 * (event.delta // 120), "units"))

def criar_janela():
    global entrada_nome, mensagem
    janela = tk.Tk()
    janela.title("Consulta de Funcionários")
    janela.geometry("400x200")
    

    tk.Label(janela, text="Nome do Funcionário:").pack(pady=10)
    entrada_nome = tk.Entry(janela, width=30)
    entrada_nome.pack(pady=5)
    

    tk.Button(janela, text="Buscar", command=buscar_funcionario).pack(pady=10)

    mensagem = tk.StringVar()
    tk.Label(janela, textvariable=mensagem, fg="blue").pack(pady=10)
    

    janela.mainloop()


if __name__ == "__main__":
    configurar_banco()
    criar_janela()