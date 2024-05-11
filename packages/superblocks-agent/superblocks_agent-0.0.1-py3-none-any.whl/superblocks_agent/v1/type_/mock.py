from typing import Callable

from superblocks_agent.v1.model.abstract.MockFilters import MockFilters

# when {these filters}
WhenCallable = Callable[[MockFilters], bool]

# when {these filters} return {this value}
# TODO: ugh. naming is hard
FilteredDictCallable = Callable[[MockFilters], dict]
