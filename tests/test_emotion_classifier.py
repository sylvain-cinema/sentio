"""Tests for the emotion classification system."""

import numpy as np
import pytest

from sentio.emotion.classifier import (
    Emotion,
    EmotionClassifier,
    EmotionalArcTracker,
    EmotionPrediction,
)


class TestEmotionClassifier:
    def test_load_pretrained(self):
        classifier = EmotionClassifier.load_pretrained("sentio-base-v1")
        assert classifier._loaded

    def test_predict_returns_all_emotions(self):
        classifier = EmotionClassifier.load_pretrained("sentio-base-v1")
        features = {"visual": np.zeros(2048), "audio": np.zeros(512)}
        result = classifier.predict(features)

        assert isinstance(result, EmotionPrediction)
        assert len(result.scores) == 6
        for emotion in Emotion:
            assert emotion in result.scores

    def test_prediction_has_valence_arousal(self):
        classifier = EmotionClassifier.load_pretrained("sentio-base-v1")
        features = {"visual": np.zeros(2048), "audio": np.zeros(512)}
        result = classifier.predict(features)

        assert -1.0 <= result.valence <= 1.0
        assert 0.0 <= result.arousal <= 1.0


class TestEmotionalArcTracker:
    def test_update_returns_metrics(self):
        tracker = EmotionalArcTracker(window_size=30)
        prediction = EmotionPrediction(
            scores={e: 0.5 for e in Emotion},
            dominant=Emotion.JOY,
            valence=0.3,
            arousal=0.6,
            confidence=0.9,
        )
        metrics = tracker.update(prediction)

        assert "trend" in metrics
        assert "volatility" in metrics
        assert "intensity" in metrics

    def test_window_respects_size(self):
        tracker = EmotionalArcTracker(window_size=10)
        prediction = EmotionPrediction(
            scores={e: 0.5 for e in Emotion},
            dominant=Emotion.TENSION,
            valence=-0.2,
            arousal=0.8,
            confidence=0.85,
        )
        for _ in range(20):
            tracker.update(prediction)

        assert len(tracker.history) == 10
