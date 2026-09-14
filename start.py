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

# Escreve o cache nos dois nomes que o Spotipy costuma procurar
if spotify_cache:
    print("--> SPOTIFY_CACHE detetado! A criar ficheiros .cache...", flush=True)
    with open(".cache", "w") as f:
        f.write(spotify_cache)
    if client_id:
        with open(f".cache-{client_id}", "w") as f:
            f.write(spotify_cache)

print("Setup concluido com sucesso!", flush=True)

# Inicia o SpotiAFK
subprocess.run(["poetry", "run", "python", "-m", "spotiafk", "run"])
