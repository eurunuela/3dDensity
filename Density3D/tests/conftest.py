import os.path as op

import pytest
from nilearn.datasets import fetch_development_fmri


@pytest.fixture(scope="session")
def testpath(tmp_path_factory):
    """ Test path that will be used to download all files """
    return tmp_path_factory.getbasetemp()


@pytest.fixture
def nilearn_data(testpath):
    return fetch_development_fmri(n_subjects=1, age_group="adult",
                                  data_dir=str(testpath))
