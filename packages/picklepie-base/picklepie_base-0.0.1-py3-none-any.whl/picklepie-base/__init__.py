from . import base
from . import chart
from . import data # dataframe
from . import dlearn # deep learning
from . import mlearn # machine learning
from . import model
from . import statmodel # statistical model

from . import __eval

from pkg_resources import get_distribution as __dist

def version () :
    return __dist('picklepie-base').version

