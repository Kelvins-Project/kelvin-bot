import tomli

with open("cred.toml", "rb") as file:
    configs = tomli.load(file)

bot_token = configs["configs"]["bot_token"]
lava_token = configs["configs"]["lava_token"]
client_id = configs["configs"]["client_id"]
client_secret = configs["configs"]["client_secret"]
db_link = configs["configs"]["db_link"]