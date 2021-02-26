from PyQt5.QtChart import QBarSeries


class GraphBar:
    def __init__(self):
        pass

    def create_graph(self, sets, ranges):
        sets_arr = []
        for i in range(len(sets)):
            print(i)
            sets_arr.append(sets[i])
            sets_arr[i].append(ranges[i])

        series = QBarSeries()
        for ele in sets_arr:
            series.append(ele)
        return series
