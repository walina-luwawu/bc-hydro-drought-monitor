"""
WFS client utilities.

This module defines network-layer functions for retrieving geospatial
data from Web Feature Service (WFS) endpoints. These functions send requests,
handle HTTP responses, and write raw files to disk.
"""

from pathlib import Path
import requests
from ..config import WFSSourceConfig

def download_shapefile(
        cfg: WFSSourceConfig,
        timeout: int = 30
) -> Path:
    """
    Download a shapefile from a WFS endpoint.

    Sends a WFS GetFeature request using the provided configuration
    and streams the response to disk as a shapefile ZIP archive.

    Parameters
    ----------
    cfg : WFSSourceConfig
        Configuration describing the WFS endpoint and output location.
    timeout : int
        Maximum number of seconds to wait for a server response
        (default is 30).

    Returns
    -------
    Path
        Filesystem path to the downloaded shapefile ZIP archive.

    Notes
    -----
    - The response is streamed in chunks to ensure constant memory usage.
    - The raw directory is created if it does not already exist.
    - HTTP errors are raised via `response.raise_for_status()`.
    """
    params = {
        'service': 'WFS',
        'version': cfg.version,
        'request': 'GetFeature',
        'typeName': cfg.type_name,
        'outputFormat': 'SHAPE-ZIP'
    }

    output_path = cfg.raw_dir / cfg.output_name
    output_path.parent.mkdir( parents=True, exist_ok=True )

    with requests.get( cfg.base_url, params=params, stream=True, timeout=timeout ) as response:
        response.raise_for_status()

        with open( output_path, 'wb' ) as file:
            for chunk in response.iter_content( chunk_size=8192 ):
                if chunk:
                    file.write( chunk )
    
    return output_path