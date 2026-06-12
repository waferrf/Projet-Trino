# Projet Trino Data Lakehouse + GenAI

Ce projet met en place une architecture locale de Data Lakehouse avec un moteur SQL federe, un stockage objet, un catalogue de metadonnees, une base analytique rapide, un assistant IA local et un dashboard Power BI.

L'objectif est de montrer un flux complet:

1. ingestion de donnees;
2. stockage dans un lakehouse;
3. interrogation avec Trino;
4. analyse rapide avec ClickHouse;
5. exploration avec Streamlit;
6. generation de SQL avec un LLM local;
7. visualisation finale dans Power BI.

## Architecture

- MinIO: stockage objet compatible S3 pour le data lake.
- PostgreSQL: base relationnelle utilisee par le Hive Metastore.
- Hive Metastore: catalogue technique pour Hive et Apache Iceberg.
- Trino: moteur SQL federe pour interroger Iceberg, Hive, ClickHouse et PostgreSQL.
- Apache Iceberg: format lakehouse pour les tables analytiques.
- ClickHouse: base colonne rapide utilisee pour le dataset Power BI.
- Ollama: serveur IA local pour executer le modele `qwen2.5-coder:1.5b`.
- Streamlit: interface web pour explorer les tables et utiliser le Text-to-SQL.
- Power BI: dashboard final connecte aux tables ClickHouse.

## Datasets

Deux datasets sont utilises:

- `data/manju_bhai_sales.csv`: dataset principal stocke dans le Data Lakehouse avec Iceberg.
- `data/products.csv`: dataset produits charge dans ClickHouse pour Power BI.

Le dataset Power BI est volontairement different du dataset Iceberg, car le professeur a demande un autre dataset pour ClickHouse.

Note: `data/manju_bhai_sales.csv` est volumineux et n'est pas pousse sur GitHub. Il doit rester localement dans le dossier `data/` pour executer le pipeline complet.

## Structure du projet

```text
.
|-- clickhouse/init/01_create_tables.sql
|-- data/
|   |-- manju_bhai_sales.csv
|   |-- products.csv
|-- docker-compose.yml
|-- etc/catalog/
|-- etc/hive/metastore-site.xml
|-- hive-metastore/Dockerfile
|-- powerbi/
|   |-- PowerBI.pbix
|   |-- mesures.dax
|   |-- requetes_clickhouse.sql
|-- scripts/
|-- streamlit_app/
|-- README.md
|-- RAPPORT_PROJET.md
```

## Rapport complet

Le rapport detaille du projet est disponible ici:

```text
RAPPORT_PROJET.md
```

## Prerequis

Installer:

- Docker Desktop
- Python 3
- Power BI Desktop
- le driver/connecteur ClickHouse si Power BI ne reconnait pas ClickHouse directement

## Lancement complet

Depuis le dossier du projet:

```powershell
cd C:\Users\user\Desktop\Projet-Trino
.\scripts\setup_all.ps1
```

Ce script:

1. construit et demarre les conteneurs Docker;
2. cree le bucket MinIO `warehouse`;
3. copie les fichiers CSV dans MinIO;
4. importe `data/products.csv` dans ClickHouse;
5. cree les tables Hive et Iceberg avec Trino;
6. telecharge le modele Ollama `qwen2.5-coder:1.5b`.

Si la machine manque de RAM ou si le telechargement du modele prend trop de temps:

```powershell
.\scripts\setup_all.ps1 -SkipModel
.\scripts\pull_ollama_model.ps1
```

## Dashboard Streamlit

Pour lancer l'interface:

```powershell
.\scripts\run_dashboard.ps1
```

URL:

```text
http://localhost:8501
```

L'interface Streamlit contient:

- `Accueil`: supervision de Trino, Ollama, catalogues, schemas et tables.
- `Explorateur de schemas`: exploration des catalogues, schemas, tables, colonnes et apercu des lignes.
- `Produits de donnees`: inspection des tables Iceberg, partitions et snapshots.
- `Assistant SQL`: generation de requetes Trino avec Ollama puis execution du resultat.

L'interface a ete mise a jour avec un design plus professionnel: bandeau principal, cartes de statut, cartes KPI, sections visuelles et meilleure organisation.

## Power BI

Power BI est connecte a ClickHouse avec le dataset `data/products.csv`.

Le fichier Power BI du projet est:

```text
powerbi/PowerBI.pbix
```

### Connexion Power BI Desktop

Dans Power BI Desktop:

1. ouvrir `Obtenir les donnees`;
2. choisir `ClickHouse`;
3. renseigner les informations suivantes:

```text
Host: localhost
Port: 8123
Database: analytics
Data Connectivity mode: DirectQuery
Username: default
Password: clickhouse
```

Si le connecteur ClickHouse n'apparait pas, installer le driver ODBC ClickHouse puis utiliser:

```text
Obtenir les donnees > ODBC
```

### Tables a charger dans Power BI

Selectionner ces tables:

- `products`
- `powerbi_product_kpi_overview`
- `powerbi_product_category_summary`
- `powerbi_product_brand_summary`
- `powerbi_product_stock_summary`
- `powerbi_product_timeline`

### Dashboard Power BI conseille

Page 1 - Overview:

- cartes KPI:
  - `total_products`
  - `total_categories`
  - `total_brands`
  - `avg_price`
  - `avg_rating`
  - `inventory_value`
- graphique en barres: `total_products` par `category`
- graphique donut: `inventory_value` par `category`

Page 2 - Categories:

- matrice: `category`, `subcategory`, `total_products`, `avg_price`, `avg_rating`
- graphique en barres: `total_stock` par `subcategory`

Page 3 - Brands:

- graphique en barres: `total_products` par `brand`
- graphique nuage de points:
  - X: `avg_price`
  - Y: `avg_rating`
  - Taille: `total_reviews`
  - Legende: `category`

Page 4 - Stock:

- graphique en barres: `total_products` par `stock_status`
- table: `category`, `stock_status`, `total_stock`, `inventory_value`

## URLs utiles

- Streamlit Dashboard: http://localhost:8501
- Trino UI: http://localhost:8080
- MinIO Console: http://localhost:9001
- Ollama API: http://localhost:11434
- ClickHouse HTTP: http://localhost:8123

Identifiants MinIO:

```text
user: minioadmin
password: minioadmin
```

## Tables creees

Hive brut:

- `hive.raw.people_csv`
- `hive.raw.sales_csv`

Iceberg:

- `iceberg.lakehouse.people`
- `iceberg.lakehouse.sales`
- `iceberg.lakehouse.sales_partitioned`
- `iceberg.lakehouse.sales_city_summary`

ClickHouse:

- `clickhouse.analytics.products`
- `clickhouse.analytics.powerbi_product_kpi_overview`
- `clickhouse.analytics.powerbi_product_category_summary`
- `clickhouse.analytics.powerbi_product_brand_summary`
- `clickhouse.analytics.powerbi_product_stock_summary`
- `clickhouse.analytics.powerbi_product_timeline`

## Requetes de demo

```powershell
.\scripts\run_demo_queries.ps1
```

Ou directement:

```powershell
docker compose exec -T trino trino --file /project/scripts/demo_queries.sql
```

## Arret du projet

Pour arreter les conteneurs:

```powershell
docker compose down
```

Pour supprimer aussi les volumes:

```powershell
docker compose down -v
```

Attention: `docker compose down -v` supprime les donnees stockees dans MinIO, PostgreSQL, ClickHouse et Ollama.

## Sources utiles

- ClickHouse Power BI: https://clickhouse.com/docs/integrations/powerbi
- ClickHouse ODBC: https://clickhouse.com/docs/interfaces/odbc
- Microsoft Power Query ClickHouse: https://learn.microsoft.com/en-us/power-query/connectors/clickhouse
