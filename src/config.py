"""
Configurations for data sources.

This module defines immutable configuration objects that describe
where data is stored and how it is accessed.

These configurations are used by the API client and ingestion
modules to separate metadata from executable code.
"""

from dataclasses import dataclass
from pathlib import Path

# Absolute path to the project root directory
# Assumes this module is under src/
PROJECT_ROOT = Path( __file__ ).resolve().parents[1]

# Root directory for all raw and processed data
DATA_DIR = PROJECT_ROOT / 'data'

# ---------------------
# Configuration classes
# ---------------------

@dataclass( frozen=True )
class BaseSourceConfig:
    """
    Base configuration for a data source.

    This class defines filesystem locations common to all data sources.

    Attributes
    ----------
    name : str
        Unique identifier for the data source.
    raw_dir : Path
        Directory where raw data are stored.
    processed_dir : Path
        Directory where processed data are written.
    """
    name: str
    raw_dir: Path
    processed_dir: Path

@dataclass( frozen=True )
class WFSSourceConfig( BaseSourceConfig ):
    """
    Configuration for a Web Feature Service (WFS) data source.

    Extends BaseSourceConfig with the information required to retrieve
    vector data from a WFS endpoint using a GetFeature request.

    Attributes
    ----------
    base_url : str
        Base URL of the WFS service endpoint.
    type_name : str
        Fully qualified WFS feature type name.
    output_name : str
        Name of the output file.
    version : str
        WFS protocol version to use (default is '2.0.0').
    """
    base_url: str
    type_name: str
    output_name: str
    version: str = '2.0.0'

# ---------------------
# Configuration objects
# ---------------------

FACILITIES = BaseSourceConfig(
    name='facilities',
    raw_dir=DATA_DIR / 'raw',
    processed_dir=DATA_DIR / 'spacial'
)

FWA_WATERSHED_GROUPS = WFSSourceConfig(
    name='fwa_watershed_groups',
    raw_dir=DATA_DIR / 'raw/watershed_groups',
    processed_dir=DATA_DIR / 'spacial',
    base_url='https://openmaps.gov.bc.ca/geo/pub/ows?',
    type_name='WHSE_BASEMAPPING.FWA_WATERSHED_GROUPS_POLY',
    output_name='watershed_groups.zip'
)