"""
Filesystem-based geospatial I/O utilities.

This module defines functions for reading and writing
geospatial and tabular data to and from disk. Functions here
perform format conversion and CRS conversion.
"""

from pathlib import Path
import zipfile
import pandas
import geopandas
from shapely.geometry import Point

def unzip_file(
        zip_path: Path,
        output_dir: Path,
        overwrite: bool = True
) -> list[Path]:
    """
    Extract a ZIP archive to a directory.

    Parameters
    ----------
    zip_path : Path
        Path to the ZIP archive.
    output_dir : Path
        Directory where files will be extracted.
    overwrite : bool
        Whether existing files may be overwritten
        (default is True).

    Returns
    -------
    list[Path]
        Paths of extracted files.
    """
    output_dir.mkdir( parents=True, exist_ok=True )

    extracted = []

    with zipfile.ZipFile( zip_path, "r" ) as zipped:
        for entry in zipped.namelist():
            target = output_dir / entry

            if target.exists() and not overwrite:
                continue

            zipped.extract(entry, output_dir)
            extracted.append(target)

    return extracted

def csv_to_geodataframe(
        csv_path: Path,
        x_col: str,
        y_col: str,
        crs: str = 'EPSG:4326'
) -> geopandas.GeoDataFrame:
    """
    Load a CSV file with coordinate columns into a GeoDataFrame.

    Parameters
    ----------
    csv_path : Path
        Path to the CSV file.
    x_col : str
        Column name for longitude or X coordinate.
    y_col : str
        Column name for latitude or Y coordinate.
    crs : str
        CRS of the input coordinates (default is EPSG:4326).

    Returns
    -------
    geopandas.GeoDataFrame
        GeoDataFrame with point geometries.
    """
    df = pandas.read_csv( csv_path )

    geometry = [
        Point( xy ) for xy in zip( df[x_col], df[y_col] )
    ]

    gdf = geopandas.GeoDataFrame(
        df,
        geometry=geometry,
        crs=crs
    )

    return gdf

def vector_to_geodataframe(
        path: Path,
        target_crs: str | None = 'EPSG:4326'
) -> geopandas.GeoDataFrame:
    """
    Load a vector file into a GeoDataFrame.

    Parameters
    ----------
    path : Path
        Path to the vector file (e.g. Shapefile, GeoJSON).
    target_crs : str or None
        CRS to project to. If None, CRS is left unchanged.

    Returns
    -------
    geopandas.GeoDataFrame
        Loaded (and possibly reprojected) data.
    """

    gdf = geopandas.read_file( path )

    if target_crs and gdf.crs and target_crs != gdf.crs.to_string() != target_crs:
        gdf = gdf.to_crs( target_crs )
    
    return gdf

def write_geojson(
        gdf: geopandas.GeoDataFrame,
        output_path: Path
) -> None:
    """
    Write a GeoDataFrame to GeoJSON.

    Parameters
    ----------
    gdf : geopandas.GeoDataFrame
        Data to write.
    output_path : Path
        Destination file path.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)
    gdf.to_file(output_path, driver="GeoJSON")