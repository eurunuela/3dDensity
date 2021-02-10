from os.path import join, split
import requests
import tarfile
import os
from io import BytesIO
from gzip import GzipFile
from denvol.denvol import denvol


def download_test_data(osf, outpath):
    """
    Downloads tar.gz data stored at `osf` and unpacks into `outpath`

    Parameters
    ----------
    osf : str
        URL to OSF file that contains data to be downloaded
    outpath : str
        Path to directory where OSF data should be extracted
    """

    req = requests.get(osf)
    req.raise_for_status()
    t = tarfile.open(fileobj=GzipFile(fileobj=BytesIO(req.content)))
    os.makedirs(outpath, exist_ok=True)
    t.extractall(outpath)


def test_integration(nilearn_data):

    # Obtain test path
    test_path, _ = split(nilearn_data.func[0])

    # Create output path
    out_path = join(test_path, "out")

    download_test_data('https://osf.io/9c42e/download',
                       os.path.dirname(out_path))

    breakpoint()

    denvol(input_file='p06.SBJ01_S09_Task11_e1.sm.nii.gz', in_dir=test_path, out_dir=out_path, n_bins=10)

    assert os.path.isfile(join(out_path, 'density_volume.nii'))
