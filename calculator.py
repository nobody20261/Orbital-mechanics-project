"""
calculator.py — Orbital Mechanics Calculations
All formulas based on Newtonian gravity and Kepler's Laws.

Key equations
─────────────
  Orbital Period     T     = 2π √(a³ / GM)          [Kepler's 3rd Law]
  Orbital Velocity   v     = √(GM / r)               [Circular orbit]
  Escape Velocity    v_esc = √(2GM / r)              [Surface escape]
  Surface Gravity    g     = GM / r²
  Hohmann Δv₁        Δv₁   = v_transfer_peri - v_circ_1   [Departure burn]
  Hohmann Δv₂        Δv₂   = v_circ_2 - v_transfer_apo    [Arrival burn]
"""

import math

# ── Physical constants ────────────────────────────────────────────────────────
G       = 6.674e-11    # Gravitational constant  (m³ kg⁻¹ s⁻²)
M_SUN   = 1.989e30     # Mass of the Sun          (kg)
G_EARTH = 9.807        # Earth surface gravity    (m/s²)
AU      = 1.496e11     # Astronomical unit        (m)


# ── Core functions ────────────────────────────────────────────────────────────

def orbital_period(semi_major_axis, central_mass=M_SUN):
    """
    Kepler's Third Law:  T = 2π √(a³ / GM)

    Args:
        semi_major_axis (float): Semi-major axis in metres
        central_mass    (float): Mass of central body in kg  (default: Sun)

    Returns:
        float: Orbital period in days
    """
    T_sec = 2 * math.pi * math.sqrt(semi_major_axis**3 / (G * central_mass))
    return T_sec / 86400


def orbital_velocity(radius, central_mass=M_SUN):
    """
    Circular orbital velocity:  v = √(GM / r)

    Args:
        radius       (float): Orbital radius in metres
        central_mass (float): Mass of central body in kg

    Returns:
        float: Velocity in km/s
    """
    return math.sqrt(G * central_mass / radius) / 1000


def escape_velocity(mass, radius):
    """
    Escape velocity:  v_esc = √(2GM / r)

    Args:
        mass   (float): Mass of body in kg
        radius (float): Radius of body in metres

    Returns:
        float: Escape velocity in km/s
    """
    return math.sqrt(2 * G * mass / radius) / 1000


def surface_gravity(mass, radius):
    """
    Surface gravity:  g = GM / r²

    Args:
        mass   (float): Mass of body in kg
        radius (float): Radius of body in metres

    Returns:
        dict: { 'ms2': float, 'relative': float }
              ms2      — acceleration in m/s²
              relative — multiple of Earth gravity
    """
    g = G * mass / radius**2
    return {
        "ms2":      round(g, 2),
        "relative": round(g / G_EARTH, 2),
    }


def hohmann_transfer(r1, r2, central_mass=M_SUN):
    """
    Hohmann transfer orbit — the most fuel-efficient two-burn maneuver
    between two coplanar circular orbits.

    Geometry:
        The transfer ellipse has its periapsis at r1 and apoapsis at r2.
        Semi-major axis:  a = (r1 + r2) / 2
        The Sun sits at one focus of the transfer ellipse.

    Burns:
        Δv₁ (departure) — speed up / slow down to enter transfer ellipse
        Δv₂ (arrival)   — circularise into target orbit

    Args:
        r1           (float): Initial orbital radius in metres
        r2           (float): Target  orbital radius in metres
        central_mass (float): Mass of central body in kg

    Returns:
        dict:
            delta_v1           — Δv of first  burn  (km/s)
            delta_v2           — Δv of second burn  (km/s)
            total_delta_v      — Δv₁ + Δv₂          (km/s)
            transfer_time_days — flight time         (days)
    """
    a = (r1 + r2) / 2                                      # semi-major axis

    v1_circ = math.sqrt(G * central_mass / r1)             # circular speed at r1
    v2_circ = math.sqrt(G * central_mass / r2)             # circular speed at r2

    v_peri  = math.sqrt(G * central_mass * (2/r1 - 1/a))  # transfer speed at periapsis
    v_apo   = math.sqrt(G * central_mass * (2/r2 - 1/a))  # transfer speed at apoapsis

    dv1 = abs(v_peri  - v1_circ)
    dv2 = abs(v2_circ - v_apo)

    t_transfer = math.pi * math.sqrt(a**3 / (G * central_mass))  # half-period of ellipse

    return {
        "delta_v1":          round(dv1 / 1000, 3),
        "delta_v2":          round(dv2 / 1000, 3),
        "total_delta_v":     round((dv1 + dv2) / 1000, 3),
        "transfer_time_days": round(t_transfer / 86400, 1),
    }


# ── Formatting helper ─────────────────────────────────────────────────────────

def format_period(days):
    """Return a human-readable orbital period string."""
    if days < 1:
        return f"{days * 24:.1f} hours"
    if days < 365.25:
        return f"{days:.1f} days"
    return f"{days / 365.25:.2f} years"
