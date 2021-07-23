Redistricting in Houston
========================

Documented here are key portions of the code, alongside some of the mathematics,
used to study redistricting in
Houston. First is the :class:`scores` module, which details the scoring methods
used to decide which districting plans are acceptable and which are not.

.. automodule:: scores
   :members:

The calculation of this score, which we call **Ideal**, takes
advantage of three key mathematical facts relating to its domain, a function
implicitly defined by the sorting of vector entries, and the image of the
previous function.

**Ideal**'s Domain
^^^^^^^^^^^^^^^^^^

First, we note that **Ideal** is a function from :math:`\{\pi\} \times \mathbb R^k`
to the reals, as we pair vectors in the space :math:`\mathbb R^k` with the our
ideal vector :math:`\pi`:

.. math::
	\textbf{Ideal}: \mathbb \{\pi\} \times \mathbb R^k \to \mathbb R.

However, we can further constrain the domain and image sets. First, we note that
any input vector :math:`v` to **Ideal** has all its entries in :math:`[0,1]`.
We label the set of vectors defined by the above condition by :math:`W`;
formally,

.. math::
	W = \left\{ v \in \mathbb R^k: v_i \in [0,1] \right\}.

Consequently, we have that :math:`||v||_2 \leq \sqrt k`, as, for any two vectors
:math:`p` and :math:`q` in :math:`W`, :math:`0 \leq (p_i-q_i)^2 \leq 1`. Thus,
the set :math:`W` is isomorphic to the chunk :math:`S^*` of the :math:`(k-1)`-dimensional
sphere :math:`S^{k-1} \supset S^*` such that all points in :math:`S^*` have
positive entries in :math:`[0,1]`. Now, we can better describe our function
**Ideal**:

.. math::
	\textbf{Ideal}: \{\pi\} \times W \to [0,1].


Implicit Functions on Sorted Vectors
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The purpose of the **Ideal** function is to compare some vector :math:`v` to
some "ideal" vector :math:`\pi` and spit out a score on :math:`[0,1]` telling
us how "close" the vectors are to each other. For our purposes, we're treating
these vectors as distributions – not as probability distributions, but as
population distributions –

