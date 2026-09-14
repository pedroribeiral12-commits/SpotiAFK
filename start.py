import os
import subprocess

client_id = os.getenv("CLIENT_ID", "")
client_secret = os.getenv("CLIENT_SECRET", "")

config_content = f"""[spotify]
client_id = "{client_id}"
client_secret = "{client_secret}"
redirect_uri = "http://127.0.0.1:8888/callback"
playlist = "Best drake songs ever"
play_on = ["iPhone"]
"""

# Open, write, and explicitly close the file before proceeding
with open("spotiafk.toml", "w") as f:
    f.write(config_content)
    f.flush()

print("spotiafk.toml generated successfully!")

# Now launch SpotiAFK
subprocess.run(["poetry", "run", "python", "-m", "spotiafk", "run"])
