"""Scene boundary detection and analysis.

Detects shot boundaries, scene transitions, and extracts
visual features for emotion classification.
"""

from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

import numpy as np


class TransitionType(Enum):
    """Types of scene transitions."""
    CUT = "cut"
    DISSOLVE = "dissolve"
    FADE_IN = "fade_in"
    FADE_OUT = "fade_out"
    WIPE = "wipe"


@dataclass
class SceneBoundary:
    """A detected scene boundary."""
    frame_number: int
    transition_type: TransitionType
    confidence: float
    visual_change_score: float


@dataclass
class SceneFeatures:
    """Extracted features for a scene segment."""
    brightness: float        # Average brightness (0-1)
    contrast: float          # Contrast ratio
    color_temperature: float # Estimated color temp (Kelvin)
    motion_intensity: float  # Optical flow magnitude
    shot_scale: str          # "close-up", "medium", "wide", "extreme-wide"
    dominant_colors: List[tuple]  # RGB tuples


class SceneAnalyzer:
    """Analyzes film frames to detect scene boundaries and extract features.

    Uses frame differencing for cut detection and gradient analysis
    for dissolve/fade detection.
    """

    def __init__(self, cut_threshold: float = 0.3, dissolve_threshold: float = 0.15):
        self.cut_threshold = cut_threshold
        self.dissolve_threshold = dissolve_threshold
        self._prev_frame: Optional[np.ndarray] = None
        self._frame_count = 0

    def analyze_frame(self, frame: np.ndarray) -> Optional[SceneBoundary]:
        """Analyze a single frame for scene boundaries.

        Args:
            frame: RGB frame as numpy array (H, W, 3), dtype uint8.

        Returns:
            SceneBoundary if a transition is detected, None otherwise.
        """
        self._frame_count += 1

        if self._prev_frame is None:
            self._prev_frame = frame.copy()
            return None

        # Compute frame difference
        diff = np.abs(frame.astype(float) - self._prev_frame.astype(float))
        change_score = float(np.mean(diff) / 255.0)

        self._prev_frame = frame.copy()

        # Cut detection
        if change_score > self.cut_threshold:
            return SceneBoundary(
                frame_number=self._frame_count,
                transition_type=TransitionType.CUT,
                confidence=min(change_score / self.cut_threshold, 1.0),
                visual_change_score=change_score,
            )

        # Dissolve detection (gradual change)
        if change_score > self.dissolve_threshold:
            return SceneBoundary(
                frame_number=self._frame_count,
                transition_type=TransitionType.DISSOLVE,
                confidence=change_score / self.cut_threshold,
                visual_change_score=change_score,
            )

        return None

    def extract_features(self, frame: np.ndarray) -> SceneFeatures:
        """Extract visual features from a frame."""
        brightness = float(np.mean(frame) / 255.0)
        contrast = float(np.std(frame) / 128.0)

        # Estimate color temperature from average color
        avg_color = np.mean(frame, axis=(0, 1))
        r, g, b = avg_color[0], avg_color[1], avg_color[2]
        warmth = (r - b) / 255.0
        color_temp = 5500.0 + warmth * 3000.0

        return SceneFeatures(
            brightness=brightness,
            contrast=contrast,
            color_temperature=color_temp,
            motion_intensity=0.0,  # Requires optical flow computation
            shot_scale="medium",   # Requires ML classification
            dominant_colors=[(int(r), int(g), int(b))],
        )
