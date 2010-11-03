"""\
Fuzzy number module. Contains basic fuzzy number class definitions.

@author: Aaron Mavrinac
@organization: University of Windsor
@contact: mavrin1@uwindsor.ca
@license: LGPL-3
"""

from math import e, sqrt, log
from numbers import Number

from .fset import FuzzySet


class RealRange(tuple):
    """\
    Real range class.
    """
    def __new__(cls, arg=(0.0, 0.0)):
        """\
        Instatiation method. Verifies the validity of the range argument
        before returning the range object.
        """
        if not len(arg) == 2:
            raise ValueError('range must consist of two values')
        if not isinstance(arg[0], Number) \
        or not isinstance(arg[1], Number):
            raise TypeError('range values must be numeric')
        if arg[0] > arg[1]:
            raise ValueError('range may not have negative size')
        return tuple.__new__(cls, arg)

    @property
    def size(self):
        """\
        Return the size of the range.

        @rtype: C{float}
        """
        return float(self[1] - self[0])

    def __add__(self, other):
        """\
        Addition operation.
   
        @param other: The other operand.
        @type other: L{RealRange}
        @return: Sum of ranges.
        @rtype: L{RealRange}
        """
        return RealRange((self[0] + other[0], self[1] + other[1]))

    def __sub__(self, other):
        """\
        Subtraction operation.
   
        @param other: The other operand.
        @type other: L{RealRange}
        @return: Difference of ranges.
        @rtype: L{RealRange}
        """
        return RealRange((self[0] - other[1], self[1] - other[0]))

    def __contains__(self, value):
        """\
        Report whether a given value is within this range.

        @param value: The value.
        @type value: C{float}
        @return: True if within the range, false otherwise.
        @rtype: C{bool}
        """
        return value >= self[0] and value <= self[1]

    def issubset(self, other):
        """\
        Report whether another range contains this range.

        @param other: The other range.
        @type other: L{RealRange}
        @return: True if a subset, false otherwise.
        @rtype: C{bool}
        """
        if not isinstance(other, RealRange):
            raise TypeError('argument must be a RealRange')
        if other[0] <= self[0] and other[1] >= self[1]:
            return True
        return False

    def issuperset(self, other):
        """\
        Report whether this range contains another range.

        @param other: The other range.
        @type other: L{RealRange}
        @return: True if a superset, false otherwise.
        @rtype: C{bool}
        """
        if not isinstance(other, RealRange):
            raise TypeError('argument must be a RealRange')
        if self[0] <= other[0] and self[1] >= other[1]:
            return True
        return False

    __le__ = issubset
    __ge__ = issuperset

    def __lt__(self, other):
        """\
        Report whether another range strictly contains this range.

        @param other: The other range.
        @type other: L{RealRange}
        @return: True if a strict subset, false otherwise.
        @rtype: C{bool}
        """
        return self.issubset(other) and not self == other

    def __gt__(self, other):
        """\
        Report whether this range strictly contains another range.

        @param other: The other range.
        @type other: L{RealRange}
        @return: True if a strict superset, false otherwise.
        @rtype: C{bool}
        """
        return self.issuperset(other) and not self == other


class FuzzyNumber(object):
    """\
    Fuzzy number class (abstract base class for all fuzzy numbers).
    """
    def __init__(self):
        """\
        Constructor. Not to be instantiated directly.
        """
        if self.__class__ is FuzzyNumber:
            raise NotImplementedError('please use one of the subclasses')

    def __repr__(self):
        """\
        Return the canonical representation of a fuzzy number.

        @return: Canonical representation.
        @rtype: C{str}
        """
        return '<%s>' % self.__class__.__name__

    def __str__(self):
        """\
        Return the string representation of a fuzzy number.

        @return: String representation.
        @rtype: C{str}
        """
        return '%s: kernel %s, support %s' % \
               (self.__class__.__name__, str(self.kernel), str(self.support))

    @staticmethod
    def _binary_sanity_check(other):
        """\
        Check that the other argument to a binary operation is also a
        fuzzy number, raising a TypeError otherwise.

        @param other: The other argument.
        @type other: L{FuzzyNumber}
        """
        if not isinstance(other, FuzzyNumber):
            raise TypeError('operation only permitted between fuzzy numbers')

    def mu(self, value):
        """\
        Return the membership level of a value in the universal set domain of
        the fuzzy number.

        @param value: A value in the universal set.
        @type value: C{float}
        """
        raise NotImplementedError('mu method must be overridden')

    def normalize(self):
        """\
        Normalize this fuzzy number, so that its height is equal to 1.0.
        """
        if not self.height == 1.0:
            raise NotImplementedError('normalize method must be overridden')

    def to_polygonal(self):
        """\
        Convert this fuzzy number into a polygonal fuzzy number.

        @return: Result polygonal fuzzy number.
        @rtype: L{PolygonalFuzzyNumber}
        """
        raise NotImplementedError('to_polygonal method must be overridden')

    kernel = None
    support = None
    height = None

    def __or__(self, other):
        """\
        Return the standard fuzzy union of two polygonal fuzzy numbers.

        @param other: The other fuzzy number.
        @type other: L{FuzzyNumber}
        @return: The fuzzy union.
        @rtype: L{FuzzyNumber}
        """
        return self.union(other)

    def __ior__(self, other):
        """\
        In-place standard fuzzy union.

        @param other: The other fuzzy number.
        @type other: L{FuzzyNumber}
        @return: The fuzzy union (self).
        @rtype: L{FuzzyNumber}
        """
        self = self.union(other)
        return self

    def union(self, other):
        """\
        Return the standard fuzzy union of two fuzzy numbers as a new polygonal
        fuzzy number.

        @param other: The other fuzzy number.
        @type other: L{FuzzyNumber}
        @return: The fuzzy union.
        @rtype: L{PolygonalFuzzyNumber}
        """
        self._binary_sanity_check(other)
        return self.to_polygonal() | other.to_polygonal()

    def __and__(self, other):
        """\
        Return the standard fuzzy intersection of two fuzzy numbers.

        @param other: The other fuzzy number.
        @type other: L{FuzzyNumber}
        @return: The fuzzy intersection.
        @rtype: L{FuzzyNumber}
        """
        return self.intersection(other)

    def __iand__(self, other):
        """\
        In-place standard fuzzy intersection.

        @param other: The other fuzzy number.
        @type other: L{FuzzyNumber}
        @return: The fuzzy intersection (self).
        @rtype: L{FuzzyNumber}
        """
        self = self.intersection(other)
        return self

    def intersection(self, other):
        """\
        Return the standard fuzzy intersection of two fuzzy numbers as a new
        polygonal fuzzy number.

        @param other: The other fuzzy number.
        @type other: L{FuzzyNumber}
        @return: The fuzzy union.
        @rtype: L{PolygonalFuzzyNumber}
        """
        self._binary_sanity_check(other)
        return self.to_polygonal() & other.to_polygonal()


class PolygonalFuzzyNumber(FuzzyNumber):
    """\
    Polygonal fuzzy number class.
    """
    def __init__(self, points):
        """\
        Constructor.

        @param points: A set of points from which to generate the polygon.
        @type points: C{list} of C{tuple}
        """
        if not points[0][1] == 0.0 or not points[-1][1] == 0.0:
            raise ValueError('points must start and end with mu = 0')
        for i in range(1, len(points)):
            if not points[i][0] >= points[i - 1][0]:
                raise ValueError('points must be in increasing order')
        self.points = points
        super(PolygonalFuzzyNumber, self).__init__()

    def __repr__(self):
        """\
        Return the canonical string representation of this polygonal fuzzy
        number.

        @return: Canonical string representation.
        @rtype: C{str}
        """
        return 'PolygonalFuzzyNumber(%s)' % self.points

    def __eq__(self, other):
        """\
        Return whether this polygonal fuzzy number is equal to another fuzzy
        number.

        @param other: The other fuzzy number.
        @type other: L{FuzzyNumber}
        @return: True if equal.
        @rtype: C{bool}
        """
        return self.points == other.to_polygonal().points

    def mu(self, value):
        """\
        Return the membership level of a value in the universal set domain of
        the fuzzy number.

        @param value: A value in the universal set.
        @type value: C{float}
        """
        if not True in [value in subrange for subrange in self.support]:
            return 0.0
        for i in range(1, len(self.points)):
            if self.points[i][0] > value:
                return ((value - self.points[i - 1][0]) / (self.points[i][0] \
                       - self.points[i - 1][0])) * (self.points[i][1] - \
                       self.points[i - 1][1]) + self.points[i - 1][1]
        return 0.0

    @property
    def kernel(self):
        """\
        Return the kernel of the fuzzy number (range of values in the
        universal set where membership degree is equal to one).

        @rtype: C{list} of L{RealRange}
        """
        kernel = []
        start = None
        for i in range(1, len(self.points)):
            if start is None and self.points[i][1] == 1.0:
                start = i
            elif start is not None and self.points[i][1] < 1.0:
                kernel.append(RealRange((self.points[start][0],
                                         self.points[i - 1][0])))
                start = None
        return kernel

    @property
    def support(self):
        """\
        Return the support of the fuzzy number (range of values in the
        universal set where membership degree is nonzero).

        @rtype: C{list} of L{RealRange}
        """
        support = []
        start = None
        for i in range(1, len(self.points)):
            if start is None and self.points[i][1] > 0.0:
                start = i - 1
            elif start is not None and self.points[i][1] == 0.0:
                support.append(RealRange((self.points[start][0],
                                          self.points[i][0])))
                start = None
        return support

    @property
    def height(self):
        """\
        Return the height of the fuzzy number (maximum membership degree
        value).

        @rtype: C{float}
        """
        return max([point[1] for point in self.points])

    @staticmethod
    def _line_intersection(p, q, r, s):
        """\
        Return the point of intersection of line segments pq and rs. Helper
        function for union and intersection.

        @return: The point of intersection.
        @rtype: C{tuple} of C{float}
        """
        try:
            ua = ((s[0] - r[0]) * (p[1] - r[1]) - \
                 (s[1] - r[1]) * (p[0] - r[0])) / \
                 ((s[1] - r[1]) * (q[0] - p[0]) - \
                 (s[0] - r[0]) * (q[1] - p[1]))
        except ZeroDivisionError:
            return None
        return(p[0] + ua * (q[0] - p[0]), p[1] + ua * (q[1] - p[1]))

    def union(self, other):
        """\
        Return the standard fuzzy union of two polygonal fuzzy numbers as a new
        polygonal fuzzy number.

        @param other: The other fuzzy number.
        @type other: L{FuzzyNumber}
        @return: The fuzzy union.
        @rtype: L{PolygonalFuzzyNumber}
        """
        other = other.to_polygonal()
        # collect and sort all the existing points
        points = [[point, i, self] for i, point in enumerate(self.points)] \
               + [[point, i, other] for i, point in enumerate(other.points)]
        points.sort()
        # take the maximum of duplicates
        i = 0
        while True:
            try:
                if points[i][0][0] == points[i + 1][0][0]:
                    if points[i][0][1] < points[i + 1][0][1]:
                        del points[i]
                    else:
                        del points[i + 1]
                    continue
                i += 1
            except IndexError:
                break
        # add intersection points
        i = 0
        while True:
            try:
                if points[i][2] is not points[i + 1][2]:
                    int = self._line_intersection(points[i][0],
                        points[i][2].points[points[i][1] + 1], points[i + 1][0],
                        points[i + 1][2].points[points[i + 1][1] - 1])
                    if int and int[1] > 0 and int[0] > points[i][0][0] \
                       and int[0] < points[i + 1][0][0]:
                        points.insert(i + 1, [int, None, None])
                        i += 1
                i += 1
            except IndexError:
                break
        # take the maximum mu value for all points
        for point in points:
            point[0] = (point[0][0], max(self.mu(point[0][0]), other.mu(point[0][0])))
        # remove redundant points
        while points[1][0][1] == 0.0:
            del points[0]
        while points[-2][0][1] == 0.0:
            del points[-1]
        i = 1
        while True:
            try:
                if points[i][0][1] == points[i - 1][0][1] \
                   and points[i][0][1] == points[i + 1][0][1]:
                    del points[i]
                    continue
                i += 1
            except IndexError:
                break
        return PolygonalFuzzyNumber([point[0] for point in points])

    def intersection(self, other):
        """\
        Return the standard fuzzy intersection of two polygonal fuzzy numbers
        as a new polygonal fuzzy number.

        @param other: The other fuzzy number.
        @type other: L{FuzzyNumber}
        @return: The fuzzy intersection.
        @rtype: L{PolygonalFuzzyNumber}
        """
        other = other.to_polygonal()
        # collect and sort all the existing points
        points = [[point, i, self] for i, point in enumerate(self.points)] \
               + [[point, i, other] for i, point in enumerate(other.points)]
        points.sort()
        # take the minimum of duplicates
        i = 0
        while True:
            try:
                if points[i][0][0] == points[i + 1][0][0]:
                    if points[i][0][1] > points[i + 1][0][1]:
                        del points[i]
                    else:
                        del points[i + 1]
                    continue
                i += 1
            except IndexError:
                break
        # add intersection points
        i = 0
        while True:
            try:
                if points[i][2] is not points[i + 1][2]:
                    int = self._line_intersection(points[i][0],
                        points[i][2].points[points[i][1] + 1], points[i + 1][0],
                        points[i + 1][2].points[points[i + 1][1] - 1])
                    if int and int[1] > 0 and int[0] > points[i][0][0] \
                       and int[0] < points[i + 1][0][0]:
                        points.insert(i + 1, [int, None, None])
                        i += 1
                i += 1
            except IndexError:
                break
        # take the minimum mu value for all points
        for point in points:
            point[0] = (point[0][0], min(self.mu(point[0][0]), other.mu(point[0][0])))
        # remove redundant points
        while points[1][0][1] == 0.0:
            del points[0]
        while points[-2][0][1] == 0.0:
            del points[-1]
        i = 1
        while True:
            try:
                if points[i][0][1] == points[i - 1][0][1] \
                   and points[i][0][1] == points[i + 1][0][1]:
                    del points[i]
                    continue
                i += 1
            except IndexError:
                break
        return PolygonalFuzzyNumber([point[0] for point in points])

    def normalize(self):
        """\
        Normalize this fuzzy number, so that its height is equal to 1.0.
        """
        self.points = [(point[0], point[1] * (1.0 / self.height)) \
                       for point in self.points]

    def to_polygonal(self):
        """\
        Return this polygonal fuzzy number.

        @return: This polygonal fuzzy number.
        @rtype: L{PolygonalFuzzyNumber}
        """
        return self

    def to_fuzzy_set(self, samplepoints=None):
        """\
        Convert this polygonal fuzzy number to a discrete fuzzy set at the
        specified sample points. If no sample points are specified, the
        vertices of the polygonal fuzzy number will be used.

        @param samplepoints: Set of points at which to sample the number.
        @type samplepoints: C{set} of C{float}
        @return: Result fuzzy set.
        @rtype: L{fset.FuzzySet}
        """
        if samplepoints is None:
            samplepoints = [point[0] for point in self.points]
        F = FuzzySet()
        for point in samplepoints:
            F.add(point, self.mu(point))
        return F


class TrapezoidalFuzzyNumber(FuzzyNumber):
    """\
    Trapezoidal fuzzy number class.
    """
    def __init__(self, kernel=(0.0, 0.0), support=(0.0, 0.0)):
        """\
        Constructor.

        @param kernel: The kernel of the fuzzy number.
        @type kernel: C{tuple}
        @param support: The support of the fuzzy number.
        @type support: C{tuple}
        """
        if not (isinstance(kernel, tuple) and len(kernel) == 2) \
        or not (isinstance(support, tuple) and len(support) == 2):
            raise TypeError('kernel and support must be 2-tuples')
        self.kernel = RealRange(kernel)
        self.support = RealRange(support)
        if not self.kernel <= self.support:
            raise ValueError('kernel range must be within support range')
        self.height = 1.0
        super(TrapezoidalFuzzyNumber, self).__init__()

    @property
    def triangular(self):
        """\
        Report if this is a triangular fuzzy number (kernel has zero size).

        @rtype: C{bool}
        """
        return self.kernel.size == 0

    def __add__(self, other):
        """\
        Addition operation.

        @param other: The other trapezoidal fuzzy number.
        @type other: L{TrapezoidalFuzzyNumber}
        @return: Sum of the trapezoidal fuzzy numbers.
        @rtype: L{TrapezoidalFuzzyNumber}
        """
        if not isinstance(other, TrapezoidalFuzzyNumber):
            raise TypeError('operation only permitted between trapezoidal '
                            'fuzzy numbers')
        return self.__class__(self.kernel + other.kernel,
                              self.support + other.support)

    def __sub__(self, other):
        """\
        Subtraction operation.

        @param other: The other trapezoidal fuzzy number.
        @type other: L{TrapezoidalFuzzyNumber}
        @return: Difference of the trapezoidal fuzzy numbers.
        @rtype: L{TrapezoidalFuzzyNumber}
        """
        if not isinstance(other, TrapezoidalFuzzyNumber):
            raise TypeError('operation only permitted between trapezoidal '
                            'fuzzy numbers')
        return self.__class__(self.kernel - other.kernel,
                              self.support - other.support)

    def mu(self, value):
        """\
        Return the membership level of a value in the universal set domain of
        the fuzzy number.

        @param value: A value in the universal set.
        @type value: C{float}
        """
        if value in self.kernel:
            return 1.
        elif value > self.support[0] and value < self.kernel[0]:
            return (value - self.support[0]) / \
                   (self.kernel[0] - self.support[0])
        elif value < self.support[1] and value > self.kernel[1]:
            return (self.support[1] - value) / \
                   (self.support[1] - self.kernel[1])
        else:
            return 0.

    def alpha(self, alpha):
        """\
        Alpha cut function. Returns the interval within the fuzzy number whose
        membership levels meet or exceed the alpha value.

        @param alpha: The alpha value for the cut in [0, 1].
        @type alpha: C{float}
        @return: The alpha cut interval.
        @rtype: L{RealRange}
        """
        return RealRange(((self.kernel[0] - self.support[0]) * alpha \
                           + self.support[0], self.support[1] - \
                           (self.support[1] - self.kernel[1]) * alpha))

    def to_polygonal(self):
        """\
        Convert this trapezoidal fuzzy number into a polygonal fuzzy number.

        @return: Result polygonal fuzzy number.
        @rtype: L{PolygonalFuzzyNumber}
        """
        points = [(self.support[0], 0.0),
                  (self.kernel[0], 1.0),
                  (self.kernel[1], 1.0),
                  (self.support[1], 0.0)]
        return PolygonalFuzzyNumber(points)


class TriangularFuzzyNumber(TrapezoidalFuzzyNumber):
    """\
    Triangular fuzzy number class (special case of trapezoidal fuzzy number).
    """
    def __init__(self, kernel=0.0, support=(0.0, 0.0)):
        """\
        Constructor.

        @param kernel: The kernel value of the fuzzy number.
        @type kernel: C{float}
        @param support: The support of the fuzzy number.
        @type support: C{tuple}
        """
        super(TriangularFuzzyNumber, self).__init__(kernel=(kernel, kernel),
            support=support)


class GaussianFuzzyNumber(FuzzyNumber):
    """\
    Gaussian fuzzy number class.
    """
    def __init__(self, mean, stddev):
        """\
        Constructor.

        @param mean: The mean (central value) of the Gaussian.
        @type mean: C{float}
        @param stddev: The standard deviation of the Gaussian.
        @type stddev: C{float}
        """
        self.mean = mean
        self.stddev = stddev
        self.height = 1.0
        super(GaussianFuzzyNumber, self).__init__()

    def __add__(self, other):
        """\
        Addition operation.

        @param other: The other gaussian fuzzy number.
        @type other: L{GaussianFuzzyNumber}
        @return: Sum of the gaussian fuzzy numbers.
        @rtype: L{GaussianFuzzyNumber}
        """
        if not isinstance(other, GaussianFuzzyNumber):
            raise TypeError('operation only permitted between Gaussian '
                            'fuzzy numbers')
        return self.__class__(self.mean + other.mean,
                              self.stddev + other.stddev)

    def __sub__(self, other):
        """\
        Subtraction operation.
        
        @param other: The other gaussian fuzzy number.
        @type other: L{GaussianFuzzyNumber}
        @return: Difference of the gaussian fuzzy numbers.
        @rtype: L{GaussianFuzzyNumber}
        """
        if not isinstance(other, GaussianFuzzyNumber):
            raise TypeError('operation only permitted between Gaussian '
                            'fuzzy numbers')
        return self.__class__(self.mean - other.mean,
                              self.stddev + other.stddev)
    
    def mu(self, value):
        """\
        Return the membership level of a value in the universal set domain of
        the fuzzy number.

        @param value: A value in the universal set.
        @type value: C{float}
        """
        return e ** -((value - self.mean) ** 2 / (2.0 * self.stddev ** 2)) \
            if value in self.support else 0.0

    @property
    def kernel(self):
        """\
        Return the kernel of the fuzzy number (range of values in the
        universal set where membership degree is equal to one).

        @rtype: L{RealRange}
        """
        return RealRange((self.mean, self.mean))

    @property
    def support(self):
        """\
        Return the support of the fuzzy number (range of values in the
        universal set where membership degree is nonzero).

        @rtype: L{RealRange}
        """
        return self.alpha(1e-10)

    def alpha(self, alpha):
        """\
        Alpha cut function. Returns the interval within the fuzzy number whose
        membership levels meet or exceed the alpha value.

        @param alpha: The alpha value for the cut in [0, 1].
        @type alpha: C{float}
        @return: The alpha cut interval.
        @rtype: L{RealRange}
        """
        if alpha < 1e-10:
            alpha = 1e-10
        edge = sqrt(-2.0 * (self.stddev ** 2) * log(alpha))
        return RealRange((self.mean - edge, self.mean + edge))

    def to_polygonal(self, np=20):
        """\
        Convert this Gaussian fuzzy number into a polygonal fuzzy number
        (approximate).

        @param np: The number of points to interpolate per side (optional).
        @type np: C{int}
        @return: Result polygonal fuzzy number.
        @rtype: L{PolygonalFuzzyNumber}
        """
        if np < 0:
            raise ValueError('number of points must be positive')
        points = []
        start, end = self.support
        increment = (self.mean - start) / float(np + 1)
        points.append((start, 0.0))
        for i in range(1, np + 1):
            value = start + i * increment
            points.append((value, self.mu(value)))
        points.append((self.mean, 1.0))
        for i in range(1, np + 1):
            value = self.mean + i * increment
            points.append((value, self.mu(value)))
        points.append((end, 0.0))
        return PolygonalFuzzyNumber(points)
