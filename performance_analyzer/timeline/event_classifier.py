class EventClassifier:

    def classify(
            self,
            event
    ):

        metric=event["metric"].lower()

        if "cpu" in metric:

            return "Infrastructure"

        if "memory" in metric:

            return "Infrastructure"

        if "thread" in metric:

            return "Tomcat"

        if "oracle" in metric:

            return "Database"

        if "apache" in metric:

            return "Web"

        return "Unknown"