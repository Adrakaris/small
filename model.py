
from constants import Pair


class Model:
    """
    A simple linear regression model in one dimension with one bias
    """

    def fit(self, data:list[Pair]) -> tuple[float,float]:
        """
        Parameters:
            data: list of {x, y} values, normalised between 0 and 1

        Return:
            a line of best fit, described by the two end y co-ordinates, between 0 and 1
        """
        # TODO: finish me
        return (0.25, 0.75)
