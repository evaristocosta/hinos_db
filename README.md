# 🎵 Hinos DB - Base de Dados de Hinos da ICM

![Python](https://img.shields.io/badge/Python-3.11.10-blue)
![Status](https://img.shields.io/badge/Status-Ativo-green)

Repositório para armazenamento, processamento e análise de dados sobre hinos da Igreja Cristã Maranata (ICM). Este projeto mantém um banco de dados estruturado com informações sobre hinos, coletâneas, autores, categorias e suas relações, além de ferramentas para análise exploratória de dados.

## 📋 Sobre o Projeto

Este projeto foi desenvolvido para organizar e analisar sistematicamente a coletânea de hinos da ICM. Ele oferece:

- **Banco de dados SQL** estruturado com informações sobre hinos, coletâneas, autores e categorias
- **Pipeline ETL** para extração de dados de slides em PowerPoint
- **Sistema de migrações** para versionamento do banco de dados
- **Análise exploratória de dados (EDA)** com técnicas de Ciência de Dados e NLP
- **Aplicação web interativa** para visualização dos dados e insights

## 🗂️ Estrutura do Repositório

```
hinos_db/
├── db/                          # Banco de dados e migrações
│   ├── migrations/              # Scripts SQL de migração
│   └── run_migrations.py        # Executor de migrações
├── etl_slides/                  # Pipeline ETL para slides PowerPoint
│   ├── pipeline.py              # Pipeline completo
│   ├── pptx2txt.py              # Extrator de texto dos slides
│   ├── txt2json.py              # Conversor texto → JSON
│   ├── json2sql.py              # Conversor JSON → SQL
│   └── slides_adapt/            # Slides processados
├── adicionar_hino/              # Ferramentas para adicionar novos hinos
│   ├── pipeline.ipynb           # Pipeline de adição
│   └── arquivos_hinos/          # Arquivos de hinos em Markdown
├── eda1/                        # 🌟 Projeto EDA (ver seção especial abaixo)
│   ├── streamlit_app.py         # Aplicação Streamlit
│   ├── src/                     # Código-fonte das análises
│   ├── notebooks/               # Notebooks Jupyter de desenvolvimento
│   └── assets/                  # Dados processados e banco de dados
├── requirements.txt             # Dependências Python
└── README.md                    # Este arquivo
```

## 🗄️ Estrutura do Banco de Dados

O banco de dados possui as seguintes tabelas principais:

- **hino**: Informações principais dos hinos (título, texto, categoria, coletânea)
- **coletanea**: Coletâneas de hinos
- **categoria**: Categorias temáticas dos hinos
- **autor**: Autores e compositores
- **hino_autor**: Relação entre hinos e autores
- **autor_acao**: Tipo de contribuição do autor (letra, melodia, etc.)

## 🔄 Pipeline ETL

O pipeline de extração, transformação e carga (ETL) processa slides do PowerPoint:

1. **pptx2txt**: Extrai texto bruto dos slides
2. **txt2json**: Estrutura os dados em formato JSON
3. **json2sql**: Insere os dados no banco SQL

```bash
python etl_slides/pipeline.py
```

## 🌟 Projeto EDA1 - Análise Exploratória de Dados

O diretório `eda1/` contém um **projeto especial e em desenvolvimento ativo** de Análise Exploratória de Dados (EDA) da Coletânea de Hinos. Este é um projeto contínuo que utiliza técnicas avançadas de Ciência de Dados e Processamento de Linguagem Natural (NLP).

### Características do EDA1:

- ✅ **Análise de Categorias**: Distribuição temática dos hinos
- ✅ **Análise de Títulos**: Padrões e características dos títulos
- ✅ **Análise Textual**: Exploração de palavras-chave e termos frequentes
- ✅ **Word Embeddings**: Representação vetorial de palavras
- ✅ **Sentence Embeddings**: Similaridade semântica entre hinos
- ✅ **Análise de Emoções**: Identificação de sentimentos nas letras
- ✅ **Sistema de Recomendação**: Seleção de hinos similares usando TOPSIS

### Aplicação Web Interativa

O projeto inclui uma aplicação Streamlit com visualizações interativas:

```bash
cd eda1
streamlit run streamlit_app.py
```

### 🚀 Projeto Ativo

Este é um **projeto em desenvolvimento contínuo**! Futuros trabalhos incluem:

- 📊 **EDA2, EDA3, ...**: Novas análises exploratórias com diferentes enfoques
- 🤖 **Machine Learning**: Modelos preditivos e de classificação
- 📈 **Análise Avançada**: Estudos sobre evolução temporal, redes semânticas, etc.
- 🎼 **Análise Musical**: Integração com dados de melodias e harmonias

Para mais detalhes sobre o EDA1, consulte o [README específico](eda1/README.md).

## 🛠️ Instalação e Uso

### Pré-requisitos

- Python 3.11.10
- pip

### Instalação

1. Clone o repositório:

```bash
git clone https://github.com/evaristocosta/hinos_db.git
cd hinos_db
```

2. Instale as dependências:

```bash
pip install -r requirements.txt
```

3. Execute as migrações do banco de dados:

```bash
python db/run_migrations.py
```

## 📚 Tecnologias Utilizadas

- **Python 3.11.10**: Linguagem principal
- **SQLite/SQLAlchemy**: Banco de dados
- **Pandas**: Manipulação de dados
- **Streamlit**: Interface web interativa
- **NLTK**: Processamento de linguagem natural
- **Transformers/Torch**: Modelos de embeddings
- **Scikit-learn**: Machine learning e análise
- **Plotly/Matplotlib/Seaborn**: Visualizações

## 👨‍💻 Autor

**Lucas Piccioni Costa**

- 📧 Email: lucascosta74@gmail.com
- 📸 Instagram: [@lucas.costa74](https://www.instagram.com/lucas.costa74/)
- 💼 LinkedIn: [lucascosta74](https://www.linkedin.com/in/lucascosta74/)
- 🐙 GitHub: [evaristocosta](https://github.com/evaristocosta)

## 📄 Licença

Este projeto é de código aberto e está disponível sob a licença MIT.

---

**Nota**: Este repositório é mantido de forma independente e não possui afiliação oficial com a Igreja Cristã Maranata.
