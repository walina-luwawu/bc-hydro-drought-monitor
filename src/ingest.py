"""
Ingestion workflows for data sources.

This module defines high-level ingestion functions 
that retrieve and organise raw data into standardized
formats.

Each function completes ingestion for a specific data source
and coordinates API requests and file I/O operations.
"""

from src.clients import download_shapefile
from src.io import unzip_file, csv_to_geodataframe, vector_to_geojson
from src.config import FACILITIES, FWA_WATERSHED_GROUPS

def ingest_facilities(
        raw_file: str='facilities.csv',
        processed_file: str='facilities.geojson'
) -> None:
    """
    Convert facilities CSV to GeoJSON.

    Parameters
    ----------
    raw_file : str
        Name of the CSV file in the configured raw directory
    processed_file : str
        Name of the GeoJSON file written to the configured processed directory
    """
    csv_path = FACILITIES.raw_dir / raw_file
    output_path = FACILITIES.processed_dir / processed_file

    csv_to_geodataframe( csv_path, output_path )

def ingest_watershed_groups(
        raw_file: str='WHSE_BASEMAPPING_FWA_WATERSHED_GROUPS_POLYPolygon.shp',
        processed_file: str='watershed_groups.geojson'
) -> None:
    """
    Download, extract, and convert watershed groups to GeoJSON.

    Parameters
    ----------
    raw_file : str
        Name of the shapefile in the configured raw directory
    processed_file : str
        Name of the GeoJSON file written to the configured processed directory
    """
    zip_path = download_shapefile( FWA_WATERSHED_GROUPS )

    unzip_file( zip_path, FWA_WATERSHED_GROUPS.raw_dir )

    vector_to_geojson(
        FWA_WATERSHED_GROUPS.raw_dir / raw_file,
        FWA_WATERSHED_GROUPS.processed_dir / processed_file
    )