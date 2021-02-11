from os.path import join, split
import nibabel as nib
from nilearn.image import new_img_like
import os
from Density3D.Density3D import Density3D


def test_integration(nilearn_data):

    # Obtain test path
    test_path, _ = split(nilearn_data.func[0])
    out_path = test_path

    data = new_img_like(nilearn_data.func[0], nib.load(nilearn_data.func[0]).get_fdata()[:20, :20, :20, :20])

    Density3D(input_file=data, in_dir=test_path, out_dir=out_path, n_bins=10, hist_range=[-0.05, 0.05])

    assert os.path.isfile(join(out_path, 'density_volume.nii'))
