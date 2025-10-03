import os
import uuid
from datetime import datetime, timezone
import tempfile

import numpy as np
import matplotlib.pyplot as plt
from fastmcp import FastMCP
from fastmcp.utilities.types import Image
from mcp.types import ImageContent
import requests
import boto3
from botocore.exceptions import ClientError


# --- AWS / S3 Config ---
AWS_REGION = os.environ.get("AWS_REGION")
AWS_S3_BUCKET = os.environ.get("AWS_S3_BUCKET")

# boto3 uses the default credential chain:
# - Env vars (AWS_ACCESS_KEY_ID / AWS_SECRET_ACCESS_KEY / AWS_SESSION_TOKEN)
s3 = boto3.client("s3", region_name=AWS_REGION)


# --- Local HTTP config (still used for your MCP server itself) ---
HOSTNAME = os.environ.get("HOSTNAME", "localhost")
PORT = os.environ.get("PORT", 8000)

mcp = FastMCP("test-mcp", stateless_http=True)


def _s3_object_url(bucket: str, key: str, region: str) -> str:
    # Path-style URL (works for us-east-1 and many setups)
    return f"https://s3.{region}.amazonaws.com/{bucket}/{key}"


def _s3_presigned_url(bucket: str, key: str, expires_seconds: int = 3600) -> str:
    try:
        return s3.generate_presigned_url(
            ClientMethod="get_object",
            Params={"Bucket": bucket, "Key": key},
            ExpiresIn=expires_seconds,
        )
    except ClientError as e:
        raise RuntimeError(f"Failed to create presigned URL: {e}") from e


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
    public: bool = True,
) -> str:
    """
    Generate a sine wave plot, upload to S3, and return the served URL.
    If `public=True`, returns the S3 object URL (requires public-read access).
    If `public=False`, returns a time-limited presigned URL.
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

    # 3) save to a temp file
    unique_name = f"sine_{uuid.uuid4().hex}.png"
    key = unique_name
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    try:
        plt.savefig(tmp.name, format="png")
    finally:
        plt.close()

    # 4) upload to S3
    extra_args = {
        "ContentType": "image/png",
        "CacheControl": "public, max-age=31536000",
    }

    try:
        s3.upload_file(tmp.name, AWS_S3_BUCKET, key, ExtraArgs=extra_args)
    except ClientError as e:
        # make sure tmp is removed even on failure
        try:
            os.unlink(tmp.name)
        finally:
            raise RuntimeError(f"Failed to upload to S3: {e}") from e
    finally:
        # remove temp file after successful upload as well
        if os.path.exists(tmp.name):
            os.unlink(tmp.name)

    # 5) return URL
    if public:
        return _s3_object_url(AWS_S3_BUCKET, key, AWS_REGION)
    else:
        return _s3_presigned_url(AWS_S3_BUCKET, key)


if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=PORT)
