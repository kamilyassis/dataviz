# 🫀 ECVD — Estudo de Caso: Saúde Cardiovascular no Brasil

Dashboard interativo para análise espacial e epidemiológica das doenças cardiovasculares no Brasil, com dados de 2025. A aplicação permite explorar internações hospitalares e atendimentos ambulatoriais por município, cruzando dados geoespaciais da INDE com dados populacionais do Censo IBGE 2022.

---

## 📊 Dados

Os datasets são de acesso público, disponibilizados pela **INDE — Infraestrutura Nacional de Dados Espaciais**:

| Dataset | Descrição | Link |
|---|---|---|
| Internações 2025 | Internações hospitalares por DCV por município | [Metadados INDE](https://metadados.inde.gov.br/geonetwork/srv/por/catalog.search#/metadata/55017136-1efd-4f48-80db-885170b6610c) |
| Ambulatórios 2025 | Atendimentos ambulatoriais por DCV por município | [Metadados INDE](https://metadados.inde.gov.br/geonetwork/srv/por/catalog.search#/metadata/8481d11e-b109-4433-8d29-b2b9be1b4904) |

Os dados populacionais são consumidos em tempo real via **API do IBGE** (Censo 2022), utilizados para calcular taxas por 100 mil habitantes.

---

## 🗂️ Estrutura do Projeto

```
├── app_test.py                  # Ponto de entrada da aplicação
├── data/
│   └── dataset.csv              # Dataset consolidado (internações + ambulatórios)
├── utils/
│   ├── data_loader.py           # Carregamento, ETL e cache dos dados
│   └── map_utils.py             # Filtros, cálculo de view e geração de GeoJSON
└── components/
    ├── tab_doc.py               # Aba: Relatório do Projeto
    ├── tab_mapa.py              # Aba: Mapa Interativo (deck.gl)
    ├── tab_rank.py              # Aba: Análise e Ranking (Plotly)
    └── mapa_deck/
        └── index.html           # Componente customizado deck.gl (JS)
```

---

## 🛠️ Tecnologias

| Camada | Tecnologia |
|---|---|
| Aplicação web | [Streamlit](https://streamlit.io/) |
| Dados geoespaciais | [GeoPandas](https://geopandas.org/) + SIRGAS2000/EPSG:4326 |
| Mapa 3D interativo | [deck.gl](https://deck.gl/) via componente customizado |
| Visualizações | [Plotly Express](https://plotly.com/python/plotly-express/) |
| API de população | [IBGE Agregados v3](https://servicodados.ibge.gov.br/api/docs/agregados) |

---

## ▶️ Como rodar

**1. Instale as dependências:**
```bash
pip install streamlit geopandas pandas shapely plotly requests
```

**2. Execute a aplicação:**
```bash
python -m streamlit run app_test.py
```

---

## 👥 Autores

- **Jessica Nagahama**
- **Kamily Assis**