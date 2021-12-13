# THIS NEEDS TO BE MADE AN ARTIFACT

class MovingAverage:
    def __init__(self, window_len):
        self.values = []
        self.window_len = window_len

    def add(self, value):
        num_values = len(self.values)
        if num_values < self.window_len:
            self.values.append(value)
        else:
            self.values.pop(0)
            self.values.append(value)

    def get_moving_average(self):
        total = 0.0
        for i in self.values:
            total = total + float(i)
        average = total / len(self.values)
        return round(average, 2)

    def get_values(self):
        return self.values


# example usage
def main():
    values = [10, 21, 33, 41, 50, 60, 65, 70, 78, 80]
    window_len = 5

    s1 = MovingAverage(window_len)

    for i in values:
        print('---')
        s1.add(i)
        print(s1.get_values())
        moving_avg = s1.get_moving_average()
        print('moving_average=' + moving_avg.__str__())


if __name__ == '__main__':
    main()

