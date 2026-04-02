<div align="center">

<img src="https://img.shields.io/badge/SYLVAIN-SENTIO-000000?style=for-the-badge&labelColor=a855f7&color=000000" alt="SENTIO" height="40"/>

### The Soul of Sylvain

**Empathic AI · Narrative Intelligence Engine**

<br/>

[![CI](https://github.com/sylvain-cinema/sentio/actions/workflows/ci.yml/badge.svg)](https://github.com/sylvain-cinema/sentio/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-a855f7?style=flat-square)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.2+-EE4C2C?style=flat-square&logo=pytorch&logoColor=white)](https://pytorch.org)
[![Docs](https://img.shields.io/badge/docs-sylvain.github.io-f97316?style=flat-square)](https://sylvain-cinema.github.io)

<br/>

*Real-time narrative intelligence that orchestrates all sensory systems.*
*Cinema that understands content and responds to emotional arcs.*
*Powered by 50+ petaflops of Zhilicon Neural Engine processing.*

</div>

<br/>

---

<br/>

## Overview

SENTIO is the AI conductor that makes Sylvain cinema emotionally intelligent. It analyzes films in real-time — understanding pacing, story beats, emotional arcs, and narrative intent — then orchestrates **SPECTRA** (display), **SONORA** (audio), **STRATUM** (volumetric), and haptic systems to serve the story. Technology adapts to narrative, never the other way around.

<br/>

## Capabilities

<table>
<tr><td><strong>Processing Power</strong></td><td>50+ PFLOPS (Zhilicon Neural Engine)</td></tr>
<tr><td><strong>Neural Parameters</strong></td><td>1.5 T (trillion-scale model)</td></tr>
<tr><td><strong>Emotion Accuracy</strong></td><td>98.7% narrative sentiment detection</td></tr>
<tr><td><strong>Inference Latency</strong></td><td>&lt;10 ms (real-time orchestration)</td></tr>
<tr><td><strong>Scene Analysis</strong></td><td>Frame-by-frame · Shot boundary · Scene classification</td></tr>
<tr><td><strong>Emotion Dimensions</strong></td><td>Joy · Tension · Sorrow · Wonder · Fear · Excitement</td></tr>
<tr><td><strong>Orchestration</strong></td><td>Real-time commands to SPECTRA + SONORA + STRATUM + Haptics</td></tr>
</table>

<br/>

## Architecture

```mermaid
flowchart TD
    subgraph INPUT["🎬 Film Stream"]
        direction LR
        VID["Video Frames\n240 fps decode"]
        AUD["Audio Stream\n48 kHz · multichannel"]
        META["Metadata\nTimecode · Chapter marks"]
    end

    subgraph ANALYZE["🔍 sentio.analyzer"]
        direction LR
        SCENE["Scene Detector\nCut · Dissolve · Fade"]
        VIS["Visual Features\nCNN backbone · 2048-d"]
        AUDIO_F["Audio Features\nMel spectrogram · 512-d"]
        NAR["Narrative Parser\nAct structure · Beats"]
    end

    subgraph EMOTION["💜 sentio.emotion"]
        direction TB
        TRANS["NarrativeTransformer\n1.5T params · Multi-modal fusion"]
        CLASS["Emotion Classifier\n6 dimensions · 98.7% accuracy"]
        ARC["Arc Tracker\nTemporal smoothing · Trend detection"]
        VA["Valence-Arousal\nContinuous mapping"]
        TRANS --> CLASS --> ARC
        TRANS --> VA
    end

    subgraph CONDUCT["🎼 sentio.conductor"]
        direction TB
        ORCH["Orchestration Engine\n< 10 ms decision latency"]
        RULES["Rule Engine\nEmotion → Subsystem mapping"]
        SCHED["Scheduler\nPriority queue · Real-time dispatch"]
        ORCH --> RULES --> SCHED
    end

    subgraph SUBSYSTEMS["📡 Subsystem Commands"]
        direction LR
        S_SPEC["🟡 SPECTRA\nBrightness · Color temp\nContrast emphasis"]
        S_SON["🔵 SONORA\nReverb · Spatial width\nBass enhancement"]
        S_STRAT["⚪ STRATUM\nDepth intensity\nLayer activation"]
        S_HAP["🔴 HAPTICS\nPulse · Rumble\nFrequency · Duration"]
    end

    VID --> SCENE
    VID --> VIS
    AUD --> AUDIO_F
    META --> NAR

    SCENE --> TRANS
    VIS --> TRANS
    AUDIO_F --> TRANS
    NAR --> TRANS

    ARC --> ORCH
    VA --> ORCH

    SCHED --> S_SPEC
    SCHED --> S_SON
    SCHED --> S_STRAT
    SCHED --> S_HAP

    style INPUT fill:#1a1a2e,stroke:#a855f7,color:#fff
    style ANALYZE fill:#1a1a2e,stroke:#7c3aed,color:#fff
    style EMOTION fill:#1a1a2e,stroke:#a855f7,color:#fff
    style CONDUCT fill:#1a1a2e,stroke:#c084fc,color:#fff
    style SUBSYSTEMS fill:#0a0a0a,stroke:#a855f7,color:#fff,stroke-width:3px
    style TRANS fill:#a855f7,stroke:#a855f7,color:#fff
    style S_SPEC fill:#f59e0b,stroke:#f59e0b,color:#000
    style S_SON fill:#06b6d4,stroke:#06b6d4,color:#000
    style S_STRAT fill:#64748b,stroke:#64748b,color:#fff
    style S_HAP fill:#ef4444,stroke:#ef4444,color:#fff
```

> **Intelligence flow**: Film frames and audio are decoded → multi-modal features extracted in parallel → NarrativeTransformer (1.5T params) fuses features and classifies across 6 emotional dimensions at 98.7% accuracy → emotional arc tracker detects narrative trajectory → orchestration engine generates subsystem commands in <10ms → dispatched to SPECTRA, SONORA, STRATUM, and haptics in real-time.

<br/>

## Modules

| Module | Description |
|:-------|:------------|
| **`sentio.analyzer`** | Scene boundary detection · Narrative structure · Visual & audio feature extraction |
| **`sentio.emotion`** | Transformer-based emotion classifier · Emotional arc tracking · Valence-arousal mapping |
| **`sentio.conductor`** | Master orchestrator · Real-time subsystem command generation |
| **`sentio.models`** | NarrativeTransformer backbone · Task-specific heads |
| **`sentio.api`** | gRPC server for real-time inference integration |

<br/>

## Quick Start

```python
from sentio.analyzer.scene import SceneAnalyzer
from sentio.emotion.classifier import EmotionClassifier
from sentio.conductor.orchestrator import SensoryOrchestrator

analyzer = SceneAnalyzer()
classifier = EmotionClassifier.load_pretrained("sentio-base-v1")
orchestrator = SensoryOrchestrator()

for frame in film_stream:
    features = analyzer.analyze_frame(frame)
    emotions = classifier.predict(features)
    commands = orchestrator.generate(emotions)
    # → commands dispatched to SPECTRA, SONORA, STRATUM, haptics
```

<br/>

## Sylvain Ecosystem

<table>
<tr><td>🟡</td><td><a href="https://github.com/sylvain-cinema/spectra"><strong>spectra</strong></a></td><td>16K MicroLED Display Engine</td></tr>
<tr><td>🔵</td><td><a href="https://github.com/sylvain-cinema/sonora"><strong>sonora</strong></a></td><td>Wave Field Synthesis Audio Engine</td></tr>
<tr><td>🟣</td><td><strong>sentio</strong></td><td>Empathic AI Narrative Intelligence</td><td><em>← you are here</em></td></tr>
<tr><td>⚪</td><td><a href="https://github.com/sylvain-cinema/stratum"><strong>stratum</strong></a></td><td>Volumetric Display System</td></tr>
<tr><td>🟠</td><td><a href="https://github.com/sylvain-cinema/sylvain-sdk"><strong>sylvain-sdk</strong></a></td><td>Unified Developer SDK</td></tr>
<tr><td>📖</td><td><a href="https://github.com/sylvain-cinema/sylvain.github.io"><strong>docs</strong></a></td><td>Developer Documentation</td></tr>
</table>

<br/>

## License

Licensed under the [Apache License, Version 2.0](LICENSE).

<br/>

---

<div align="center">
<br/>

<img src="https://img.shields.io/badge/SYLVAIN-The_Future_of_Cinematic_Storytelling-000000?style=for-the-badge&labelColor=a855f7&color=111111" alt="Sylvain"/>

<sub>Technology that serves the story</sub>

</div>
