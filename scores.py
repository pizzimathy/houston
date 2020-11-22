
from scipy.spatial.distance import euclidean


# Write our scoring function
def idealscore(ideal):
    r"""
    This function accepts an ideal (population) distribution and returns a score
    function. This score function rates a given districting plan based on its
    similarity (using some pre-defined metric of "similarity") to ``ideal``.

    :param list ideal: Desired values for a single statistic across :math:`k`
        districts; ``ideal`` is a :math:`k`-dimensional vector :math:`\pi`
        whose entries are in non-decreasing order on :math:`[0,1]` and such that

        .. math::
            \sum_{i=1}^k \pi_i \leq k,

        which matches the intuition that any given population can, at most, make
        up all of the population in any given district.

    :return: A score in :math:`[0,1]`.
    :rtype: float
    """
    def __(distribution):
        # First, we verify that the distribution sums properly.
        assert sum(distribution) <= len(distribution)

        # Now, we sort the values in the distribution so it doesn't matter in
        # what district the desired populations reside. This permutes the
        # entries in the vector such that they are in non-decreasing order.
        distribution = list(sorted(distribution))

        # Next, we find the euclidean distance between the two vectors.
        d_present = euclidean(ideal, distribution)

    return __
