import os
import json
import subprocess
from pathlib import Path

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
    if (raw_cache.startswith('"') and raw_cache.endswith('"')) or (raw_cache.startswith("'") and raw_cache.endswith("'")):
        raw_cache = raw_cache[1:-1]
    
    try:
        cache_data = json.loads(raw_cache)
        clean_cache = json.dumps(cache_data)
        
        home = Path.home()
        
        # Mapeia todas as localizações possíveis onde o SpotiAFK procura o token
        target_paths = [
            Path(".cache"),
            Path(f".cache-{client_id}"),
            Path("spotiafk.cache"),
            home / ".cache" / "spotiafk" / ".cache",
            home / ".cache" / "spotiafk" / "cache",
            home / ".config" / "spotiafk" / ".cache",
            home / ".config" / "spotiafk" / "cache",
            home / ".cache" / "spotiafk" / f".cache-{client_id}",
            home / ".config" / "spotiafk" / f".cache-{client_id}",
        ]
        
        for p in target_paths:
            p.parent.mkdir(parents=True, exist_ok=True)
            with open(p, "w") as f:
                f.write(clean_cache)
                
        print("--> SPOTIFY_CACHE gravada em todas as pastas de sistema!", flush=True)
    except Exception as e:
        print(f"--> ERRO no JSON: {e}", flush=True)
else:
    print("--> ERRO: SPOTIFY_CACHE nao encontrada!", flush=True)

subprocess.run(["poetry", "run", "python", "-m", "spotiafk", "run"])
