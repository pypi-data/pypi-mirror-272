"""Generic utility functions."""

from pathlib import Path
from tqdm.auto import tqdm
import pandas as pd
import requests
import tarfile
import logging
logger = logging.getLogger(__name__)


def list_datasets() -> pd.DataFrame:
    """List available datasets.

    Returns:
        DataFrame: List of available datasets including name, description, and url.

    """
    # use requests to get the list of datasets and parse it using yaml
    import requests
    import yaml
    url = 'https://edu.lu/g3988'  # short url for the list of URLs
    response = requests.get(url)
    if response.status_code == 200:
        datasets = pd.DataFrame(yaml.safe_load(response.text))
        return datasets
    else:
        logger.error(f'Failed to get the list of datasets from {url}.')
        raise Exception(f'Failed to get the list of datasets from {url}.')


def extract_dataset(name: str, **kwargs) -> Path:
    """Extract a dataset and return the path to the extracted directory.

    Args:
        name: Name of the datasets, e.g., `P500` for a compressed file of the name
              `P500.tar.gz`.
        kwargs (dict): Additional arguments, including `dest` which is the
                       destination directory to extract the file. Defaults to (i.e.,
                       `~/.behaverse/datasets/{name}/`).

    Returns:
        Path: Path to the extracted directory.

    """
    src = Path.home() / '.behaverse' / 'datasets' / f'{name}.tar.gz'
    if not src.exists():
        raise FileNotFoundError(f'{src} not found.')

    dest = Path(kwargs.get('dest', Path.home() / '.behaverse' / 'datasets'))

    if not dest.exists():
        dest.mkdir(parents=True, exist_ok=True)
        logger.info(f'Destination directory created: {dest.parent}')

    # TODO support both .tar.* and .tar formats
    ext = src.suffixes[-1].replace('.', '')
    tar = tarfile.open(src, f'r:{ext}')
    # Python 3.12+ gives a deprecation warning if TarFile.extraction_filter is None.
    if hasattr(tarfile, 'fully_trusted_filter'):
        tar.extraction_filter = staticmethod(tarfile.fully_trusted_filter)  # type: ignore

    tar.extractall(dest)
    output_folder = dest / tar.getnames()[0]
    tar.close()
    logger.info(f'Extracted to {output_folder}')

    return output_folder


def download_dataset(name: str, **kwargs) -> Path:
    """Download dataset from the given URL.

    Args:
        name: the name of the dataset to download.
        kwargs (dict): additional arguments. For example you can specify the destination
                        path (`dest`) to save the dataset file. Defaults to
                        `~/.behaverse/datasets/{name}/`. Or `chunk_size` to specify the chunk size for downloading.
    """
    assert name is not None, 'Dataset name is required.'

    datasets: pd.DataFrame = list_datasets()
    # query datasets for the url of a row with the given name
    url = datasets[datasets['name'] == name]['url'].values[0]

    dest = Path(kwargs.get('dest',
                           Path.home() / '.behaverse' / 'datasets' / f'{name}.tar.gz'))
    chunk_size = kwargs.get('chunk_size', 8096)

    if dest.exists():
        return extract_dataset(name)

    dest.parent.mkdir(parents=True, exist_ok=True)

    with requests.get(url, stream=True) as r:
        r.raise_for_status()

        with open(dest, 'wb') as f:
            for chunk in tqdm(r.iter_content(chunk_size=chunk_size),
                              leave=False,
                              unit='B'):
                f.write(chunk)

    logger.info(f'Downloaded dataset to {dest}, now extracting...')

    output_path = extract_dataset(name)
    logger.info(f'Extracted dataset to {output_path}')
    return output_path
