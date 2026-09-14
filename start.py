import os
import json
import subprocess

client_id = os.getenv("CLIENT_ID", "").strip()
client_secret = os.getenv("CLIENT_SECRET", "").strip()
raw_cache = os.getenv("SPOTIFY_CACHE", "").strip()

config_content = f"""playlist = "Best drake songs ever"
play_on = ["iPhone"]

[spotify]
client_id = "{client_id}"
client_secret = "{client_secret}"
redirect_uri = "http://127.0.0.1:8888/callback"
"""

with open("spotiafk.toml", "w") as f:
    f.write(config_content)

if raw_cache:
    # Remove aspas externas acidentais caso tenham sido coladas do Render
    if (raw_cache.startswith('"') and raw_cache.endswith('"')) or (raw_cache.startswith("'") and raw_cache.endswith("'")):
        raw_cache = raw_cache[1:-1]
    
    try:
        # Valida e re-formata para JSON estrito
        cache_data = json.loads(raw_cache)
        clean_cache = json.dumps(cache_data)
        
        # Escreve nos caminhos possíveis consultados pelo Spotipy
        targets = [".cache", f".cache-{client_id}", "spotiafk.cache"]
        for target in targets:
            with open(target, "w") as f:
                f.write(clean_cache)
                
        print("--> SPOTIFY_CACHE validado e gravado com sucesso!", flush=True)
    except Exception as e:
        print(f"--> ERRO: O JSON na SPOTIFY_CACHE esta mal formatado: {e}", flush=True)
else:
    print("--> ERRO: A variavel SPOTIFY_CACHE nao foi encontrada!", flush=True)

# Inicia o SpotiAFK
subprocess.run(["poetry", "run", "python", "-m", "spotiafk", "run"])
