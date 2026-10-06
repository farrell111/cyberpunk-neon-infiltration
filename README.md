<div align="center">

# ⚡ NEON INFILTRATION // CYBERPUNK STEALTH CORE

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Engine](https://img.shields.io/badge/engine-Pygame--CE%20v2.5%2B-orange.svg?style=for-the-badge&logo=python&logoColor=white)](https://pyga.me/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg?style=for-the-badge)]()

**A 2D top-down cyberpunk stealth-puzzle game built with modular Python & Pygame-CE.**  
*100 procedurally generated sectors, diverse operative abilities, raycast-based AI vision, and persistent JSON storage.*

[Features](#-key-features) • [Architecture](#-project-architecture) • [Operative Roster](#-operative-roster) • [Installation](#-installation--quick-start) • [Controls](#-controls)

</div>

---

## 🚀 Key Features

- **Procedural Sector Generation (100 Levels):** Algorithmic maze construction with seed-based scaling parameters (enemy density, patrol velocity, vision ranges, and environmental obstacles).
- **Line-of-Sight Raycasting AI:** Autonomous security drones using vector trigonometry and occlusion raycasting for realistic Field-of-View (FOV) detection.
- **Dynamic Guard State Machine (FSM):** Multi-archetype guards (`PATROL`, `TURRET`, and `STALKER`) transitioning across `PATROL`, `SUSPICIOUS`, and `STUNNED` states.
- **Tactical Environment Hazards:** Pulsing laser tripwires and hackable security terminals that disable detection grids globally on successful bypass.
- **Screen Shake & Neon Particle Physics:** Smooth alpha-blended particle vectors, burst feedback, and trauma-decay camera shake.
- **Local Persistence Pipeline:** Auto-sync JSON storage recording credits, unlocked operatives, and sector progress.

---

## 🎮 Operative Roster

| Operative | Speed | Size | Cost | Special Ability / Passive |
|:---|:---:|:---:|:---:|:---|
| **Specter** | 3.6 | 18px | Free | Standard balanced infiltrator chassis. |
| **Phantom** | 4.6 | 14px | 15 CR | Ultra-compact collision box with sprint agility. |
| **Juggernaut** | 3.0 | 22px | 30 CR | **Energy Shield:** Absorbs 1 alarm trigger per sector. |
| **Glitch** | 3.4 | 18px | 45 CR | **EMP Jammer [SPACE]:** Disables all enemy FOVs for 3.5s. |
| **Blink** | 3.5 | 16px | 60 CR | **Phase Dash [SPACE]:** Teleports 85px in movement direction. |

---

## 🕹️ Controls

| Key Binding | Action |
|:---|:---|
| `W, A, S, D` / `Arrow Keys` | Move Operative |
| `SPACE` | Activate Unique Operative Ability (EMP / Dash) |
| `C` / `ESC` | Toggle Tactical Roster (Unlock & Switch Agents) |
| `1` - `5` | Select / Purchase Operative (in Roster Menu) |
| `R` | Retry current sector (upon alarm trigger) |
| Stand near Terminal | Auto-hack Security Grid (holds for 1.8s) |

---

## 📁 Project Architecture

```text
neon-infiltration/
├── data/
│   └── save_data.json         # Auto-generated persistent player data
├── src/
│   ├── __init__.py            # Package root marker
│   ├── player.py              # Operative classes, skills, and Coin logic
│   ├── enemy.py               # AI Finite State Machine & FOV Raycasting
│   ├── interactive.py         # Laser tripwires and hackable terminals
│   ├── fx.py                  # Particle physics engine & screen trauma
│   ├── map.py                 # Procedural seed-based level synthesizer
│   ├── storage.py             # JSON persistence serializer & deserializer
│   └── renderer.py            # HUD rendering, overlays, and draw calls
├── main.py                    # Core engine loop and state orchestrator
├── requirements.txt           # Project dependencies
└── README.md                  # Documentation and showcase