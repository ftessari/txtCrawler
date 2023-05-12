########################################################
#                                                      #
#                                       12/05/2023     #
#   txtCrawler                                         # 
#        Consulte frases dentro de diversos livros     #
#                          (.doc .docx .pdf .txt)      #
#        Dev. FTessari                              #
#                                                      #
########################################################

import os
import sys
import PyPDF2
from tqdm import tqdm
import textract
import docx2txt
 
def procurar_frase_em_arquivo(nome_arquivo, frase):
    try:
        extensao = os.path.splitext(nome_arquivo)[1]

        if extensao == ".pdf":
            with open(nome_arquivo, "rb") as arquivo:
                leitor_pdf = PyPDF2.PdfReader(arquivo)
                for num_pagina, pagina in enumerate(leitor_pdf.pages, start=1):
                    texto = pagina.extract_text()
                    linhas = texto.split("\n")
                    for num_linha, linha in enumerate(linhas, start=1):
                        if frase in linha:
                            tqdm.write(f"\nA frase '{frase}' foi encontrada no arquivo: {nome_arquivo}")
                            tqdm.write(f"Localização: Página {num_pagina}, Linha {num_linha}")
                            tqdm.write("Texto completo da linha: " + linha)
                            return True

        elif extensao == ".txt":
            with open(nome_arquivo, "r", encoding='utf-8') as arquivo:
                linhas = arquivo.readlines()
                for num_linha, linha in enumerate(linhas, start=1):
                    if frase in linha:
                        tqdm.write(f"\nA frase '{frase}' foi encontrada no arquivo: {nome_arquivo}")
                        tqdm.write(f"Localização: Linha {num_linha}")
                        tqdm.write("Texto completo da linha: " + linha)
                        return True

        elif extensao == ".docx":
            texto = docx2txt.process(nome_arquivo)
            linhas = texto.split("\n")
            for num_linha, linha in enumerate(linhas, start=1):
                if frase in linha:
                    tqdm.write(f"\nA frase '{frase}' foi encontrada no arquivo: {nome_arquivo}")
                    tqdm.write(f"Localização: Linha {num_linha}")
                    tqdm.write("Texto completo da linha: " + linha)
                    return True

        elif extensao == ".doc":
            texto = textract.process(nome_arquivo)
            linhas = texto.decode("utf-8").split("\n")
            for num_linha, linha in enumerate(linhas, start=1):
                if frase in linha:
                    tqdm.write(f"\nA frase '{frase}' foi encontrada no arquivo: {nome_arquivo}")
                    tqdm.write(f"Localização: Linha {num_linha}")
                    tqdm.write("Texto completo da linha: " + linha)
                    return True

        return False

    except Exception as e:
        tqdm.write(f"\nOcorreu um erro ao processar o arquivo {nome_arquivo}: {str(e)}")
        return False


def procurar_frase(frase, diretorio):
    encontrou_resultado = False
    try:
        for diretorio_atual, subdiretorios, arquivos in os.walk(diretorio):
            for nome_arquivo in tqdm(arquivos, desc="Pesquisando", unit="arquivos"):
                caminho_arquivo = os.path.join(diretorio_atual, nome_arquivo)
                encontrou_resultado = procurar_frase_em_arquivo(caminho_arquivo, frase)
                if encontrou_resultado:
                    tqdm.write("----------------------------------------------------------")

    except Exception as e:
        tqdm.write(f"\nOcorreu um erro ao pesquisar a frase: {str(e)}")


if __name__ == "__main__":
    if len(sys.argv) < 3 or sys.argv[1] in ['-h', '--help']:
        print("Uso: python txtCrawler.py <frase> <diretorio>")
        print("Descrição: Este script realiza a pesquisa da frase em arquivos de texto (PDF, TXT, DOC, DOCX) presentes no diretório especificado.")
        print("Argumentos:")
        print("  <frase> A frase a ser pesquisada nos arquivos.")
        print("  <diretorio> O diretório onde a pesquisa será realizada. (Para diretório atual utiliza '.' )\n")
    else:
        frase = sys.argv[1]
        diretorio = sys.argv[2]

        if frase.strip() == "":
            print("A frase não pode estar em branco.")
        else:
            if not os.path.isdir(diretorio): # Usando diretório atual como padrão.
                diretorio = os.getcwd()

            procurar_frase(frase, diretorio)
