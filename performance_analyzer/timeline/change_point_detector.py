import pandas as pd


class ChangePointDetector:

    def detect(
            self,
            df,
            column,
            increase_percent=20
    ):

        events=[]

        previous=None

        for _,row in df.iterrows():

            value=row[column]

            if previous is None:

                previous=value

                continue

            change=((value-previous)/max(previous,1))*100

            if change>increase_percent:

                events.append({

                    "time":row["time"],

                    "old":previous,

                    "new":value,

                    "change":change

                })

            previous=value

        return events