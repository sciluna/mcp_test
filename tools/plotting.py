"""Plotting utilities that return raw artifacts for downstream adapters."""

from __future__ import annotations

import io
import uuid
from typing import Tuple

import matplotlib.pyplot as plt
import numpy as np

import matplotlib
matplotlib.use('Agg')


def generate_sine_wave_plot(
    frequency: float = 1.0,
    duration: float = 2.0,
    sample_rate: int = 500,
    title: str | None = None,
) -> Tuple[str, bytes]:
    """Create a sine-wave plot and return a unique filename with PNG bytes."""
    if sample_rate <= 0:
        raise ValueError("sample_rate must be positive")
    if duration <= 0:
        raise ValueError("duration must be positive")

    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    y = np.sin(2 * np.pi * frequency * t)

    figure, ax = plt.subplots()
    ax.plot(t, y)
    plot_title = title or f"Sine Wave: {frequency} Hz"
    ax.set_title(plot_title)
    ax.set_xlabel("Time [s]")
    ax.set_ylabel("Amplitude")

    buffer = io.BytesIO()
    figure.savefig(buffer, format="png")
    plt.close(figure)
    buffer.seek(0)
    key = f"sine_{uuid.uuid4().hex}.png"
    return key, buffer.read()
