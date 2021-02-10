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

from denvol import _version
from denvol.cli.run import _get_parser

from . import __version__

LGR = logging.getLogger(__name__)

def denvol(input_file, input_mask, n_bins='50', out_name='density_volume', in_dir=',',
           out_dir='.', history=False, debug=False, quiet=False):

    # Save call for file history
    arg_str = ' '.join(sys.argv[1:])
    history_str = '[{username}@{hostname}: {date}] denvol {arguments}'.format(
        username=getpass.getuser(),
        hostname=socket.gethostname(),
        date=datetime.datetime.now().strftime("%c"),
        arguments=arg_str,
    )

    # Create output directory if it does not exist
    out_dir = os.path.abspath(out_dir)
    os.makedirs(out_dir, exist_ok=True)
    out_name = os.path.join(out_dir, out_name)

    # Save absolute path to input files
    in_dir = os.path.abspath(in_dir)
    input_file = os.path.join(in_dir, input_file)
    input_mask = os.path.join(in_dir, input_mask)

    # Create logfile name
    basename = 'denvol_'
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

    # Read data
    data_masked = masking.apply_mask(input_file, input_mask)
    nvoxels = data_masked.shape[1]
    LGR.info(f'{nvoxels} found in the volume.')

    # Calculate density for each voxel
    LGR.info('Starting density calculation...')
    kde = np.zeros((n_bins, data_masked.shape[1]))
    for voxidx in tqdm(range(nvoxels)):
        hist = plt.hist(np.squeeze(data_masked[:, voxidx]), bins=n_bins)
        density, _, _ = hist
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

    LGR.info('denvol finished.')


def _main(argv=None):
    options = _get_parser().parse_args(argv)
    denvol(**vars(options))


if __name__ == '__main__':
    _main(sys.argv[1:])