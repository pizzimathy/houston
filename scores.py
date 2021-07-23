
from scipy.optimize import linear_sum_assignment as lsa
import numpy as np
from numpy import e, floor


def temperature(t, L, N, k, phi=1/2):
    r"""
    Here we define our temperature parameter, which is a function polynomial in
    the number of steps in the chain. This is a sigmoid.

    :param int t: The current step number.
    :param float L: The maximum temperature achieved by the function.
    :param int N: The total number of steps.
    :param float k: The growth rate of the sigmoid.
    :param float phi: The fraction of N at which the temperature L/2 is achieved.
    :return: Temperature at time t, according to the parameterized sigmoid.
    :rtype: float
    """
    return L/(1+e**(-k*(t-phi*N)))


def maxcost(u, v):
    r"""
    Solves the maximum bipartite matching problem for the bipartite graph with
    vertex sets :math:`A=\{a_1,\dots,a_k\}` and :math:`B=\{b_1,\dots,b_k\}`
    such that the edge :math:`(a_i, b_j)` has weight :math:`|u_i-v_j|`, with
    :math:`u,v` distribution vectors in the unit :math:`k`-cube. Tells us the
    maximum sum of squared differences over all permutations of coordinates in
    :math:`u` and :math:`v`.

    :param list u: Vector.
    :param list v: Vector.
    :return: Maximum sum of squared differences.
    :rtype: float
    """
    # Create a cost matrix for the linear sum assignment method.
    C = np.array([
        [(u[i]-v[j])**2 for j in range(len(v))]
        for i in range(len(u))
    ])

    return np.sqrt(C[lsa(C, maximize=False)].sum())


def _npd(ideal, partition, name):
    """
    Finds the normalized permuted euclidean distance between the distribution
    vector of the provided updater (with alias ``name``) and the ideal vector
    provided in ``ideal``.

    :param list ideal: Vector.
    :param gerrychain.Partition partition: Current step in the chain.
    :param str name: Updater alias from which to get the distribution vector.
    :return: Normalized permuted euclidean distance in :math:`[0,1]`.
    :rtype: float
    """
    ideal = list(sorted(ideal))
    distribution = [partition[name][d] for d in partition.parts]

    return maxcost(ideal, distribution)/np.sqrt(len(partition))


def npd(i, name):
    """
    Wrapper function for the :meth:`_npd` method.

    :param list i: Ideal vector.
    :param str name: Updater alias from which to get the distribution vector.
    :return: :meth:`_npd` function with the ``ideal`` and ``name`` arguments
        pre-filled.
    :rtype: func
    """
    def __(partition):
        return _npd(i, partition, name)
    return __


# Write our scoring function
def ideal(ideal, updater, steps, L=700, k=1/2000, phi=1/2):
    r"""
    This function accepts an ideal (population) distribution and returns a score
    function. This score function rates a given districting plan based on its
    similarity (using some pre-defined metric of "similarity") to ``ideal``.

    :param list ideal: Desired values for a single statistic across :math:`k`
        districts; ``ideal`` is a :math:`k`-dimensional vector :math:`\pi`
        whose entries are in non-decreasing order on :math:`[0,1]` and such that

        .. math::
            \sum_{i=1}^k \pi_i \leq k,

        which matches the intuition that any given demographic group can, at
        most, make up all of the population in any given district.
    :param str updater: Updater alias for the statistic we're collecting.
    :param int steps: The number of steps taken by the chain simulation.
    :param int L: Maximum temperature.
    :param float k: Slope of the logit curve.
    :return: A function which produces a score in :math:`[0,1]`.
    :rtype: function
    """
    # Sort our ideal distribution.
    def __(partition):
        """
        :param gerrychain.Partition partition: Partition object for the current
            step in the chain.
        :return: Normalized permuted euclidean distance.
        :rtype: float
        """
        # First, we retrieve the distributions.

        # Now, we calculate the difference between the current score and the
        # previous score; the score should be negative if the current score is
        # better than the last one.
        dist = _npd(ideal, partition, updater)
        temp = -temperature(partition["step"], L, steps, k, phi=phi)
        sigma = temp * dist

        # Return our exponentiated score.
        return min(1, e**sigma)
    return __


def droop(seats, updater):
    r"""
    Returns an updater function to calculate how many seats are won by a given
    voting bloc in a district. Makes use of the droop quota, which gives that,
    for :math:`n` ballots cast in an election for :math:`k` seats, any candidate
    receiving

    .. math::
        \left\lfloor \frac{n}{k+1} \right\rfloor + 1

    ballots is guaranteed to win a seat. We can infer, then, that any population
    making up a :math:`1/(k+1)` proportion of the population can elect a
    candidate of their choice.

    :param int seats: The number of seats per district.
    :param str updater: The name of the updater for population proportions.
    :return: Updater function.
    :rtype: func
    """
    def __(partition):
        return {
            district: min(seats, floor(partition[updater][district]/(1/(seats+1))))
            for district in partition.parts
        }
    return __


def cutedges(updater):
    def __(partition):
        return len(partition[updater])
    return __
