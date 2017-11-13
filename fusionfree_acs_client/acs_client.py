"""Fusion FreeACS client"""

from suds.client import Client


class ACSClient(object):
    """ACS client to interact with Fusion FreeACS"""

    def __init__(self, acs_url, acs_username, acs_password):
        """Instantiate ACS client"""

        self.client = Client(acs_url)
        login = self.client.factory.create('Login')
        login.username = acs_username
        login.password = acs_password
        self.client.login = login

    def add_unit_type(self, name, vendor, description, parameters=None):
        """Add a unit type"""

        client = self.client
        unittype = client.factory.create('Unittype')
        unittype.name = name
        unittype.vendor = vendor
        unittype.description = description
        params = []
        if not parameters:
            parameters = []
        for parameter in parameters:
            param = client.factory.create('Parameter')
            param.name = parameter
            param.value = 'RWD'
            params.append(param)
        if params:
            parameter_list = client.factory.create('parameterList')
            parameter_array = client.factory.create('ArrayOfParameter')
            parameter_array.item = params
            parameter_list.parameterArray = parameter_array
            unittype.parameters = parameter_list
        client.service.addOrChangeUnittype(client.login, unittype)

    def get_unit_types(self, name):
        """Get unit types"""

        client = self.client
        client.service.getUnittypes(client.login, name)

    def delete_unit_type(self, name):
        """Delete unit type"""

        client = self.client
        client.service.deleteUnittype(client.login, name)

    def add_profile(self, unit_type_name, profile_name, parameters=None):
        """Add a profile"""

        client = self.client
        unittype = client.factory.create('Unittype')
        unittype.name = unit_type_name
        profile = client.factory.create('Profile')
        profile.name = profile_name
        params = []
        if not parameters:
            parameters = {}
        for name, value in parameters.items():
            param = client.factory.create('Parameter')
            param.name = name
            param.value = value
            params.append(param)
        if params:
            parameter_list = client.factory.create('parameterList')
            parameter_array = client.factory.create('ArrayOfParameter')
            parameter_array.item = params
            parameter_list.parameterArray = parameter_array
            profile.parameters = parameter_list
        client.service.addOrChangeProfile(client.login, unittype, profile)

    def get_profiles(self, unit_type_name, profile_name):
        """Get profiles"""

        client = self.client
        unittype = client.factory.create('Unittype')
        unittype.name = unit_type_name
        profile = client.factory.create('Profile')
        profile.name = profile_name
        client.service.getProfiles(client.login, unittype, profile)

    def delete_profile(self, unit_type_name, profile_name):
        """Delete a profile"""

        client = self.client
        unittype = client.factory.create('Unittype')
        unittype.name = unit_type_name
        profile = client.factory.create('Profile')
        profile.name = profile_name
        client.service.deleteProfile(client.login, unittype, profile)

    def add_unit(self, unit_id, unit_secret, unit_type_name,
                 profile_name, parameters=None):

        """Add a unit"""

        client = self.client
        unittype = client.factory.create('Unittype')
        unittype.name = unit_type_name
        profile = client.factory.create('Profile')
        profile.name = profile_name
        unit = client.factory.create('Unit')
        unit.unitId = unit_id
        unit.unittype = unittype
        unit.profile = profile
        params = []
        secret = client.factory.create('Parameter')
        secret.name = 'System.X_OWERA-COM.Secret'
        secret.value = unit_secret
        params.append(secret)
        if not parameters:
            parameters = {}
        for name, value in parameters.items():
            param = client.factory.create('Parameter')
            param.name = name
            param.value = value
            params.append(param)
        if params:
            parameter_list = client.factory.create('parameterList')
            parameter_array = client.factory.create('ArrayOfParameter')
            parameter_array.item = params
            parameter_list.parameterArray = parameter_array
            unit.parameters = parameter_list
        client.service.addOrChangeUnit(client.login, unit)

    def delete_unit(self, unit_id):
        """Delete a unit"""

        client = self.client
        unit = client.factory.create('Unit')
        unit.unitId = unit_id
        client.service.deleteUnit(client.login, unit)
