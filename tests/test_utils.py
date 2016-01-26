import pytest

from addok_trigrams.utils import compute_trigrams


@pytest.mark.parametrize('given,expected', [
    ['lille', ['lil', 'ill', 'lle']],
    ['y', ['y']],
    ['31310', ['31310']],
])
def test_compute_trigrams(given, expected):
    assert compute_trigrams(given) == expected
