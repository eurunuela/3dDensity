# -*- coding: utf-8 -*-
"""Parser for Density3D."""


import argparse

import numpy as np

from Density3D import __version__


def two_floats(value):
    """Convert string into float.

    Parameters
    ----------
    value : str
        String containing two floats.

    Returns
    -------
    Numpy array
        Numpy array containign two floats.

    Raises
    ------
    argparse.ArgumentError
        Raised when more than 2 floats are given.
    """
    values = value.split()
    if len(values) != 2:
        raise argparse.ArgumentError
    values = map(float, values)
    values = np.fromiter(values, dtype=np.float)
    return values


def _get_parser():
    """
    Parse command line inputs for this function.

    Returns
    -------
    parser.parse_args() : argparse dict

    Notes
    -----
    # Argument parser follow template provided by RalphyZ.
    # https://stackoverflow.com/a/43456577
    """
    parser = argparse.ArgumentParser()
    optional = parser._action_groups.pop()
    required = parser.add_argument_group('Required Argument:')
    required.add_argument('-i', '--input',
                          dest='input_file',
                          type=str,
                          help='The name of the file to calculate densities on.',
                          required=True)
    optional.add_argument('-m', '--mask',
                          dest='input_mask',
                          type=str,
                          help='The filename of the mask to apply on <input>. '
                               'Default is None (nilearn automatically creates the mask).',
                          default=None)
    optional.add_argument('-n', '--nbins',
                          dest='n_bins',
                          type=int,
                          help='Only output info about the file, don\'t process. '
                               'Default is to process.',
                          default=50)
    optional.add_argument('-r', '--range',
                          dest='hist_range',
                          type=two_floats,
                          help='Range to limit the densities. '
                               'Default is "-0.01 0.01".',
                          default=[-0.01, 0.01])
    optional.add_argument('-o', '--outname',
                          dest='out_name',
                          type=str,
                          help='Name for the output file.'
                               'Default is current density_volume.nii',
                          default='density_volume')
    optional.add_argument('-outdir', '--outdir',
                          dest='out_dir',
                          type=str,
                          help='Output directory containing density volumes. '
                               'Default is current directory.',
                          default='.')
    optional.add_argument('-indir', '--indir',
                          dest='in_dir',
                          type=str,
                          help='Input directory containing <input>. Default is current '
                               'directory.',
                          default='.')
    optional.add_argument('-history', '--history',
                          dest='history',
                          action='store_true',
                          help='Update the file history to contain the Density3D command.',
                          default=False)
    optional.add_argument('-debug', '--debug',
                          dest='debug',
                          action='store_true',
                          help='Only print debugging info to log file. Default is False.',
                          default=False)
    optional.add_argument('-quiet', '--quiet',
                          dest='quiet',
                          action='store_true',
                          help='Only print warnings to log file. Default is False.',
                          default=False)
    optional.add_argument('-v', '--version', action='version',
                          version=('%(prog)s ' + __version__))

    parser._action_groups.append(optional)

    return parser


if __name__ == '__main__':
    raise RuntimeError('Density3D/cli/run.py should not be run directly;\n'
                       'Please `pip install` Density3D and use the '
                       '`Density3D` command')
