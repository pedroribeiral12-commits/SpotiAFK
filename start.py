import os
import subprocess
import sys

client_id = os.getenv("CLIENT_ID", "")
client_secret = os.getenv("CLIENT_SECRET", "")

# Playback settings MUST go at the very top, before [spotify]
config_content = f"""playlist = "Best drake songs ever"
play_on = ["iPhone"]

[spotify]
client_id = "{client_id}"
client_secret = "{client_secret}"
redirect_uri = "http://127.0.0.1:8888/callback"
"""

with open("spotiafk.toml", "w") as f:
    f.write(config_content)

print("spotiafk.toml generated successfully!", flush=True)

# Launch SpotiAFK
subprocess.run(["poetry", "run", "python", "-m", "spotiafk", "run"])
