from sqlalchemy import create_engine
import pandas as pd
import glob
import os
from dotenv import load_dotenv
load_dotenv()

engine = create_engine("mssql+pyodbc://{0}:{1}@{2}:{3}/{4}?driver={5}".format(username,password,ip_add,port,driver))

cnxn = engine.connect()

filename = os.getenv('filename')
result=[]
# getting excel files from Directory Desktop
path = os.getenv('extraction_path')
print(path)
file_type = os.getenv('file_type')
sheet = os.getenv('sheet')
column_to_extract = os.getenv('column_to_extract')

def get_files_from_dir(path,file_type):
    # read all the files with extension .xlsx i.e. excel 
    filenames = glob.glob(path + file_type)
    print('File names:', filenames)
    return filenames

def put_IMEI_in_file():
    filenames = get_files_from_dir(path,file_type)
    # for loop to iterate all excel files 
    for file in filenames:
        try:
            # reading excel files
            print("Reading file = ",file)
            df = pd.read_excel(file, sheet_name=sheet)
            df = df.fillna(value=0)
            print(df)
            df.to_sql("Table",con= engine, schema='dbo', index= True , if_exists='append')

        except Exception as e: print(e)

put_IMEI_in_file()