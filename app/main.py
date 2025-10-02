import os
import uuid
from datetime import datetime, timezone
from pathlib import Path
import tempfile
import shutil

import numpy as np
import matplotlib.pyplot as plt
from fastmcp import FastMCP
from fastmcp.utilities.types import Image
from mcp.types import ImageContent
import requests

# --- Config (single directory, fixed port) ---
HOSTNAME = os.environ.get("HOSTNAME", "localhost")
PORT = 8000
FILES_DIR = Path("files")          # one directory for writing + serving
FILES_DIR.mkdir(exist_ok=True)

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

@mcp.tool()
def greet(name: str) -> str:
    return f"Hello, {name}!"

@mcp.tool()
def get_time() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

@mcp.tool()
def health() -> dict:
    return {"status": "ok"}

@mcp.tool()
def plot_sine_wave(
    frequency: float = 1.0,
    duration: float = 2.0,
    sample_rate: int = 500,
) -> str:
    """
    Generate a sine wave plot, save into `files/`, and return a normal HTTP URL
    that serves the image from /files/<filename>.png.
    """
    # 1) data
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    y = np.sin(2 * np.pi * frequency * t)

    # 2) plot
    plt.figure()
    plt.plot(t, y)
    plt.title(f"Sine Wave: {frequency} Hz")
    plt.xlabel("Time [s]")
    plt.ylabel("Amplitude")

    # 3) write directly into files/ under a unique name
    unique_name = f"sine_{uuid.uuid4().hex}.png"
    dest_path = FILES_DIR / unique_name

    # save atomically: write to tmp, then move into place
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    try:
        plt.savefig(tmp.name, format="png")
    finally:
        plt.close()
    shutil.move(tmp.name, dest_path)

    # 4) return stable HTTP URL (port fixed at 8000)
    return f"http://{HOSTNAME}:{PORT}/files/{unique_name}"

if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=PORT)
