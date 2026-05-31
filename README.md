# 🚀 Orbital Mechanics Toolkit

**Stanford Code in Place — Final Project**

An interactive solar system simulator and orbital mechanics calculator built entirely with Python's standard library.

![Python](https://img.shields.io/badge/Python-3.6+-blue) ![tkinter](https://img.shields.io/badge/GUI-tkinter-green) ![No dependencies](https://img.shields.io/badge/dependencies-none-brightgreen)

---

## Features

| Feature | Description |
|---|---|
| 🪐 **Live Solar System** | All 8 planets orbit in real time with accurate relative speeds |
| 🔭 **Planet Info Panel** | Click any planet to view mass, radius, gravity, orbital velocity, and escape velocity |
| ⚡ **Hohmann Calculator** | Compute Δv₁, Δv₂, total Δv, and transfer time between any two planets |
| 🛸 **Transfer Orbit Map** | Visualise the Hohmann ellipse overlaid on the solar system |
| ⏩ **Speed Control** | Adjust simulation speed from 0.5 to 60 days per frame |
| ⏸ **Pause / Resume** | Freeze the simulation at any moment |

---

## Physics Behind the Toolkit

All calculations use real Newtonian gravity and Kepler's Laws with NASA planetary data.

| Quantity | Formula |
|---|---|
| Orbital Period | `T = 2π √(a³ / GM)` |
| Orbital Velocity | `v = √(GM / r)` |
| Escape Velocity | `v_esc = √(2GM / r)` |
| Surface Gravity | `g = GM / r²` |
| Hohmann Δv₁ (departure) | `Δv₁ = v_transfer_peri − v_circ_1` |
| Hohmann Δv₂ (arrival) | `Δv₂ = v_circ_2 − v_transfer_apo` |

### Example: Earth → Mars
| Value | Result |
|---|---|
| Δv₁ | ~2.94 km/s |
| Δv₂ | ~2.64 km/s |
| Total Δv | ~5.59 km/s |
| Transfer time | ~259 days |

---

## Running the Project

**Requirements:** Python 3.6 or newer. `tkinter` ships with Python — nothing to install.

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/orbital-mechanics-toolkit
cd orbital-mechanics-toolkit

# Run
python main.py
```

> **Note for Linux users:** If tkinter is missing, run `sudo apt install python3-tk`

---

## File Structure

```
orbital-mechanics-toolkit/
├── main.py          # Entry point — run this
├── planets.py       # Planetary data (NASA Planetary Fact Sheets)
├── calculator.py    # Physics: period, velocity, escape vel, Hohmann
├── visualizer.py    # tkinter GUI, animation, event handling
└── README.md
```

---

## How to Use

1. **Run** `python main.py`
2. **Click any planet** to see its full orbital data in the right panel
3. **Select From / To planets** in the Hohmann Transfer section and click **⚡ CALCULATE**
4. **Check "Show transfer orbit"** to overlay the transfer ellipse on the map
5. **Adjust the speed slider** to slow down or speed up the simulation
6. **Click pause** to freeze and study any moment

---

## Data Sources

Planetary data sourced from the [NASA Planetary Fact Sheets](https://nssdc.gsfc.nasa.gov/planetary/factsheet/).

---

## Concepts Used

This project covers everything taught in Code in Place:

- **Variables & data types** — physical constants, planet properties
- **Dictionaries** — storing and retrieving all planet data
- **Functions** — each physics formula is its own reusable function
- **Control flow** — animation loop, event handling, conditional rendering
- **Math module** — `sqrt`, `pi`, `cos`, `sin` for orbital geometry
- **Classes** — the entire app is one well-structured class
- **tkinter** — canvas drawing, widgets, event binding, animation with `after()`

---

*Built with ❤️ and real rocket science.*
