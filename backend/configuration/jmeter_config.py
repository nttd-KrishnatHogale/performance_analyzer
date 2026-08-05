# class JMeterConfig:

#     def collect(

#         self,

#         users,

#         ramp_up,

#         duration,

#         loops=None

#     ):

#         return {

#             "users": users,

#             "ramp_up": ramp_up,

#             "duration": duration,

#             "loops": loops

#         }

import xml.etree.ElementTree as ET

from config.config_service import ConfigService


class JMeterConfig:

    def collect(self):

        config = ConfigService()

        jmx_file = config.get("jmeter.test_plan")

        print("=" * 80)
        print("READING JMX:", jmx_file)
        print("=" * 80)

        root = ET.parse(jmx_file).getroot()

        thread_groups = []

        total_users = 0

        ramp_up = None
        duration = None
        loops = None

        for tg in root.iter("ThreadGroup"):

            name = tg.attrib.get("testname")

            users = int(
                tg.find("intProp[@name='ThreadGroup.num_threads']").text
            )

            ramp = int(
                tg.find("intProp[@name='ThreadGroup.ramp_time']").text
            )

            dur = int(
                tg.find("longProp[@name='ThreadGroup.duration']").text
            )

            loop_value = tg.find(
                ".//intProp[@name='LoopController.loops']"
            ).text

            thread_groups.append(
                {
                    "name": name,
                    "users": users,
                    "ramp_up": ramp,
                    "duration": dur,
                    "loops": "Forever" if loop_value == "-1" else int(loop_value)
                }
            )

            total_users += users

            ramp_up = ramp
            duration = dur
            loops = "Forever" if loop_value == "-1" else int(loop_value)

        configuration = {

            "total_users": total_users,

            "ramp_up": ramp_up,

            "duration": duration,

            "loops": loops,

            "thread_groups": thread_groups

        }

        print("\nJMeter Configuration")
        print(configuration)

        return configuration