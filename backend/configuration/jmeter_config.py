import xml.etree.ElementTree as ET

from config.config_service import ConfigService


class JMeterConfig:

    def get_prop(self, node, name, default="0"):
        """
        Returns the value of a JMeter property regardless of whether it is
        stored as stringProp, intProp or longProp.
        """

        for tag in ("stringProp", "intProp", "longProp"):
            element = node.find(f'{tag}[@name="{name}"]')
            if element is not None and element.text is not None:
                return element.text

        return default

    def collect(self):

        config = ConfigService()

        jmx_file = config.get("jmeter.test_plan")

        print("=" * 80)
        print("READING JMX:", jmx_file)
        print("=" * 80)

        tree = ET.parse(jmx_file)
        root = tree.getroot()

        thread_groups = []

        total_users = 0
        ramp_up = None
        duration = None
        loops = None

        for tg in root.iter("ThreadGroup"):

            name = tg.attrib.get("testname", "")

            users = int(
                self.get_prop(
                    tg,
                    "ThreadGroup.num_threads",
                    "0"
                )
            )

            ramp = int(
                self.get_prop(
                    tg,
                    "ThreadGroup.ramp_time",
                    "0"
                )
            )

            duration_text = self.get_prop(
                tg,
                "ThreadGroup.duration",
                "0"
            )

            try:
                dur = int(duration_text)
            except ValueError:
                dur = 0

            loop_value = self.get_prop(
                tg,
                "LoopController.loops",
                "-1"
            )

            thread_groups.append(
                {
                    "name": name,
                    "users": users,
                    "ramp_up": ramp,
                    "duration": dur,
                    "loops": (
                        "Forever"
                        if loop_value == "-1"
                        else int(loop_value)
                    )
                }
            )

            total_users += users

            ramp_up = ramp
            duration = dur
            loops = (
                "Forever"
                if loop_value == "-1"
                else int(loop_value)
            )

        configuration = {
            "total_users": total_users,
            "ramp_up": ramp_up,
            "duration": duration,
            "loops": loops,
            "thread_groups": thread_groups
        }

        print("=" * 80)
        print("JMeter Configuration")
        print(configuration)
        print("=" * 80)

        return configuration