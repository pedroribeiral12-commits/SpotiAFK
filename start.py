import os
import subprocess

client_id = os.getenv("CLIENT_ID", "")
client_secret = os.getenv("CLIENT_SECRET", "")
spotify_cache = os.getenv("SPOTIFY_CACHE", "")

config_content = f"""playlist = "Best drake songs ever"
play_on = ["iPhone"]

[spotify]
client_id = "{client_id}"
client_secret = "{client_secret}"
redirect_uri = "http://127.0.0.1:8888/callback"
"""

with open("spotiafk.toml", "w") as f:
    f.write(config_content)

# Cria o ficheiro oculto com o token
if spotify_cache:
    with open(".cache", "w") as f:
        f.write(spotify_cache)

print("Configuration and cache generated successfully!", flush=True)

# Inicia o SpotiAFK
subprocess.run(["poetry", "run", "python", "-m", "spotiafk", "run"])
