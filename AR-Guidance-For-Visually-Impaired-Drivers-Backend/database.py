from sqlalchemy.orm import declarative_base,sessionmaker
from sqlalchemy import create_engine
#from SensitiveData import username,password,database

Base=declarative_base()
# MySQL URI
DATABASE_URI = "mysql+pymysql://root:abc%40123@localhost/ar_app1"

engine=create_engine(DATABASE_URI,echo=True)
Session=sessionmaker(bind=engine)