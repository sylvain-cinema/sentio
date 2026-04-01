"""Sensory orchestration conductor.

The master orchestrator that translates emotional analysis into real-time
commands for all Sylvain subsystems: SPECTRA (display), SONORA (audio),
STRATUM (volumetric), and haptics.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class SubsystemCommand:
    """A command to be sent to a Sylvain subsystem."""
    target: str          # "spectra", "sonora", "stratum", "haptic"
    action: str          # e.g., "adjust_brightness", "set_reverb", "set_depth"
    parameters: Dict[str, Any] = field(default_factory=dict)
    priority: int = 0    # Higher = more urgent
    timestamp_ms: int = 0


class SensoryOrchestrator:
    """Maps emotional state to subsystem commands.

    The orchestrator ensures technology always serves the story:
    - High tension → subtle display darkening, tighter audio reverb
    - Wonder → expanded dynamic range, wider spatial audio field
    - Sorrow → warmer color temperature, intimate audio positioning
    - Excitement → increased brightness, bass enhancement, haptic pulses
    """

    def __init__(self):
        self._rules: List[OrchestratorRule] = self._load_default_rules()

    def generate(self, emotion_state: Dict[str, float]) -> List[SubsystemCommand]:
        """Generate subsystem commands from emotional state.

        Args:
            emotion_state: Dict with emotion scores and arc metrics.

        Returns:
            List of commands for all subsystems.
        """
        commands: List[SubsystemCommand] = []

        intensity = emotion_state.get("intensity", 0.5)
        valence = emotion_state.get("valence", 0.0)
        arousal = emotion_state.get("arousal", 0.5)

        # SPECTRA display commands
        commands.append(SubsystemCommand(
            target="spectra",
            action="adjust_brightness",
            parameters={"factor": 0.8 + 0.4 * intensity},
        ))
        commands.append(SubsystemCommand(
            target="spectra",
            action="adjust_color_temperature",
            parameters={"kelvin": 5500 + int(valence * 1000)},
        ))

        # SONORA audio commands
        commands.append(SubsystemCommand(
            target="sonora",
            action="set_reverb_level",
            parameters={"level": 0.3 + 0.4 * (1.0 - arousal)},
        ))
        commands.append(SubsystemCommand(
            target="sonora",
            action="set_spatial_width",
            parameters={"width": 0.5 + 0.5 * intensity},
        ))

        # STRATUM volumetric commands
        commands.append(SubsystemCommand(
            target="stratum",
            action="set_depth_intensity",
            parameters={"depth": intensity * 0.8},
        ))

        # Haptic commands
        if arousal > 0.7:
            commands.append(SubsystemCommand(
                target="haptic",
                action="pulse",
                parameters={"intensity": arousal, "frequency_hz": 30},
                priority=1,
            ))

        return commands

    def _load_default_rules(self) -> List["OrchestratorRule"]:
        """Load default orchestration rules."""
        return []


@dataclass
class OrchestratorRule:
    """A rule mapping emotional conditions to subsystem responses."""
    name: str
    condition: str      # Expression evaluated against emotion state
    commands: List[SubsystemCommand] = field(default_factory=list)
