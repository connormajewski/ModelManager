import dotenv
import os

dotenv_file_path = ".env"

env_data = dotenv.load_dotenv(dotenv_file_path)

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
runame = os.getenv("RUNAME")
dev_id = os.getenv("DEV_ID")
refresh_token = os.getenv("REFRESH_TOKEN")
access_token = os.getenv("ACCESS_TOKEN")
database_file = os.getenv("DATABASE_FILE")

def set_refresh_token(token):
    
    dotenv.set_key(dotenv_file_path, "REFRESH_TOKEN", tokens)
    
    refresh_token = os.getenv("REFRESH_TOKEN")
    
    return refresh_token
    
    
    
def set_access_token(token):
    
    dotenv.set_key(dotenv_file_path, "ACCESS_TOKEN", token)
    
    access_token = os.getenv("ACCESS_TOKEN")
    
    return access_token