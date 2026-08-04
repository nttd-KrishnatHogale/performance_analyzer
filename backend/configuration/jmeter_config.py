class JMeterConfig:

    def collect(

        self,

        users,

        ramp_up,

        duration,

        loops=None

    ):

        return {

            "users": users,

            "ramp_up": ramp_up,

            "duration": duration,

            "loops": loops

        }