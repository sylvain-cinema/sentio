"""Emotion classification model for narrative analysis.

Uses a transformer encoder with multi-label output to classify emotional
content across six primary dimensions: joy, tension, sorrow, wonder, fear,
and excitement. Operates at 60fps for real-time orchestration.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, List

import numpy as np


class Emotion(Enum):
    """Primary emotional dimensions for cinema narrative."""
    JOY = "joy"
    TENSION = "tension"
    SORROW = "sorrow"
    WONDER = "wonder"
    FEAR = "fear"
    EXCITEMENT = "excitement"


@dataclass
class EmotionPrediction:
    """Emotion classification result for a single frame/scene."""
    scores: Dict[Emotion, float]
    dominant: Emotion
    valence: float      # -1.0 (negative) to 1.0 (positive)
    arousal: float      # 0.0 (calm) to 1.0 (intense)
    confidence: float   # 0.0 to 1.0

    @property
    def intensity(self) -> float:
        """Overall emotional intensity."""
        return max(self.scores.values())


class EmotionClassifier:
    """Multi-label emotion classifier for film content.

    Architecture: Multi-modal transformer encoder that fuses visual
    features (from scene analyzer) and audio features to predict
    emotional content across six dimensions.
    """

    EMOTIONS = list(Emotion)

    def __init__(self, model_path: str | None = None):
        self._model_path = model_path
        self._loaded = False

    @classmethod
    def load_pretrained(cls, model_name: str) -> "EmotionClassifier":
        """Load a pretrained emotion model."""
        instance = cls(model_path=f"models/{model_name}")
        instance._loaded = True
        return instance

    def predict(self, features: Dict[str, np.ndarray]) -> EmotionPrediction:
        """Predict emotions from extracted features.

        Args:
            features: Dict with 'visual' and 'audio' feature arrays.

        Returns:
            EmotionPrediction with scores for all dimensions.
        """
        # Placeholder: in production, runs through transformer model
        scores = {emotion: 0.5 for emotion in self.EMOTIONS}
        dominant = max(scores, key=scores.get)  # type: ignore

        # Compute valence-arousal from emotion scores
        valence = (
            scores[Emotion.JOY] + scores[Emotion.WONDER]
            - scores[Emotion.SORROW] - scores[Emotion.FEAR]
        ) / 2.0

        arousal = (
            scores[Emotion.EXCITEMENT] + scores[Emotion.TENSION]
            + scores[Emotion.FEAR]
        ) / 3.0

        return EmotionPrediction(
            scores=scores,
            dominant=dominant,
            valence=valence,
            arousal=arousal,
            confidence=0.85,
        )


class EmotionalArcTracker:
    """Tracks emotional trajectory over time with temporal smoothing.

    Maintains a sliding window of emotion predictions to detect
    narrative patterns: rising tension, emotional peaks, quiet moments,
    climax detection, and resolution.
    """

    def __init__(self, window_size: int = 300):
        """Initialize arc tracker.

        Args:
            window_size: Number of frames in the smoothing window (300 = 5s at 60fps).
        """
        self.window_size = window_size
        self.history: List[EmotionPrediction] = []

    def update(self, prediction: EmotionPrediction) -> Dict[str, float]:
        """Add a prediction and return arc metrics."""
        self.history.append(prediction)
        if len(self.history) > self.window_size:
            self.history = self.history[-self.window_size:]

        return {
            "trend": self._compute_trend(),
            "volatility": self._compute_volatility(),
            "intensity": self._compute_avg_intensity(),
        }

    def _compute_trend(self) -> float:
        """Compute emotional trend (-1 = declining, +1 = rising)."""
        if len(self.history) < 10:
            return 0.0
        recent = [h.intensity for h in self.history[-10:]]
        older = [h.intensity for h in self.history[-20:-10]] if len(self.history) >= 20 else recent
        return float(np.mean(recent) - np.mean(older))

    def _compute_volatility(self) -> float:
        """Compute emotional volatility (0 = stable, 1 = chaotic)."""
        if len(self.history) < 5:
            return 0.0
        intensities = [h.intensity for h in self.history[-30:]]
        return float(np.std(intensities))

    def _compute_avg_intensity(self) -> float:
        """Average emotional intensity over the window."""
        if not self.history:
            return 0.0
        return float(np.mean([h.intensity for h in self.history]))
