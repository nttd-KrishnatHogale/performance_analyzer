from backend.utils.logger import Logger

logger = Logger.get_logger()


class TimelinePrinter:

    def print(self, timeline):

        logger.info("=" * 80)

        logger.info("TIMELINE")

        logger.info("=" * 80)

        for e in timeline:

            logger.info(

                f"{e.start_time}"

                f" | {e.component}"

                f" | {e.metric}"

                f" | Peak={e.peak_value:.2f}"

                f" | Duration={e.duration_seconds}s"

            )

        logger.info("=" * 80)