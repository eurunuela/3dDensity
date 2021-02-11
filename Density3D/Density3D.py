"""Main workflow of Density3D."""
import datetime
import getpass
import logging
import matplotlib.pyplot as plt
import numpy as np
import os
import socket
import sys

from nilearn import masking
from tqdm import tqdm

from Density3D import _version
from Density3D.cli.run import _get_parser

LGR = logging.getLogger(__name__)


def Density3D(input_file, input_mask=None, n_bins=50, hist_range=[-0.01, 0.01],
              out_name='density_volume', in_dir=',', out_dir='.', history=False,
              debug=False, quiet=False):
    """Run main workflow of Density3D.

    Parameters
    ----------
    input_file : [type]
        [description]
    input_mask : [type], optional
        [description], by default None
    n_bins : int, optional
        [description], by default 50
    out_name : str, optional
        [description], by default 'density_volume'
    in_dir : str, optional
        [description], by default ','
    out_dir : str, optional
        [description], by default '.'
    history : bool, optional
        [description], by default False
    debug : bool, optional
        [description], by default False
    quiet : bool, optional
        [description], by default False
    """
    # Save call for file history
    arg_str = ' '.join(sys.argv[1:])
    history_str = '[{username}@{hostname}: {date}] Density3D {arguments}'.format(
        username=getpass.getuser(),
        hostname=socket.gethostname(),
        date=datetime.datetime.now().strftime("%c"),
        arguments=arg_str,
    )

    # Create output directory if it does not exist
    out_dir = os.path.abspath(out_dir)
    os.makedirs(out_dir, exist_ok=True)
    out_name = os.path.join(out_dir, out_name)

    # Create logfile name
    basename = 'Density3D_'
    extension = 'tsv'
    isotime = datetime.datetime.now().strftime('%Y-%m-%dT%H%M%S')
    logname = os.path.join(out_dir, (basename + isotime + '.' + extension))

    # Set logging format
    log_formatter = logging.Formatter(
        '%(asctime)s\t%(name)-12s\t%(levelname)-8s\t%(message)s',
        datefmt='%Y-%m-%dT%H:%M:%S')

    # Set up logging file and open it for writing
    log_handler = logging.FileHandler(logname)
    log_handler.setFormatter(log_formatter)
    sh = logging.StreamHandler()

    if quiet:
        logging.basicConfig(level=logging.WARNING,
                            handlers=[log_handler, sh], format='%(levelname)-10s %(message)s')
    elif debug:
        logging.basicConfig(level=logging.DEBUG,
                            handlers=[log_handler, sh], format='%(levelname)-10s %(message)s')
    else:
        logging.basicConfig(level=logging.INFO,
                            handlers=[log_handler, sh], format='%(levelname)-10s %(message)s')

    version_number = _version.get_versions()['version']
    LGR.info(f'Currently running phys2bids version {version_number}.')
    LGR.info(f'Input file is {input_file}.')

    # Save absolute path to input files
    in_dir = os.path.abspath(in_dir)

    if type(input_file) is str:
        input_file = os.path.join(in_dir, input_file)

    # Compute mask if it does not exist
    if input_mask is None:
        input_mask = masking.compute_epi_mask(input_file)
    else:
        input_mask = os.path.join(in_dir, input_mask)

    # Read data
    data_masked = masking.apply_mask(input_file, input_mask)
    nvoxels = data_masked.shape[1]
    LGR.info(f'{nvoxels} voxels found in the volume.')

    # Calculate density for each voxel
    LGR.info('Calculating density...')
    kde = np.zeros((n_bins, data_masked.shape[1]))
    for voxidx in tqdm(range(nvoxels)):
        # Calculate overall density
        hist = plt.hist(np.squeeze(data_masked[:, voxidx]), bins=n_bins)
        density, values, _ = hist

        # Find values above and below range, and sum
        below = np.where(values <= hist_range[0])[0]
        if below.size != 0:
            below_idx = np.max(below)
            below_quantity = np.sum(density[:below_idx])
        else:
            below_quantity = 0

        above = np.where(values >= hist_range[1])[0]
        if above.size != 0:
            above_idx = np.min(above)
            above_quantity = np.sum(density[above_idx:])
        else:
            above_quantity = 0

        # Calculate density inside range
        hist = plt.hist(np.squeeze(data_masked[:, voxidx]), bins=n_bins)
        density, values, _ = hist

        # Add values outside of range
        density[0] = density[0] + below_quantity
        density[-1] = density[-1] + above_quantity

        # Save density of voxel
        kde[:, voxidx] = np.squeeze(density)
        plt.clf()

    LGR.info('Density calculation finished.')

    # Export data
    LGR.info('Exporting results...')
    output_data = masking.unmask(kde, input_mask)
    output_data.to_filename(out_name)
    LGR.info(f'Results exported to {out_name}')

    if history:
        import subprocess
        LGR.info('Updating file history...')
        subprocess.run('3dNotes -h "' + history_str + '" ' + out_name, shell=True)
        LGR.info('File history updated.')

    LGR.info('Density3D finished.')


def _main(argv=None):
    options = _get_parser().parse_args(argv)
    Density3D(**vars(options))


if __name__ == '__main__':
    _main(sys.argv[1:])
