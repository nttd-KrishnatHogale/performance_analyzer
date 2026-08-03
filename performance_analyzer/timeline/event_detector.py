import pandas as pd

from performance_analyzer.timeline.event import TimelineEvent


class EventDetector:

    def detect(
        self,
        df,
        column,
        threshold,
        component,
        metric,
        severity="HIGH"
    ):

        if df is None:
            return []

        if df.empty:
            return []

        if column not in df.columns:
            return []

        events = []

        in_event = False

        start = None

        peak_time = None

        peak_value = 0

        for time, row in df.iterrows():

            value = row[column]

            if value >= threshold:

                if not in_event:

                    in_event = True

                    start = time

                    peak_time = time

                    peak_value = value

                elif value > peak_value:

                    peak_value = value

                    peak_time = time

            else:

                if in_event:

                    event = TimelineEvent(

                        component=component,

                        metric=metric,

                        severity=severity,

                        description=f"{metric} crossed {threshold}",

                        threshold=threshold,

                        peak_value=peak_value,

                        start_time=start,

                        peak_time=peak_time,

                        recovery_time=time,

                        duration_seconds=(time-start).total_seconds(),

                        metadata={}
                    )

                    events.append(event)

                    in_event=False

        if in_event:

            event = TimelineEvent(

                component=component,

                metric=metric,

                severity=severity,

                description=f"{metric} crossed {threshold}",

                threshold=threshold,

                peak_value=peak_value,

                start_time=start,

                peak_time=peak_time,

                recovery_time=None,

                duration_seconds=0,

                metadata={}
            )

            events.append(event)

        return events