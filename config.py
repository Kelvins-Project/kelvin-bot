import tomli

with open("cred.toml", "rb") as file:
    configs = tomli.load(file)

bot_token = configs["configs"]["bot_token"]