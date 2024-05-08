from . import boxplot
from . import correlation
from . import density
from . import histogram
from . import pairplot
from . import scatterplot

from . import cumulative_gain
from . import lift
from . import precision_recall
from . import roc

def save (a_plot,a_file) :
    a_plot.savefig(fname=a_file)
