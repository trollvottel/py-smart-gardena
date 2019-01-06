from gardena.base_gardena_class import BaseGardenaClass


class BaseGardenaDeviceClass(BaseGardenaClass):
    """Base class for Gardena devices"""

    # Common fields
    description = None
    category = None
    is_configuration_synchronized = False

    abilities = {}

    def __init__(self, smart_system=None, location=None):
        """Constructor, create instance of a gardena location"""
        super(BaseGardenaDeviceClass, self).__init__(smart_system)
        if location is None:
            raise ValueError("Argument 'location' is missing")
        self.location = location

    def handle_abilities(self, abilities):
        for ability in abilities:
            if ability["type"] in self.abilities:
                self.set_ability_field(ability, self.abilities[ability["type"]])

    def register_abilities(self, abilities):
        for ability, ability_description in abilities.items():
            self.abilities[ability] = ability_description

    def set_ability_field(self, hashmap, fields_hashmap):
        for prop in hashmap["properties"]:
            if prop["name"] in fields_hashmap:
                setattr(self, fields_hashmap[prop["name"]], prop["value"])

    def update_information(self, information):
        super(BaseGardenaDeviceClass, self).update_information(information)
        self.set_field_if_exists(information, "description", "description")
        self.set_field_if_exists(information, "category", "category")
        self.set_field_if_exists(information, "device_state", "device_state")
        self.set_field_if_exists(
            information, "configuration_synchronized", "is_configuration_synchronized"
        )
        if "abilities" in information:
            self.handle_abilities(information["abilities"])

    def call_command(self, command, data):
        url = (
            "https://smart.gardena.com/sg-1/devices/"
            + self.id
            + "/abilities/"
            + command
            + "/command?locationId="
            + self.location.id
        )
        self.smart_system.call_smart_system(url=url, request_type="post", data=data)
