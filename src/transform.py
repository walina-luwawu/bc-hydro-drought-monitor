"""
Data transformation utilities.

This module defines functions that derive relationships
between geospatial datasets.
"""

import geopandas

def link_facilities_to_watershed_groups(
        facilities: geopandas.GeoDataFrame,
        watershed_groups: geopandas.GeoDataFrame,
) -> geopandas.GeoDataFrame:
    """
    Spatially link facilities to watershed groups.

    Performs a spatial join that assigns each facility to the watershed
    group polygon that contains it.

    Parameters
    ----------
    facilities : geopandas.GeoDataFrame
        Point geometries representing facilities.
    watershed_groups : geopandas.GeoDataFrame
        Polygon geometries representing watershed groups.

    Returns
    -------
    geopandas.GeoDataFrame
        Facilities enriched with watershed group attributes.
        Facilities that are not inside a watershed polygon will
        have null watershed attributes.
    """
    if facilities.crs != watershed_groups.crs:
        watershed_groups = watershed_groups.to_crs( facilities.crs )

    return geopandas.sjoin(
        facilities,
        watershed_groups,
        how='left',
        predicate='within'
    )