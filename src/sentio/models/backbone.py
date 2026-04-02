"""NarrativeTransformer backbone architecture.

The core neural architecture powering SENTIO's narrative intelligence.
Processes multi-modal inputs (visual features, audio features, narrative
structure) through a unified transformer encoder.

Architecture specs per Sylvain reference:
- 50+ PFLOPS processing (Zhilicon Neural Engine)
- 1.5T parameter model capacity
- <10ms inference latency
- 98.7% emotion detection accuracy
"""

from dataclasses import dataclass
from typing import Optional

import torch
import torch.nn as nn


@dataclass
class NarrativeTransformerConfig:
    """Configuration for the NarrativeTransformer model."""
    # Model dimensions
    hidden_size: int = 1024
    num_attention_heads: int = 16
    num_layers: int = 24
    intermediate_size: int = 4096
    dropout: float = 0.1

    # Input dimensions
    visual_feature_dim: int = 2048
    audio_feature_dim: int = 512
    narrative_feature_dim: int = 256

    # Output dimensions
    num_emotion_classes: int = 6  # joy, tension, sorrow, wonder, fear, excitement
    max_sequence_length: int = 512

    # Inference
    target_latency_ms: float = 10.0
    target_accuracy: float = 0.987

    @classmethod
    def base(cls) -> "NarrativeTransformerConfig":
        """Base configuration for real-time inference."""
        return cls()

    @classmethod
    def large(cls) -> "NarrativeTransformerConfig":
        """Large configuration for highest accuracy."""
        return cls(
            hidden_size=2048,
            num_attention_heads=32,
            num_layers=48,
            intermediate_size=8192,
        )


class MultiModalFusion(nn.Module):
    """Fuses visual, audio, and narrative features into a unified representation."""

    def __init__(self, config: NarrativeTransformerConfig):
        super().__init__()
        self.visual_proj = nn.Linear(config.visual_feature_dim, config.hidden_size)
        self.audio_proj = nn.Linear(config.audio_feature_dim, config.hidden_size)
        self.narrative_proj = nn.Linear(config.narrative_feature_dim, config.hidden_size)
        self.layer_norm = nn.LayerNorm(config.hidden_size)

    def forward(
        self,
        visual: torch.Tensor,
        audio: torch.Tensor,
        narrative: Optional[torch.Tensor] = None,
    ) -> torch.Tensor:
        fused = self.visual_proj(visual) + self.audio_proj(audio)
        if narrative is not None:
            fused = fused + self.narrative_proj(narrative)
        return self.layer_norm(fused)


class NarrativeTransformer(nn.Module):
    """Main transformer backbone for narrative intelligence.

    Processes multi-modal cinema features and produces emotional state
    vectors used by the SENTIO orchestration conductor.
    """

    def __init__(self, config: NarrativeTransformerConfig):
        super().__init__()
        self.config = config
        self.fusion = MultiModalFusion(config)

        encoder_layer = nn.TransformerEncoderLayer(
            d_model=config.hidden_size,
            nhead=config.num_attention_heads,
            dim_feedforward=config.intermediate_size,
            dropout=config.dropout,
            batch_first=True,
        )
        self.encoder = nn.TransformerEncoder(
            encoder_layer,
            num_layers=config.num_layers,
        )

        # Emotion classification head
        self.emotion_head = nn.Sequential(
            nn.Linear(config.hidden_size, config.hidden_size // 2),
            nn.GELU(),
            nn.Dropout(config.dropout),
            nn.Linear(config.hidden_size // 2, config.num_emotion_classes),
            nn.Sigmoid(),  # Multi-label output [0, 1] per emotion
        )

        # Valence-arousal regression head
        self.valence_arousal_head = nn.Sequential(
            nn.Linear(config.hidden_size, 128),
            nn.GELU(),
            nn.Linear(128, 2),  # [valence, arousal]
            nn.Tanh(),
        )

    def forward(
        self,
        visual: torch.Tensor,
        audio: torch.Tensor,
        narrative: Optional[torch.Tensor] = None,
    ) -> dict:
        # Fuse multi-modal inputs
        fused = self.fusion(visual, audio, narrative)

        # If single frame, add sequence dimension
        if fused.dim() == 2:
            fused = fused.unsqueeze(1)

        # Transformer encoding
        encoded = self.encoder(fused)

        # Pool over sequence dimension
        pooled = encoded.mean(dim=1)

        return {
            "emotions": self.emotion_head(pooled),
            "valence_arousal": self.valence_arousal_head(pooled),
            "features": pooled,
        }

    def parameter_count(self) -> int:
        """Total trainable parameters."""
        return sum(p.numel() for p in self.parameters() if p.requires_grad)
