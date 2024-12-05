import sqlite3
import re
import pyperclip
import pyautogui
import time
import webbrowser

url = "https://passaportepesquisadiretorio.findes.org.br/passaporte_industrial_arquivos/"


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
    conn.close()

def inserir_dados(nomes_contrato):
    conn = sqlite3.connect("funcionarios.db")
    cursor = conn.cursor()
    for nome, contrato in nomes_contrato:
        cursor.execute("""
            INSERT INTO funcionarios (nome_do_funcionario, numero_do_contrato)
            SELECT ?, ?
            WHERE NOT EXISTS (
                SELECT 1 FROM funcionarios WHERE UPPER(nome_do_funcionario) = UPPER(?) AND numero_do_contrato = ?
            );
        """, (nome.upper(), contrato, nome.upper(), contrato))
    conn.commit()
    conn.close()


def processar_dados_clipboard():
    try:

        clipboard_data = pyperclip.paste()

        contrato_match = re.search(r"passaporte_industrial_arquivos/\d+\s*-\s*(\d+)", clipboard_data)
        numero_contrato = contrato_match.group(1) if contrato_match else "DESCONHECIDO"


        nomes_match = re.findall(r"<dir>\s+(.+)", clipboard_data)

        nomes_contrato = [(nome.strip(), numero_contrato) for nome in nomes_match]
        return nomes_contrato

    except Exception as e:
        print(f"Erro ao processar os dados do clipboard: {e}")
        return []

##É IMPORTANTE JÁ ESTÁ LOGADO NO DIRETÓRIO ANTES DE EXECUTAR O SCRIPT

if __name__ == "__main__":
    configurar_banco()
    webbrowser.open(url)
    time.sleep(3)
    pyautogui.press('tab')

    while True:
        pyautogui.press('tab')
        time.sleep(0.3)
        pyautogui.press('enter')
        time.sleep(1)
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(1)
        pyautogui.hotkey('ctrl', 'c')
            

        dados = processar_dados_clipboard()
        if dados:
            inserir_dados(dados)
            
            print(f"{len(dados)} registros inseridos no banco de dados!")
        else:
            print("Nenhum dado válido encontrado no clipboard.")
        
        
        pyautogui.hotkey('alt', 'left')
        time.sleep(0.9)

