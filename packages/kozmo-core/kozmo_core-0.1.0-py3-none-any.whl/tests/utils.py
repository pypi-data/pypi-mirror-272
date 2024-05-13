import pytest

from kozmo_core.imports_helper import _TF_PRESENT

skipif_tf_missing = pytest.mark.skipif(
    not _TF_PRESENT, reason="tensorflow is not present"
)
