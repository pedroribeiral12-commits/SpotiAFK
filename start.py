import os
import json
import subprocess
from pathlib import Path

client_id = os.getenv("CLIENT_ID", "").strip()
client_secret = os.getenv("CLIENT_SECRET", "").strip()
raw_cache = os.getenv("SPOTIFY_CACHE", "").strip()

# Diretório de dados do SpotiAFK no Render
data_home = Path("/opt/render/project/src/.local/share")
state_dir = data_home / "spotiafk"

os.environ["XDG_DATA_HOME"] = str(data_home)

# Configuração
config_content = f"""playlist = "6rir2yuNUI8p7jjpTvi2wE"
play_on = ["iPhone"]

[spotify]
client_id = "{client_id}"
client_secret = "{client_secret}"
redirect_uri = "http://127.0.0.1:8888/callback/"
state_dir = "{state_dir}"
"""

with open("spotiafk.toml", "w", encoding="utf-8") as f:
    f.write(config_content)

# Restaurar cache do Spotify
if not raw_cache:
    print("--> ERRO: SPOTIFY_CACHE nao encontrada!", flush=True)
else:
    try:
        # Remove aspas exteriores, caso existam
        if (
            (raw_cache.startswith('"') and raw_cache.endswith('"'))
            or
            (raw_cache.startswith("'") and raw_cache.endswith("'"))
        ):
            raw_cache = raw_cache[1:-1]

        cache_data = json.loads(raw_cache)
        clean_cache = json.dumps(cache_data)

        state_dir.mkdir(parents=True, exist_ok=True)

        token_path = state_dir / "token.dat"

        with open(token_path, "w", encoding="utf-8") as f:
            f.write(clean_cache)

        print(f"--> Spotify token gravado em: {token_path}", flush=True)

    except Exception as e:
        print(f"--> ERRO ao processar SPOTIFY_CACHE: {e}", flush=True)

# Iniciar SpotiAFK
subprocess.run(
    ["poetry", "run", "python", "-m", "spotiafk", "run"],
    check=False
)
