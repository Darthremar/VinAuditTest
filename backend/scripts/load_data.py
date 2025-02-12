import pandas as pd
from sqlalchemy import create_engine

# Configurating database connection
DATABASE_URI = 'postgresql://postgres:Condor92!@localhost:5432/autos_db'

# Loading data from CSV file
file_path = 'C:/Users/USER/OneDrive/Proyectos Personales/VinAuditTest/database/NEWTEST-inventory-listing-2022-08-17.txt'
df = pd.read_csv(file_path, delimiter='|')

# Creating a database connection
engine = create_engine(DATABASE_URI)

# Loading data into the table
df.to_sql('cars', engine, if_exists='append', index=False)

# Printing confirmation message
print("data loaded.") 