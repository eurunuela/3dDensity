# -*- coding: utf-8 -*-
"""Parser for denvol."""


import argparse

from denvol import __version__


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
                          help='Update the file history to contain the denvol command.',
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
    raise RuntimeError('denvol/cli/run.py should not be run directly;\n'
                       'Please `pip install` denvol and use the '
                       '`denvol` command')
