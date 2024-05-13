# Normalize Folder Name CLI

O **Normalize Folder Name CLI** é uma ferramenta de linha de comando desenvolvida para auxiliar usuários a criarem um nome para suas pastas em um formato consistente, seguro e adequado para pastas de projetos de desenvolvimento de software.

## Funcionalidades

Esta ferramenta converte strings de entrada para um formato padronizado, substituindo espaços e caracteres especiais por underscores, removendo acentos e convertendo o texto para minúsculas. Isso facilita a criação de diretórios que são compatíveis com diversos sistemas operacionais e ambientes de desenvolvimento.

## Instalação

Você pode instalar o **Normalize Folder Name CLI** diretamente via PyPI:

```bash
pip install sigaocaue-normalize-folder-name
```
## Uso
Para usar a ferramenta, execute o comando a seguir no seu terminal:
```bash
normalize_folder_name --text "Seu Texto Aqui"
```
Isso irá gerar um nome de pasta normalizado baseado no texto fornecido.

## Exemplos

Aqui estão alguns exemplos de como você pode usar o **Normalize Folder Name CLI**:

- **Entrada:** "Meu Novo Projeto 2024!"
  **Saída:** `normalize_folder_name --text "Meu Novo Projeto 2024!"` produz `meu_novo_projeto_2024`

- **Entrada:** "Repositório de Códigos!"
  **Saída:** `normalize_folder_name --text "Repositório de Códigos!"` produz `repositorio_de_codigos`

Esses exemplos demonstram como a ferramenta transforma textos com espaços, caracteres especiais e acentuação em nomes de pasta adequados para uso em sistemas de arquivos.

## Contribuições

Contribuições para o projeto são bem-vindas e muito apreciadas. Para contribuir, você pode seguir estas etapas:

1. Faça um fork do repositório.
2. Crie uma nova branch para suas modificações (`git checkout -b feature/nova-feature`).
3. Faça suas alterações.
4. Envie suas alterações para revisão (`git push origin feature/nova-feature`).
5. Crie um pull request.

Todas as contribuições serão revisadas antes da incorporação ao projeto principal.

## Licença

Este projeto está licenciado sob a Licença MIT, que permite uso, cópia, modificação, distribuição e venda livremente, desde que a cópia original da licença e o aviso de direitos autorais sejam incluídos em todas as cópias ou partes substanciais do software.

Para mais detalhes, consulte o arquivo `LICENSE` incluído no repositório.


