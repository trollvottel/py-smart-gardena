from gardena.devices.abilities.device_info import DeviceInfoAbility
from gardena.devices.abilities.radio import RadioAbility
from gardena.devices.abilities.rechargeable_battery import RechargeableBatteryAbility


class Mower(RechargeableBatteryAbility, RadioAbility, DeviceInfoAbility):
    """Class to communicate with a mower"""

    internal_temperature = None
    mower_manual_operation = None
    mower_status = None
    mower_timestamp_next_start = None

    """Used to map data between 'mower' ability fields and class fields"""
    mower_ability_fields = {
        "manual_operation": "mower_manual_operation",
        "status": "mower_status",
        "timestamp_next_start": "mower_timestamp_next_start",
    }

    temperature_ability_fields = {"temperature": "internal_temperature"}

    def __init__(self, smart_system=None, location=None):
        super(Mower, self).__init__(smart_system=smart_system, location=location)
        self.register_abilities(
            {
                "robotic_mower": self.mower_ability_fields,
                "internal_temperature_sensor": self.temperature_ability_fields,
            }
        )

    def park_until_next_timer(self):
        self.call_command("mower", {"name": "park_until_next_timer"})

    def park_until_further_notice(self):
        self.call_command("mower", {"name": "park_until_further_notice"})

    def start_resume_schedule(self):
        self.call_command("mower", {"name": "start_resume_schedule"})

    def start_override_timer(self, duration=240):
        self.call_command(
            "mower",
            {"name": "start_override_timer", "parameters": {"duration": duration}},
        )
