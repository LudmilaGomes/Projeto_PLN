import os
import requests

def eh_arquivo_de_texto_valido_caracteres(conteudo):
    alfabeto = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
    letras = sum(1 for c in conteudo if c in alfabeto)
    outros = sum(1 for c in conteudo if c not in alfabeto and not c.isspace())
    if letras == 0:
        return False
    return letras >= outros

def eh_arquivo_de_texto_valido_numeros(conteudo):
    letras = sum(1 for c in conteudo if c.isalpha())
    numeros = sum(1 for c in conteudo if c.isdigit())
    if letras + numeros == 0:
        return False
    proporcao = numeros / (letras + numeros)
    return proporcao <= 0.1

def baixar_livros_gutenberg_direto(tamanho_alvo_mb=1000):
    tamanho_alvo_bytes = tamanho_alvo_mb * 1024 * 1024
    tamanho_total_baixado = 0
    livros_baixados = 0

    diretorio_livros = "livros_gutenberg"
    os.makedirs(diretorio_livros, exist_ok=True)

    print(f"Meta de download: {tamanho_alvo_mb} MB. Iniciando download direto...")

    for livro_id in range(1, 60000):
        if tamanho_total_baixado >= tamanho_alvo_bytes:
            print("\nMeta de download atingida!")
            break

        url = f"https://www.gutenberg.org/files/{livro_id}/{livro_id}-0.txt"

        try:
            resposta = requests.get(url, timeout=10)
            if resposta.status_code != 200:
                continue

            conteudo_texto = resposta.text

            if 'not found' in conteudo_texto.lower() or '<html' in conteudo_texto.lower():
                continue

            if not eh_arquivo_de_texto_valido_caracteres(conteudo_texto):
                print(f"ID {livro_id} descartado (caracteres inválidos).")
                continue

            if not eh_arquivo_de_texto_valido_numeros(conteudo_texto):
                print(f"ID {livro_id} descartado (números em excesso).")
                continue

            tamanho_arquivo = len(resposta.content)
            caminho_arquivo = os.path.join(diretorio_livros, f"livro_{livro_id}.txt")

            with open(caminho_arquivo, "w", encoding="utf-8") as f:
                f.write(conteudo_texto)

            tamanho_total_baixado += tamanho_arquivo
            livros_baixados += 1
            tamanho_atual_mb = tamanho_total_baixado / (1024 * 1024)

            print(f"✔ Sucesso! Livro ID {livro_id} salvo. Tamanho: {tamanho_arquivo/1024:.2f} KB.")
            print(f"   Progresso: {tamanho_atual_mb:.2f} MB / {tamanho_alvo_mb} MB")

        except requests.RequestException:
            continue

    print("\n--- Resumo do Download ---")
    print(f"Total de livros baixados: {livros_baixados}")
    print(f"Tamanho total baixado: {tamanho_total_baixado / (1024 * 1024):.2f} MB")
    print(f"Os livros estão salvos no diretório: '{diretorio_livros}'")


if __name__ == "__main__":
    baixar_livros_gutenberg_direto(tamanho_alvo_mb=100)
