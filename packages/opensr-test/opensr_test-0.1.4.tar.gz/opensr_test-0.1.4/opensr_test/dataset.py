from typing import Optional, List

import pathlib

import numpy as np
import requests
import torch


def download(url: str, save_path: str) -> str:
    """ Download a file from a url.

    Args:
        url (str): The url of the file in HuggingFace Hub.
        save_path (str): The path to save the file.

    Returns:
        str: The path to the file.
    """
    response = requests.get(url, stream=True)
    with open(save_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    return None

def load(
    dataset: str = "naip",
    model_dir: Optional[str] = None,
    force: bool = False
) -> torch.Tensor:
    """ Load a dataset.

    Args:
        dataset (str, optional): The dataset to load. Defaults to "naip".
        force (bool, optional): If True, force the download. Defaults to False.
        
    Raises:
        NotImplementedError: If the dataset is not implemented.

    Returns:
        torch.Tensor: The dataset in a tensor of shape (N, C, H, W).
    """
    if model_dir is None:
        ROOT_FOLDER = get_data_path()
    else:
        ROOT_FOLDER = pathlib.Path(model_dir)

    DATASETS = ["naip", "spot", "venus"]
    if dataset not in DATASETS:
        raise NotImplementedError("The dataset %s is not implemented." % dataset)

    URL = "https://huggingface.co/csaybar/opensr-test/resolve/main"

    # Create folder
    [(ROOT_FOLDER / x).mkdir(exist_ok=True) for x in DATASETS]

    # Download the files

    ## hr file
    hrfile_url = "%s/%s/%s" % (URL, dataset, "hr.npy")
    hrfile_path = ROOT_FOLDER / dataset / "hr.npy"
    if not hrfile_path.exists() or force:
        print(f"Downloading {dataset} dataset  - {hrfile_path.stem} file.")
        download(hrfile_url, hrfile_path)

    ## lr file
    lrfile_url = "%s/%s/lr.npy" % (URL, dataset)
    lrfile_path = ROOT_FOLDER / dataset / "lr.npy"
    if not lrfile_path.exists() or force:
        print(f"Downloading {dataset} dataset  - {lrfile_path.stem} file.")
        download(lrfile_url, lrfile_path)

    ## landuse file
    landuse_url = "%s/%s/landuse2.npy" % (URL, dataset)
    landuse_path = ROOT_FOLDER / dataset / "landuse2.npy"
    if not landuse_path.exists() or force:
        print(f"Downloading {dataset} dataset  - {landuse_path.stem} file.")
        download(landuse_url, landuse_path)

    ## metadata file
    csvfile_url = "%s/%s/metadata.csv" % (URL, dataset)
    csvfile_path = ROOT_FOLDER / dataset / "metadata.csv"
    if not csvfile_path.exists() or force:
        print(f"Downloading {dataset} dataset  - {csvfile_path.stem} file.")
        download(csvfile_url, csvfile_path)

    # Load the dataset

    ## LR file
    lr_data = np.load(ROOT_FOLDER / dataset / "lr.npy") / 10000
    lr_data_torch = lr_data.astype(np.float32)

    ## HR file
    hr_data = np.load(ROOT_FOLDER / dataset / "hr.npy") / 10000
    hr_data_torch = hr_data.astype(np.float32)

    return {
        "lr": lr_data_torch,
        "hr": hr_data_torch,
        "params": create_param_config(dataset)
    }


def get_data_path() -> str:
    cred_path = pathlib.Path.home() / ".config/opensr_test/"
    cred_path.mkdir(parents=True, exist_ok=True)
    return cred_path


def create_param_config(dataset = "naip") -> List:
    if dataset == "naip":
        gradient_threshold = [
                0.02, 0.016, 0.025, 0.015, 0.023, 0.019,
                0.021, 0.019, 0.012, 0.027, 0.016, 0.02,
                0.018, 0.02, 0.018, 0.019, 0.019, 0.019,
                0.013, 0.013, 0.013, 0.015, 0.015, 0.015,
                0.018, 0.017, 0.016, 0.015, 0.022, 0.016
        ]
    elif dataset == "spot":
        gradient_threshold = [
                0.014, 0.016, 0.013, 0.010, 0.032,
                0.040, 0.014, 0.037, 0.030, 0.036,
                0.026, 0.030
        ]

    elif dataset == "venus":
        gradient_threshold = [
            0.015, 0.012, 0.012, 0.012, 0.013, 0.011,
            0.01, 0.012, 0.011, 0.013, 0.01, 0.013,
            0.013, 0.01, 0.017, 0.01, 0.012, 0.013,
            0.011, 0.013, 0.017, 0.011, 0.01, 0.011,
            0.012, 0.015, 0.012, 0.011, 0.01, 0.017,
            0.016, 0.01, 0.011, 0.014, 0.012, 0.016,
            0.01, 0.012, 0.013, 0.01, 0.016, 0.016, 
            0.012, 0.011, 0.016, 0.01, 0.015, 0.016, 
            0.016, 0.01, 0.015, 0.011, 0.016, 0.016, 
            0.013, 0.013, 0.014, 0.01, 0.011
        ]
    return gradient_threshold