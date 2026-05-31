import os
import httpx

# SMAP L4 Global 9 km soil moisture — NASA Earthdata OPeNDAP REST endpoint.
# Docs: https://disc.gsfc.nasa.gov/datasets/SPL4SMGP_007
# Returns volumetric soil moisture (m³/m³). Multiply by 100 → percentage.
_SMAP_URL = (
    "https://n5eil01u.ecs.nsidc.org/SMAP/SPL4SMGP.007/2024.01.01/"
    "SMAP_L4_SM_gph_20240101T013000_Vv7030_001.h5.nc4"
)

# Province/state → approximate (lat, lon) centroid used for the SMAP query.
_REGION_CENTROIDS: dict[str, tuple[float, float]] = {
    "ontario":         (51.25, -85.32),
    "quebec":          (53.00, -70.67),
    "british columbia":(53.73, -127.65),
    "alberta":         (55.00, -115.00),
    "andhra pradesh":  (15.91, 79.74),
    "punjab":          (31.15, 75.34),
    "maharashtra":     (19.75, 75.71),
    "california":      (36.78, -119.42),
    "iowa":            (42.03, -93.58),
    "texas":           (31.97, -99.90),
}


class NASASMAPAdapter:
    """
    Fetches surface soil moisture from the NASA SMAP L4 satellite product.
    Requires NASA_EARTHDATA_TOKEN environment variable.

    The token is read inside the method (not at import time) so the adapter
    can be imported safely even if the env var is not set in test environments.
    """

    def get_soil_moisture(self, province_state: str) -> float:
        token = os.environ["NASA_EARTHDATA_TOKEN"]
        key = province_state.lower().strip()
        if key not in _REGION_CENTROIDS:
            raise ValueError(f"No SMAP centroid configured for region: {province_state!r}")
        lat, lon = _REGION_CENTROIDS[key]

        response = httpx.get(
            "https://appeears.earthdatacloud.nasa.gov/api/point",
            params={
                "product": "SPL4SMGP.007",
                "layer":   "sm_surface",
                "latitude":  lat,
                "longitude": lon,
            },
            headers={"Authorization": f"Bearer {token}"},
            timeout=10.0,
        )
        response.raise_for_status()
        data = response.json()

        # AppEEARS returns a list of point results; take the latest value.
        value_m3 = float(data["value"])  # m³/m³ volumetric water content
        pct = round(value_m3 * 100, 2)

        if not (0.0 <= pct <= 100.0):
            raise ValueError(f"SMAP returned out-of-range moisture: {pct}")

        return pct
