"""
visualizer.py — Interactive Solar System GUI
Built with Python's built-in tkinter — no extra installs required.

Layout
──────
  Left  : Animated solar system canvas (880 × 700 px)
  Right : Planet info panel + Hohmann transfer calculator (340 px wide)
  Bottom: Speed slider, pause/play, day counter
"""

import tkinter as tk
from tkinter import ttk
import math
import random

from planets import PLANETS, SUN
from calculator import (
    orbital_period, orbital_velocity, escape_velocity,
    surface_gravity, hohmann_transfer, format_period,
)

# ── Layout & colour constants ─────────────────────────────────────────────────
CANVAS_W, CANVAS_H = 880, 700
CX, CY             = CANVAS_W // 2, CANVAS_H // 2   # solar-system centre

BG        = "#050510"
PANEL_BG  = "#090918"
ACCENT    = "#00d4ff"
DIM       = "#8888aa"
BORDER    = "#1a1a3a"
TEXT_FG   = "#dce0ff"

FONT_TITLE  = ("Courier New", 16, "bold")
FONT_HEADER = ("Courier New", 10, "bold")
FONT_BODY   = ("Courier New", 9)
FONT_SMALL  = ("Courier New", 8)
# ─────────────────────────────────────────────────────────────────────────────


class OrbitalMechanicsToolkit:
    """Main application class — creates the window and runs the event loop."""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🚀 Orbital Mechanics Toolkit")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)

        # ── Simulation state ──────────────────────────────────────────────
        self.time_days  = 0.0        # elapsed simulation time
        self.running    = True       # animation playing?
        self.selected   = None       # currently selected planet name
        self._transfer  = None       # stored Hohmann result for map overlay

        self._build_ui()
        self._draw_stars()           # static star field drawn once
        self._animate()              # kick off the render loop
        self.root.mainloop()

    # ── UI construction ───────────────────────────────────────────────────────

    def _build_ui(self):
        root = self.root

        # Title
        tk.Label(
            root, text="🚀  ORBITAL MECHANICS TOOLKIT",
            font=FONT_TITLE, bg=BG, fg=ACCENT,
        ).pack(pady=(12, 6))

        # Main row: canvas + right panel
        row = tk.Frame(root, bg=BG)
        row.pack(padx=12, pady=4)

        self.canvas = tk.Canvas(
            row, width=CANVAS_W, height=CANVAS_H,
            bg=BG, highlightthickness=1, highlightbackground=BORDER,
        )
        self.canvas.pack(side=tk.LEFT)
        self.canvas.bind("<Button-1>", self._on_click)

        self._build_panel(row)

        # Bottom controls bar
        self._build_controls(root)

    def _build_panel(self, parent):
        """Right-side info & Hohmann calculator panel."""
        panel = tk.Frame(
            parent, bg=PANEL_BG, width=340,
            highlightthickness=1, highlightbackground=BORDER,
        )
        panel.pack(side=tk.LEFT, fill=tk.Y, padx=(8, 0))
        panel.pack_propagate(False)

        pad = dict(padx=12, pady=4)

        # ── Planet info ───────────────────────────────────────────────────
        tk.Label(panel, text="PLANET INFO", font=FONT_HEADER,
                 bg=PANEL_BG, fg=ACCENT).pack(anchor=tk.W, **pad)

        self.info_box = tk.Text(
            panel, width=36, height=16, bg="#06060f", fg=TEXT_FG,
            font=FONT_BODY, relief=tk.FLAT, state=tk.DISABLED,
            wrap=tk.WORD, cursor="arrow",
        )
        self.info_box.pack(padx=10, pady=(0, 4))
        self._add_text_tags(self.info_box)
        self._set_default_info()

        # Divider
        tk.Frame(panel, bg=BORDER, height=1).pack(fill=tk.X, padx=8, pady=6)

        # ── Hohmann transfer ──────────────────────────────────────────────
        tk.Label(panel, text="HOHMANN TRANSFER", font=FONT_HEADER,
                 bg=PANEL_BG, fg=ACCENT).pack(anchor=tk.W, **pad)

        pnames = list(PLANETS.keys())

        def combo_row(label, default):
            f = tk.Frame(panel, bg=PANEL_BG)
            f.pack(fill=tk.X, padx=12, pady=2)
            tk.Label(f, text=label, font=FONT_BODY,
                     bg=PANEL_BG, fg=DIM, width=7, anchor=tk.W).pack(side=tk.LEFT)
            var = tk.StringVar(value=default)
            ttk.Combobox(f, textvariable=var, values=pnames,
                         width=13, state="readonly",
                         font=FONT_BODY).pack(side=tk.LEFT)
            return var

        self.h_from = combo_row("From :", "Earth")
        self.h_to   = combo_row("To    :", "Mars")

        tk.Button(
            panel, text="⚡  CALCULATE",
            font=FONT_HEADER, bg="#001e3c", fg=ACCENT,
            activebackground="#003366", activeforeground="#ffffff",
            relief=tk.FLAT, cursor="hand2",
            command=self._calc_hohmann, padx=8,
        ).pack(fill=tk.X, padx=12, pady=(8, 4))

        self.h_box = tk.Text(
            panel, width=36, height=9, bg="#06060f", fg=TEXT_FG,
            font=FONT_BODY, relief=tk.FLAT, state=tk.DISABLED,
            wrap=tk.WORD, cursor="arrow",
        )
        self.h_box.pack(padx=10, pady=(0, 4))
        self._add_text_tags(self.h_box)

        self.show_transfer = tk.BooleanVar(value=False)
        tk.Checkbutton(
            panel, text="Show transfer orbit on map",
            variable=self.show_transfer, font=FONT_SMALL,
            bg=PANEL_BG, fg=DIM, selectcolor=PANEL_BG,
            activebackground=PANEL_BG,
        ).pack(anchor=tk.W, padx=12, pady=(0, 8))

    def _build_controls(self, parent):
        """Bottom control bar: speed, pause, day counter."""
        bar = tk.Frame(
            parent, bg="#07071a", height=52,
            highlightthickness=1, highlightbackground=BORDER,
        )
        bar.pack(fill=tk.X, padx=12, pady=(4, 12))
        bar.pack_propagate(False)

        tk.Label(bar, text="SPEED:", font=FONT_BODY,
                 bg="#07071a", fg=DIM).pack(side=tk.LEFT, padx=(16, 4), pady=10)

        self.speed_var = tk.DoubleVar(value=3.0)
        tk.Scale(
            bar, from_=0.5, to=60, resolution=0.5,
            orient=tk.HORIZONTAL, variable=self.speed_var,
            bg="#07071a", fg=ACCENT, troughcolor=BORDER,
            highlightthickness=0, length=220, showvalue=True, label="",
        ).pack(side=tk.LEFT, pady=4)

        tk.Label(bar, text="days/frame", font=FONT_SMALL,
                 bg="#07071a", fg=DIM).pack(side=tk.LEFT, padx=(2, 20))

        self.pause_btn = tk.Button(
            bar, text="⏸  PAUSE",
            font=FONT_HEADER, bg="#0d1a2d", fg=ACCENT,
            activebackground="#1a2e4a", relief=tk.FLAT,
            cursor="hand2", command=self._toggle_pause, padx=14,
        )
        self.pause_btn.pack(side=tk.LEFT)

        self.day_lbl = tk.Label(
            bar, text="Day 0  (Year 0.00)",
            font=FONT_SMALL, bg="#07071a", fg=DIM,
        )
        self.day_lbl.pack(side=tk.RIGHT, padx=16)

    # ── Text-widget helpers ───────────────────────────────────────────────────

    def _add_text_tags(self, widget):
        """Define colour tags for a Text widget."""
        widget.tag_configure("header", foreground=ACCENT,    font=("Courier New", 9, "bold"))
        widget.tag_configure("value",  foreground="#ffffff",  font=FONT_BODY)
        widget.tag_configure("good",   foreground="#00ff88",  font=FONT_BODY)
        widget.tag_configure("warn",   foreground="#ffaa00",  font=FONT_BODY)
        widget.tag_configure("dim",    foreground=DIM,        font=FONT_SMALL)

    def _write(self, widget, parts):
        """
        Populate a read-only Text widget.
        parts — list of (text, tag_name_or_None)
        """
        widget.config(state=tk.NORMAL)
        widget.delete("1.0", tk.END)
        for text, tag in parts:
            widget.insert(tk.END, text, tag) if tag else widget.insert(tk.END, text)
        widget.config(state=tk.DISABLED)

    # ── Star field ────────────────────────────────────────────────────────────

    def _draw_stars(self):
        """Draw a static random star field (called once at startup)."""
        rng = random.Random(2025)
        for _ in range(230):
            x  = rng.randint(0, CANVAS_W)
            y  = rng.randint(0, CANVAS_H)
            sz = rng.choice([1, 1, 1, 2])
            v  = rng.randint(80, 210)
            c  = f"#{v:02x}{v:02x}{v:02x}"
            self.canvas.create_oval(x, y, x + sz, y + sz,
                                    fill=c, outline="", tags="stars")

    # ── Animation loop ────────────────────────────────────────────────────────

    def _animate(self):
        """Main render loop (~30 FPS via tkinter after())."""
        if self.running:
            self.time_days += self.speed_var.get()
            d = int(self.time_days)
            y = self.time_days / 365.25
            self.day_lbl.config(text=f"Day {d:,}  (Year {y:.2f})")

        self._draw_frame()
        self.root.after(33, self._animate)

    def _draw_frame(self):
        """Delete and redraw every dynamic canvas element."""
        self.canvas.delete("dyn")          # stars tag is kept
        self._draw_orbit_rings()
        if self.show_transfer.get() and self._transfer:
            self._draw_transfer_ellipse()
        self._draw_sun()
        self._draw_planets()

    # ── Drawing primitives ────────────────────────────────────────────────────

    def _draw_orbit_rings(self):
        for name, p in PLANETS.items():
            r   = p["display_orbit"]
            sel = (name == self.selected)
            self.canvas.create_oval(
                CX - r, CY - r, CX + r, CY + r,
                outline="#242450" if not sel else "#4a4a80",
                width=1 if not sel else 2,
                fill="", tags="dyn",
            )

    def _draw_sun(self):
        """Sun with layered glow effect."""
        r = SUN["display_radius"]
        for gr, gc in [(r * 3.2, "#130900"), (r * 2.2, "#201000"), (r * 1.5, "#301800")]:
            self.canvas.create_oval(
                CX - gr, CY - gr, CX + gr, CY + gr,
                fill=gc, outline="", tags="dyn",
            )
        self.canvas.create_oval(
            CX - r, CY - r, CX + r, CY + r,
            fill=SUN["color"], outline="#ffe066", width=1, tags="dyn",
        )
        self.canvas.create_text(
            CX, CY + r + 11, text="Sun",
            fill="#fdb813", font=FONT_SMALL, tags="dyn",
        )

    def _planet_xy(self, name, t):
        """Canvas (x, y) of planet 'name' at simulation time t (days)."""
        p     = PLANETS[name]
        angle = 2 * math.pi * t / p["orbital_period_days"]
        r     = p["display_orbit"]
        return CX + r * math.cos(angle), CY + r * math.sin(angle)

    def _draw_planets(self):
        for name, p in PLANETS.items():
            x, y = self._planet_xy(name, self.time_days)
            r    = p["display_radius"]

            # Selection highlight ring
            if name == self.selected:
                self.canvas.create_oval(
                    x - r - 5, y - r - 5, x + r + 5, y + r + 5,
                    outline=ACCENT, width=1, fill="", tags="dyn",
                )

            # Saturn's rings (drawn before planet body so body sits on top)
            if name == "Saturn":
                self.canvas.create_oval(
                    x - r * 2.5, y - r * 0.6,
                    x + r * 2.5, y + r * 0.6,
                    outline="#c8b040", width=2, fill="", tags="dyn",
                )

            # Planet body
            self.canvas.create_oval(
                x - r, y - r, x + r, y + r,
                fill=p["color"], outline="", tags="dyn",
            )

            # Name label (show for large planets or selected one)
            if r >= 7 or name == self.selected:
                self.canvas.create_text(
                    x, y + r + 10, text=name,
                    fill=p["color"], font=FONT_SMALL, tags="dyn",
                )

    def _draw_transfer_ellipse(self):
        """
        Draw the Hohmann transfer ellipse on the canvas.

        Geometry:
            Sun is at the LEFT focus of the transfer ellipse.
            Periapsis is to the RIGHT  of the Sun at distance r1.
            Apoapsis  is to the LEFT   of the Sun at distance r2.

        Ellipse bounding box on the canvas:
            x_left  = CX - r2
            x_right = CX + r1
            y_top   = CY - b      where b = √(r1 × r2)
            y_bot   = CY + b
        """
        t  = self._transfer
        r1 = t["r1_d"]
        r2 = t["r2_d"]
        b  = math.sqrt(r1 * r2)            # semi-minor axis

        self.canvas.create_oval(
            CX - r2, CY - b, CX + r1, CY + b,
            outline="#ff6600", width=2, fill="", dash=(6, 4), tags="dyn",
        )
        # Small annotation
        self.canvas.create_text(
            CX + r1 + 6, CY,
            text=f"{t['origin']} → {t['target']}",
            fill="#ff9933", font=FONT_SMALL, anchor=tk.W, tags="dyn",
        )

    # ── Event handlers ────────────────────────────────────────────────────────

    def _on_click(self, event):
        """Select nearest planet on mouse click; deselect on empty space."""
        ex, ey       = event.x, event.y
        best, bdist  = None, float("inf")
        for name in PLANETS:
            px, py = self._planet_xy(name, self.time_days)
            d      = math.hypot(ex - px, ey - py)
            if d < bdist:
                bdist, best = d, name
        if bdist < 30:
            self.selected = best
            self._show_planet_info(best)
        else:
            self.selected = None
            self._set_default_info()

    def _toggle_pause(self):
        self.running = not self.running
        self.pause_btn.config(
            text="▶  RESUME" if not self.running else "⏸  PAUSE"
        )

    # ── Info panel content ────────────────────────────────────────────────────

    def _set_default_info(self):
        parts = [
            ("Click a planet to view\ndetailed orbital data.\n\n", "dim"),
            ("PLANETS\n", "header"),
        ]
        for name, p in PLANETS.items():
            parts.append((f"  • {name:<10}", None))
            parts.append((f"  {p['orbital_radius']/1.496e11:.2f} AU\n", "dim"))
        parts.append(("\nUse the Hohmann calculator\nbelow to plan a transfer\nbetween any two planets.", "dim"))
        self._write(self.info_box, parts)

    def _show_planet_info(self, name):
        p    = PLANETS[name]
        per  = orbital_period(p["orbital_radius"])
        orb  = orbital_velocity(p["orbital_radius"])
        esc  = escape_velocity(p["mass"], p["radius"])
        grav = surface_gravity(p["mass"], p["radius"])
        au   = p["orbital_radius"] / 1.496e11

        parts = [
            (f"{'━' * 32}\n  {name.upper()}\n{'━' * 32}\n\n", "header"),

            ("PHYSICAL DATA\n",                              "header"),
            ("  Mass:      ", None),
            (f"{p['mass']:.3e} kg\n",                       "value"),
            ("  Radius:    ", None),
            (f"{p['radius']/1000:,.0f} km\n",               "value"),
            ("  Gravity:   ", None),
            (f"{grav['ms2']} m/s²  ({grav['relative']}× Earth)\n\n", "value"),

            ("ORBITAL DATA\n",                               "header"),
            ("  Distance:  ", None),
            (f"{au:.3f} AU\n",                              "value"),
            ("  Period:    ", None),
            (f"{format_period(per)}\n",                     "value"),
            ("  Orb. vel:  ", None),
            (f"{orb:.2f} km/s\n\n",                        "value"),

            ("ESCAPE VELOCITY\n",                           "header"),
            (f"  {esc:.2f} km/s\n\n",                      "value"),

            ("FUN FACT\n",                                  "header"),
            (f"  {p['fun_fact']}",                         "dim"),
        ]
        self._write(self.info_box, parts)

    # ── Hohmann calculator ────────────────────────────────────────────────────

    def _calc_hohmann(self):
        origin = self.h_from.get()
        target = self.h_to.get()

        if origin == target:
            self._write(self.h_box, [
                ("Origin and target must\nbe different planets.", "warn")
            ])
            return

        p1, p2    = PLANETS[origin], PLANETS[target]
        res       = hohmann_transfer(p1["orbital_radius"], p2["orbital_radius"])
        direction = "↑ outward" if p2["orbital_radius"] > p1["orbital_radius"] else "↓ inward"

        parts = [
            (f"{'━' * 32}\n  {origin} → {target}  {direction}\n{'━' * 32}\n\n", "header"),

            ("BURN 1  (departure)\n",       "header"),
            ("  Δv₁ = ", None),
            (f"{res['delta_v1']} km/s\n\n", "good"),

            ("BURN 2  (arrival)\n",         "header"),
            ("  Δv₂ = ", None),
            (f"{res['delta_v2']} km/s\n\n", "good"),

            ("TOTAL  Δv\n",                 "header"),
            (f"  {res['total_delta_v']} km/s\n\n", "value"),

            ("TRANSFER TIME\n",             "header"),
            (f"  {res['transfer_time_days']:.1f} days"
             f"  ({res['transfer_time_days']/365.25:.2f} yr)", "value"),
        ]
        self._write(self.h_box, parts)

        # Store for optional map overlay
        self._transfer = {
            "origin": origin,
            "target": target,
            "r1_d":   p1["display_orbit"],
            "r2_d":   p2["display_orbit"],
        }
