from datetime import datetime


class DurationCalculator:

    def calculate(
            self,
            start,
            end
    ):

        if start is None:

            return 0

        if end is None:

            return 0

        return (end-start).total_seconds()