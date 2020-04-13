"""
Py_Qualtrics_API is comprised of two classes:

#. :class:`~py_qualtrics_api.QualtricsAPI`, which does blah;
#. :class:`~py_qualtrics_api.APIConfig`, which does blah.
"""

from py_qualtrics_api.tools import *
name = "py_qualrics_api"
from pkg_resources import get_distribution, DistributionNotFound
from os.path import join

__all__ = ['QualtricsAPI', 'APIConfig']

# This approach to setting the __version__ attribute on the package
# was stolen from:
# http://stackoverflow.com/questions/17583443/what-is-the-correct-way-to-share-package-version-with-setup-py-and-the-package
try:
    _dist = get_distribution('py_qualtrics_api')
    if not _dist:
    # if not __file__.startswith(join(_dist.location, 'pyinter')):
        # not installed, but there is another version that *is*
        raise DistributionNotFound
except DistributionNotFound:
    __version__ = 'Please install this project with setup.py'
else:
    __version__ = _dist.version
