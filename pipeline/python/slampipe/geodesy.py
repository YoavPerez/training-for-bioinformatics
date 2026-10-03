"""Module 1: WGS84 -> ECEF -> local ENU conversions.

All angles are in degrees at the API boundary, heights in metres above the ellipsoid.
"""

# WGS84 ellipsoid constants.
WGS84_A = 6378137.0
WGS84_F = 1.0 / 298.257223563
WGS84_E2 = WGS84_F * (2.0 - WGS84_F)


def wgs84_to_ecef(lat_deg, lon_deg, h):
    """Geodetic coordinates -> ECEF [m]. Accepts scalars or arrays; returns shape (..., 3)."""
    # TODO(m1): implement.
    raise NotImplementedError("wgs84_to_ecef")


def ecef_to_enu(p_ecef, ref_lat_deg, ref_lon_deg, ref_h):
    """ECEF points (..., 3) -> local ENU (..., 3) with origin at the reference geodetic point."""
    # TODO(m1): implement.
    raise NotImplementedError("ecef_to_enu")


def wgs84_to_enu(lat_deg, lon_deg, h, ref_lat_deg, ref_lon_deg, ref_h):
    """Geodetic -> local ENU. Provided: composes the two functions above."""
    return ecef_to_enu(wgs84_to_ecef(lat_deg, lon_deg, h), ref_lat_deg, ref_lon_deg, ref_h)
