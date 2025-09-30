import os

def concatenar_arquivos(diretorio_principal, arquivo_saida):
    """
    Navega por um diretório e todos os seus subdiretórios,
    tentando concatenar o conteúdo de todos os arquivos.
    Arquivos binários (imagens, áudio, etc.) serão ignorados.

    Args:
        diretorio_principal (str): O caminho do diretório a ser processado.
        arquivo_saida (str): O nome do arquivo para salvar o conteúdo concatenado.
    """
    
    codificacoes = ['utf-8', 'latin-1', 'cp1252']
    
    print(f"Iniciando a concatenação do diretório: {diretorio_principal}")
    
    with open(arquivo_saida, 'w', encoding='utf-8') as outfile:
        
        for root, _, arquivos in os.walk(diretorio_principal):
            
            for nome_arquivo in arquivos:
                caminho_completo_arquivo = os.path.join(root, nome_arquivo)
                
                conteudo = None
                
                # tenta ler o arquivo com diferentes codificações
                for codificacao in codificacoes:
                    try:
                        with open(caminho_completo_arquivo, 'r', encoding=codificacao) as infile:
                            conteudo = infile.read()
                            break 
                    except (UnicodeDecodeError, IsADirectoryError):
                        pass
                    except Exception as e:
                        print(f"    - Erro ao tentar abrir {caminho_completo_arquivo} com {codificacao}: {e}")
                
                if conteudo is not None:
                    outfile.write(f"### Conteúdo do arquivo: {caminho_completo_arquivo}\n\n")
                    outfile.write(conteudo)
                    outfile.write('\n\n')
                    print(f"    - Arquivo concatenado: {caminho_completo_arquivo}")
                else:
                    print(f"    - Ignorado (não é um arquivo de texto válido): {caminho_completo_arquivo}")
    
    print(f"\nProcesso concluído! O conteúdo foi salvo em '{arquivo_saida}'.")

# configurações
# diretorio_principal = 'livros_gutenberg/'
# arquivo_saida = 'gutenberg_concat.txt'
# diretorio_principal = 'concatenate_files_medium/'
# arquivo_saida = 'medium_concat.txt'
diretorio_principal = 'files/'
arquivo_saida = 'files_concat.txt'

if __name__ == "__main__":
    if not os.path.isdir(diretorio_principal):
        print(f"Erro: O diretório '{diretorio_principal}' não foi encontrado.")
    else:
        concatenar_arquivos(diretorio_principal, arquivo_saida)