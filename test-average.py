
import matplotlib.pyplot as plt
from charting.plots import lines
from charting.defaults import style
from numpy import median, sqrt, random
from scipy.spatial.distance import euclidean
from scores import maxcost


def npd(ideal, v):
	ideal = list(sorted(ideal))
	v = list(reversed(sorted(v)))
	return euclidean(ideal, v)/sqrt(len(ideal))


k = 4
ideal = [random.uniform() for _ in range(k)]
sample = [random.uniform() for _ in range(k)]

print(maxcost([1,0], [3/4, 1/2]))
