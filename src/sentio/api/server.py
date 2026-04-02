"""gRPC server for SENTIO real-time inference.

Exposes the narrative intelligence engine as a gRPC service
for integration with the Sylvain venue control system.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List

from pydantic import BaseModel


class EmotionResponse(BaseModel):
    """Emotion classification result."""
    joy: float
    tension: float
    sorrow: float
    wonder: float
    fear: float
    excitement: float
    valence: float
    arousal: float
    confidence: float
    frame_number: int


class OrchestrationCommand(BaseModel):
    """Command to be sent to a subsystem."""
    target: str
    action: str
    parameters: Dict[str, Any] = {}
    priority: int = 0


class AnalysisRequest(BaseModel):
    """Request to analyze a film frame."""
    film_id: str
    frame_number: int
    visual_features: List[float] = []
    audio_features: List[float] = []


class SentioService:
    """gRPC service implementation for SENTIO.

    Endpoints:
    - AnalyzeFrame: Single frame emotion analysis
    - StreamAnalysis: Continuous streaming analysis
    - GetOrchestrationCommands: Get subsystem commands for current state
    - GetEmotionalArc: Get emotional trajectory for a scene
    """

    def __init__(self):
        self._running = False
        self._current_film: str | None = None

    def start(self, host: str = "0.0.0.0", port: int = 50051) -> None:
        """Start the gRPC server."""
        self._running = True

    def stop(self) -> None:
        """Stop the gRPC server."""
        self._running = False

    def analyze_frame(self, request: AnalysisRequest) -> EmotionResponse:
        """Analyze a single frame and return emotion scores."""
        return EmotionResponse(
            joy=0.0,
            tension=0.0,
            sorrow=0.0,
            wonder=0.0,
            fear=0.0,
            excitement=0.0,
            valence=0.0,
            arousal=0.0,
            confidence=0.0,
            frame_number=request.frame_number,
        )

    @property
    def is_running(self) -> bool:
        return self._running
