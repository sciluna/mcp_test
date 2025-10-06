"""Expose plotting utilities via FastMCP tools."""

from __future__ import annotations

import os
from typing import Tuple

import boto3
from botocore.exceptions import ClientError
from fastmcp import FastMCP

from tools import plotting


def _aws_config() -> Tuple[str, str]:
    bucket = os.environ.get("AWS_S3_BUCKET")
    region = os.environ.get("AWS_DEFAULT_REGION")
    config = (("AWS_S3_BUCKET", bucket), ("AWS_DEFAULT_REGION", region))
    missing = [name for name, value in config if not value]
    if missing:
        raise RuntimeError(f"Missing required AWS configuration: {', '.join(missing)}")
    return bucket, region


def _s3_object_url(bucket: str, key: str, region: str) -> str:
    return f"https://s3.{region}.amazonaws.com/{bucket}/{key}"


def _s3_presigned_url(client, bucket: str, key: str, expires_seconds: int = 3600) -> str:
    try:
        return client.generate_presigned_url(
            ClientMethod="get_object",
            Params={"Bucket": bucket, "Key": key},
            ExpiresIn=expires_seconds,
        )
    except ClientError as exc:
        raise RuntimeError(f"Failed to create presigned URL: {exc}") from exc


def _upload_png(data: bytes, key: str, public: bool) -> str:
    bucket, region = _aws_config()
    client = boto3.client("s3", region_name=region)
    extra_args = {
        "ContentType": "image/png",
        "CacheControl": "public, max-age=31536000",
    }

    try:
        client.put_object(Bucket=bucket, Key=key, Body=data, **extra_args)
    except ClientError as exc:
        raise RuntimeError(f"Failed to upload to S3: {exc}") from exc

    if public:
        return _s3_object_url(bucket, key, region)
    return _s3_presigned_url(client, bucket, key)


def register(mcp: FastMCP) -> None:
    """Register plotting-related tools backed by the tools package."""

    @mcp.tool()
    def plot_sine_wave(
        frequency: float = 1.0,
        duration: float = 2.0,
        sample_rate: int = 500,
        public: bool = True,
    ) -> str:
        """Generate a sine wave plot, upload to S3, and return the accessible URL."""

        key, png_data = plotting.generate_sine_wave_plot(
            frequency=frequency,
            duration=duration,
            sample_rate=sample_rate,
        )
        return _upload_png(png_data, key, public)
