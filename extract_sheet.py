# Import library
import gspread as gs
from datetime import datetime
import pandas as pd
import psycopg2     #Library PostgreSQL
from sqlalchemy import create_engine

# Code url
CODE = 'seu_code_url'

# Way key
gc = gs.service_account(filename = 'caminho_json')
sh = gc.open_by_key(CODE)
print(sh)

# Connection worksheet
ws = sh.worksheet('Página1')
print(ws)

# Extract worksheet
import pandas as pd
data = pd.DataFrame(ws.get_all_records())
print(data)

# Output file
output = data.to_csv(r'extract_caminho_saida_csv')

# Creating a data frame
df = pd.DataFrame(data)

# Pritting data types
print(df.dtypes)

### Transforming dataframe 
#
#   Faça as tranformações necessárias em sua tabela.
#

# Creating carga_timestamp
df['carga_timestamp'] = datetime.now()

# Pritting the data frame
print(df)

# Download data frame in .csv
output_transform = df.to_csv(r'transform_caminho_saida_csv', sep=';', encoding = 'utf-8' )

# Conexão com o banco de dados PostgreSQL
conn = psycopg2.connect(
    host="seu_host",
    database="seu_banco_de_dados",
    user="seu_usuario",
    password="sua_senha"
)
print(conn)

# Crie um motor SQLAlchemy
engine = create_engine('postgresql+psycopg2://seu_usuario:sua_senha@seu_host/seu_banco_de_dados')

# Delete e append table
df.to_sql('nome_da_tabela', engine, schema='seu_esquema', if_exists='replace', index=False)

# Fechar conexão
engine.dispose()