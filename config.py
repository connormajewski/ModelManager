import json

config_file_path = "production_config.json"
config_file = open(config_file_path, "r")
config_file_data = json.load(config_file)
config_file.close()

client_id = config_file_data["client_id"]
dev_id = config_file_data["dev_id"]
client_secret = config_file_data["client_secret"]
runame = config_file_data["runame"]

access_token = config_file_data["access_token"]
refresh_token = config_file_data["refresh_token"]