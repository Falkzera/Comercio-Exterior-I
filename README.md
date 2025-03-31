# 📦 Comercio-Exterior-I

Um buscador de bases de dados do comércio exterior, desenvolvido em Python com interface via [Streamlit](https://streamlit.io/). Com ele, o usuário pode visualizar e filtrar dados por ano, além de baixá-los com facilidade.

## 🌐 Acesse Agora

Você pode acessar o app diretamente pelo navegador, sem precisar instalar nada:

👉 [https://comercio-exterior-1.streamlit.app/](https://comercio-exterior-1.streamlit.app/)

## 🚀 Funcionalidades

- 🔎 Filtragem de dados por ano
- 📚 Download de dados históricos diretamente do site da balança comercial
- 🔁 Atualização automática dos dados do ano corrente
- 📊 Visualização tabular interativa dos dados com paginação
- 💾 Download completo dos dados em formato `.parquet`
- 📦 Dados disponíveis nos modos:
  - `EXP`: Exportações brasileiras
  - `IMP`: Importações brasileiras

## 🛠 Tecnologias Utilizadas

- Python
- Streamlit
- Pandas
- PyArrow
- Requests
- Logging (built-in)

## ⚙️ Instalação Local

Caso queira rodar o projeto localmente:

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/Comercio-Exterior-I.git
cd Comercio-Exterior-I
```
2. Crie um ambiente virtual e ative:
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
```
3. Instale as dependências:
```bash
pip install -r requirements.txt
```
4. Rode o projeto
```bash
streamlit run app.py
```

## ✍️ Créditos

Desenvolvido por: [Lucas Falcão](https://falkzera.streamlit.app/)