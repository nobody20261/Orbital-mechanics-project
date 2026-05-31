"""
planets.py — Solar System Data
All physical values sourced from NASA Planetary Fact Sheets.
https://nssdc.gsfc.nasa.gov/planetary/factsheet/
"""

# ── Sun ───────────────────────────────────────────────────────────────────────
SUN = {
    "name":           "Sun",
    "mass":           1.989e30,   # kg
    "radius":         6.957e8,    # m
    "color":          "#FDB813",
    "display_radius": 16,         # pixels (not to scale)
}

# ── Planets ───────────────────────────────────────────────────────────────────
# Keys
#   mass                 — kg
#   radius               — m  (mean)
#   orbital_radius       — m  (semi-major axis)
#   eccentricity         — dimensionless
#   orbital_period_days  — Earth days
#   color                — hex colour for display
#   display_radius       — pixel radius on canvas (NOT to physical scale)
#   display_orbit        — pixel orbit radius on canvas (NOT to physical scale)
#   fun_fact             — one-liner shown in info panel

PLANETS = {
    "Mercury": {
        "mass":                3.285e23,
        "radius":              2.439e6,
        "orbital_radius":      5.791e10,
        "eccentricity":        0.206,
        "orbital_period_days": 87.97,
        "color":               "#a8a8a8",
        "display_radius":      4,
        "display_orbit":       58,
        "fun_fact":            "Smallest planet & closest to the Sun",
    },
    "Venus": {
        "mass":                4.867e24,
        "radius":              6.051e6,
        "orbital_radius":      1.082e11,
        "eccentricity":        0.007,
        "orbital_period_days": 224.70,
        "color":               "#e8cda0",
        "display_radius":      7,
        "display_orbit":       92,
        "fun_fact":            "Hottest planet — surface temp 465 °C",
    },
    "Earth": {
        "mass":                5.972e24,
        "radius":              6.371e6,
        "orbital_radius":      1.496e11,
        "eccentricity":        0.017,
        "orbital_period_days": 365.25,
        "color":               "#4fa3e0",
        "display_radius":      7,
        "display_orbit":       128,
        "fun_fact":            "Only known planet harboring life",
    },
    "Mars": {
        "mass":                6.390e23,
        "radius":              3.389e6,
        "orbital_radius":      2.279e11,
        "eccentricity":        0.093,
        "orbital_period_days": 686.97,
        "color":               "#c1440e",
        "display_radius":      5,
        "display_orbit":       170,
        "fun_fact":            "Target for future human exploration",
    },
    "Jupiter": {
        "mass":                1.898e27,
        "radius":              6.991e7,
        "orbital_radius":      7.783e11,
        "eccentricity":        0.049,
        "orbital_period_days": 4332.59,
        "color":               "#c88b3a",
        "display_radius":      14,
        "display_orbit":       238,
        "fun_fact":            "Largest planet — 11× Earth's diameter",
    },
    "Saturn": {
        "mass":                5.683e26,
        "radius":              5.823e7,
        "orbital_radius":      1.432e12,
        "eccentricity":        0.057,
        "orbital_period_days": 10759.22,
        "color":               "#e4d191",
        "display_radius":      12,
        "display_orbit":       298,
        "fun_fact":            "Ring system extends 282,000 km from its surface",
    },
    "Uranus": {
        "mass":                8.681e25,
        "radius":              2.536e7,
        "orbital_radius":      2.867e12,
        "eccentricity":        0.046,
        "orbital_period_days": 30688.50,
        "color":               "#7de8e8",
        "display_radius":      9,
        "display_orbit":       352,
        "fun_fact":            "Rotates on its side — 98° axial tilt",
    },
    "Neptune": {
        "mass":                1.024e26,
        "radius":              2.462e7,
        "orbital_radius":      4.515e12,
        "eccentricity":        0.010,
        "orbital_period_days": 60182.00,
        "color":               "#4b70dd",
        "display_radius":      9,
        "display_orbit":       400,
        "fun_fact":            "Windiest planet — gusts up to 2,100 km/h",
    },
}
