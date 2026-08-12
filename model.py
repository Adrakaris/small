
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
        
        # you need two points to make a line
        if len(data) < 2:
            return (0, 0)

        x_bar = self.mean(data, 0)
        y_bar = self.mean(data, 1)

        m_top = sum(((pt.x - x_bar) * (pt.y - y_bar) for pt in data))
        m_bottom = sum((pt.x - x_bar) ** 2 for pt in data)
        m = m_top / m_bottom

        c = y_bar - m * x_bar
        
        return (c, m + c)

    def mean(self, data:list[Pair], index:int) -> float:
        sum = 0
        for i in data:
            sum += i[index]
        return sum / len(data)
