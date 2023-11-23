
import pandas as pd
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import simpledialog

def restructure_data(file_path, save_path, column_values):
    # Carraga o arquivo Excel
    data = pd.read_excel(file_path)

    # Remove as informação não desejadas (titles, 'Colaborador', 'Adiant', 'Total geral')
    data_filtered = data.dropna(subset=['Unnamed: 1', 'Unnamed: 13'])
    data_filtered = data_filtered[data_filtered['Unnamed: 1'] != 'COLABORADOR ']
    data_filtered = data_filtered[data_filtered['Unnamed: 13'] != 'ADIANT.']
    data_filtered = data_filtered[~data_filtered['Unnamed: 1'].str.upper().str.contains('TOTAL GERAL')]

    # Divide as colunas das Lojas que estão agrupadas em uma uncica celula 'Unnamed: 1'
    split_names = data_filtered['Unnamed: 1'].str.split('\n', expand=True).stack()
    split_names = split_names.reset_index(level=1, drop=True).rename('E2_NOMFOR')

    # Entra com os nome das lojas sepadas 
    data_restructured = data_filtered.drop(columns=['Unnamed: 1']).join(split_names)
    data_restructured = data_restructured.rename(columns={'Unnamed: 0': 'E2_FILIAL', 'Unnamed: 13': 'E2_VALOR'})

    # Preenche a coluna E2_FILIAL com o nome da linha de cima
    data_restructured['E2_FILIAL'] = data_restructured['E2_FILIAL'].fillna(method='ffill')

    # Reorganiza informações das filiais
    store_codes = {
        "PRO-LABORE": "01zz",
        "DISTRIBUIDORA": "0198",
        "ADM": "0199"
    }

    # Substitui os nomes de Loja para formato '0101'
    data_restructured['E2_FILIAL'] = data_restructured['E2_FILIAL'].replace(store_codes)
    data_restructured['E2_FILIAL'] = data_restructured['E2_FILIAL'].apply(
        lambda x: '01' + x.split(' ')[-1].zfill(2) if 'bred' in x.lower() else x
    )

    # Converte 'E2_VALOR' para valor numerico
    data_restructured['E2_VALOR'] = pd.to_numeric(data_restructured['E2_VALOR'], errors='coerce').fillna(0)
    data_restructured['E2_VALOR'] = data_restructured['E2_VALOR'].apply(lambda x: f"{x:.2f}")

    # Remove linha com valor 0.00
    final_data = data_restructured[data_restructured['E2_VALOR'] != '0.00']

    # Cria um Dataframe com o molde de importação
    final_structure = pd.DataFrame(columns=[
        'E2_FILIAL', 'E2_PREFIXO', 'E2_NUM', 'E2_TIPO', 'E2_NATUREZ', 'E2_FORNECE', 'E2_LOJA', 
        'E2_NOMFOR', 'E2_EMISSAO', 'E2_VENCTO', 'E2_VENCREA', 'E2_VALOR', 'E2_HIST'
    ])

    # Informa os dados do Dataframe
    final_structure['E2_FILIAL'] = final_data['E2_FILIAL']
    final_structure['E2_NOMFOR'] = final_data['E2_NOMFOR']
    final_structure['E2_VALOR'] = final_data['E2_VALOR']
    final_structure['E2_PREFIXO'] = "RHI"
    final_structure['E2_NUM'] = column_values['E2_NUM']
    final_structure['E2_TIPO'] =  "TF"
    final_structure['E2_NATUREZ'] = column_values['E2_NATUREZ']
    final_structure['E2_EMISSAO'] = column_values['E2_EMISSAO']
    final_structure['E2_VENCTO'] = column_values['E2_VENCTO']
    final_structure['E2_VENCREA'] = column_values['E2_VENCTO']
    final_structure['E2_HIST'] = column_values['E2_HIST']

    start_num = int(column_values['E2_NUM'])  # Converte para o formato de 9 digitos
    final_structure['E2_NUM'] = [f"{num:09d}" for num in range(start_num, start_num + len(final_data))]


    # Mensagem de finalização
    final_structure.to_excel(save_path, index=False)
    messagebox.showinfo("Sucesso!", "Importação salva com sucesso!")

def select_file():
    root = tk.Tk()
    root.withdraw() 

    # Solicita que o Usuario informe os valores das colunas
    e2_num = simpledialog.askstring("Input", "Enter starting value for E2_NUM", parent=root)
    column_values = {
        'E2_NUM': e2_num.zfill(9),  # Verificar se esta com 9 digitos
        'E2_NATUREZ': simpledialog.askstring("Input", "Enter value for E2_NATUREZ", parent=root),
        'E2_EMISSAO': simpledialog.askstring("Input", "Enter value for E2_EMISSAO", parent=root),
        'E2_VENCTO': simpledialog.askstring("Input", "Enter value for E2_VENCTO", parent=root),
        'E2_HIST': simpledialog.askstring("Input", "Enter value for E2_HIST", parent=root)
    }

    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
    if file_path:
        save_path = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                                 filetypes=[("Excel files", "*.xlsx")])
        if save_path:
            restructure_data(file_path, save_path, column_values)

select_file()