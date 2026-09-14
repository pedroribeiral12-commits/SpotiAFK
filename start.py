import os
import json
import subprocess
import threading
from pathlib import Path
from http.server import BaseHTTPRequestHandler, HTTPServer

client_id = os.getenv("CLIENT_ID", "").strip()
client_secret = os.getenv("CLIENT_SECRET", "").strip()
raw_cache = os.getenv("SPOTIFY_CACHE", "").strip()

# Diretório de dados do SpotiAFK
data_home = Path("/opt/render/project/src/.local/share")
state_dir = data_home / "spotiafk"

os.environ["XDG_DATA_HOME"] = str(data_home)

# Configuração
config_content = f"""playlist = "Best drake songs ever (2)"
play_on = ["iPhone"]

[spotify]
client_id = "{client_id}"
client_secret = "{client_secret}"
redirect_uri = "http://127.0.0.1:8888/callback/"
state_dir = "{state_dir}"
"""

with open("spotiafk.toml", "w", encoding="utf-8") as f:
    f.write(config_content)

# Restaurar token do Spotify
if not raw_cache:
    print("--> ERRO: SPOTIFY_CACHE nao encontrada!", flush=True)
else:
    try:
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


# Mini servidor HTTP para o Render
class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(b"SpotiAFK is running")

    def log_message(self, format, *args):
        pass


def run_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), HealthHandler)
    print(f"--> Health server running on port {port}", flush=True)
    server.serve_forever()


# Iniciar servidor do Render numa thread
threading.Thread(target=run_server, daemon=True).start()

# Iniciar SpotiAFK
subprocess.run(
    ["poetry", "run", "python", "-m", "spotiafk", "run"],
    check=False
)
