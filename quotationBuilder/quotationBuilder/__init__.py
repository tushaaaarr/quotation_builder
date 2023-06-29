from __future__ import absolute_import

# Get git tag and SHA-id
from ._version import get_active_branch_name
__version__ = get_active_branch_name()
del get_active_branch_name
