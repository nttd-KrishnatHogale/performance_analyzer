class EventMerger:

    def merge(self, events):

        if not events:

            return []

        events = sorted(

            events,

            key=lambda x: x.start_time

        )

        merged = []

        for e in events:

            merged.append(e)

        return merged