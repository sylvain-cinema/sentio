"""Tests for the scene analysis system."""

import numpy as np
import pytest

from sentio.analyzer.scene import SceneAnalyzer, TransitionType


class TestSceneAnalyzer:
    def test_no_boundary_on_static_frames(self):
        analyzer = SceneAnalyzer()
        frame = np.ones((480, 640, 3), dtype=np.uint8) * 128
        # First frame never returns boundary
        assert analyzer.analyze_frame(frame) is None
        # Same frame again — no change
        assert analyzer.analyze_frame(frame) is None

    def test_detects_cut_on_drastic_change(self):
        analyzer = SceneAnalyzer()
        dark_frame = np.zeros((480, 640, 3), dtype=np.uint8)
        bright_frame = np.ones((480, 640, 3), dtype=np.uint8) * 255

        analyzer.analyze_frame(dark_frame)
        boundary = analyzer.analyze_frame(bright_frame)

        assert boundary is not None
        assert boundary.transition_type == TransitionType.CUT

    def test_extract_features(self):
        analyzer = SceneAnalyzer()
        frame = np.ones((480, 640, 3), dtype=np.uint8) * 128
        features = analyzer.extract_features(frame)

        assert 0.0 <= features.brightness <= 1.0
        assert features.contrast >= 0.0
        assert features.color_temperature > 0
