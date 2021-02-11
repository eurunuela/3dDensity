# 3dDensity

[![CircleCI](https://circleci.com/gh/eurunuela/3dDensity.svg?style=shield)](https://circleci.com/gh/eurunuela/3dDensity)
[![codecov](https://codecov.io/gh/eurunuela/3dDensity/branch/main/graph/badge.svg?token=o4QhYt5i9u)](https://codecov.io/gh/eurunuela/3dDensity)

Density Volumes for concatenated statistical maps of multi-subject, multi-run or surrogate fMRI datasets.

## How to install

First, clone the repository:

```
git clone https://github.com/eurunuela/denvol.git
```

Then, move into the cloned repository:

```
cd denvol
```

Once inside the directory, install the package:

```
pip install denvol
```

Finally, make sure the installation was successful by checking the version.

```
❯ denvol -v
denvol 0+untagged.17.gfef5cc4.dirty
```

To learn how to use it, make use of the help option:

```
❯ denvol -h
usage: denvol [-h] -i INPUT_FILE [-m INPUT_MASK] [-n N_BINS] [-o OUT_NAME] [-outdir OUT_DIR]
              [-indir IN_DIR] [-history] [-debug] [-quiet] [-v]

Required Argument::
  -i INPUT_FILE, --input INPUT_FILE
                        The name of the file to calculate densities on.

optional arguments:
  -h, --help            show this help message and exit
  -m INPUT_MASK, --mask INPUT_MASK
                        The filename of the mask to apply on <input>. Default is None (nilearn
                        automatically creates the mask).
  -n N_BINS, --nbins N_BINS
                        Only output info about the file, don't process. Default is to process.
  -o OUT_NAME, --outname OUT_NAME
                        Name for the output file.Default is current density_volume.nii
  -outdir OUT_DIR, --outdir OUT_DIR
                        Output directory containing density volumes. Default is current directory.
  -indir IN_DIR, --indir IN_DIR
                        Input directory containing <input>. Default is current directory.
  -history, --history   Update the file history to contain the denvol command.
  -debug, --debug       Only print debugging info to log file. Default is False.
  -quiet, --quiet       Only print warnings to log file. Default is False.
  -v, --version         show program's version number and exit
```

## Requirements

- matplotlib
- nilearn
- numpy
- tqdm
