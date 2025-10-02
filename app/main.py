import os
import shutil
import tempfile
import uuid
from datetime import datetime, timezone

import numpy as np
import matplotlib.pyplot as plt
from fastmcp import FastMCP
from fastmcp.utilities.types import Image
from mcp.types import ImageContent
import requests

# Read hostname from environment (fall back to "localhost" if not set)
HOSTNAME = os.environ.get("HOSTNAME", "localhost")

# Directory where images will be placed and served
TMP_DIR = "tmp"
os.makedirs(TMP_DIR, exist_ok=True)

mcp = FastMCP("My MCP Server")

@mcp.tool()
def get_star() -> ImageContent:
    url = "https://raw.githubusercontent.com/cannin/cannin.github.io/refs/heads/master/images/star_big.png"
    resp = requests.get(url)
    resp.raise_for_status()
    img_data = resp.content
    img = Image(data=img_data, format="png")
    return img.to_image_content()

@mcp.tool()
def get_star_link() -> str:
    return "https://raw.githubusercontent.com/cannin/cannin.github.io/refs/heads/master/images/star_big.png"

@mcp.tool
def greet(name: str) -> str:
    return f"Hello, {name}!"

@mcp.tool
def get_time() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

@mcp.tool
def health() -> dict:
    return {"status": "ok"}


@mcp.tool
def plot_sine_wave(frequency: float = 1.0,
                   duration: float = 2.0,
                   sample_rate: int = 500) -> str:
    """
    Generate a sine wave plot, save via tempfile, then move into tmp directory,
    and return the public URL (always using https).
    """
    # 1. Prepare data
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    y = np.sin(2 * np.pi * frequency * t)

    # 2. Plot
    plt.figure()
    plt.plot(t, y)
    plt.title(f"Sine Wave: {frequency} Hz")
    plt.xlabel("Time [s]")
    plt.ylabel("Amplitude")

    # 3. Save to a temporary file
    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    try:
        plt.savefig(tmp_file.name, format="png")
    finally:
        plt.close()

    # 4. Move / rename into the `tmp` folder under a unique name
    unique_basename = f"sine_{uuid.uuid4().hex}.png"
    dest_path = os.path.join(TMP_DIR, unique_basename)
    shutil.move(tmp_file.name, dest_path)

    # 5. Build the HTTPS URL
    url = f"https://{HOSTNAME}/{unique_basename}"
    return url


if __name__ == "__main__":
    # You MUST configure your HTTP / reverse proxy / FastMCP routing so that
    # requests to https://<HOSTNAME>/<filename>.png are served from tmp/<filename>.png
    mcp.run(transport="http", host="0.0.0.0", port=8000)
