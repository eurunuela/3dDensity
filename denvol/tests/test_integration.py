from os.path import join, split

from denvol.denvol import denvol


def test_denvol(nilearn_data):

    # Obtain test path
    test_path, _ = split(nilearn_data.func[0])

    # Create output path
    out_path = join(test_path, "out")

    denvol(input_file=nilearn_data.func[0])

    breakpoint()
