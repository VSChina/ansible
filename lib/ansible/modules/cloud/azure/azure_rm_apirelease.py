#!/usr/bin/python
#
# Copyright (C) 2019 audevbot
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

# ----------------------------------------------------------------------------
#
#     ***     AUTO GENERATED CODE    ***    AUTO GENERATED CODE     ***
#
# ----------------------------------------------------------------------------
#
#     This file is automatically generated by Magic Modules and manual
#     changes will be clobbered when the file is regenerated.
#
#     Please read more about how to change this file at
#     https://github.com/Azure/magic-module-specs
#
# ----------------------------------------------------------------------------

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = '''
---
module: azure_rm_apirelease
version_added: "2.9"
short_description: Manage Azure ApiRelease instance.
description:
    - Create, update and delete instance of Azure Api Release.

options:
    resource_group:
        description:
        - The name of the resource group.
        required: true
        type: str
    api_id:
        description:
        - Identifier of the API the release belongs to.
        - It can be the TBD name which is in the same resource group.
        - "It can be the TBD ID. e.g., /subscriptions/{{ subscription_id }}/resourceGroups/{{ resource_group
          }}/providers/Microsoft.ApiManagement/service/{{ service_name }}/apis/{{ name }}."
        - It can be a dict which contains C(name) and C(resource_group) of the TBD.
        type: raw
    notes:
        description:
        - Release Notes.
        type: str
    release_id:
        description:
        - Release identifier within an API. Must be unique in the current API Management service instance.
        required: true
        type: str
    service_name:
        description:
        - The name of the API Management service.
        required: true
        type: str
    state:
        description:
        - Assert the state of the Api Release.
        - Use 'present' to create or update a Api Release and 'absent' to delete it.
        default: present
        choices:
        - present
        - absent

extends_documentation_fragment:
    - azure
    
author:
    - "audevbot"
'''


RETURN = '''
created_date_time:
    description:
    - 'The time the API was released. The date conforms to the following format: yyyy-MM-ddTHH:mm:ssZ as specified by the ISO 8601 standard.'
    returned: always
    type: str
updated_date_time:
    description:
    - The time the API release was updated.
    returned: always
    type: str
id:
    description:
    - Resource ID.
    returned: always
    type: str
name:
    description:
    - Resource name.
    returned: always
    type: str
type:
    description:
    - Resource type for API Management resource.
    returned: always
    type: str
'''

import time
from ansible.module_utils.azure_rm_common_ext import AzureRMModuleBaseExt
from ansible.module_utils.common.dict_transformations import _snake_to_camel

try:
    from msrestazure.azure_exceptions import CloudError
    from msrest.polling import LROPoller
    from msrestazure.azure_operation import AzureOperationPoller
    from msrest.serialization import Model
    from azure.mgmt.apimanagement import ApiManagementClient
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMApiRelease(AzureRMModuleBaseExt):
    """Configuration class for an Azure RM Api Release resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                required=True,
                type='str'
            ),
            api_id=dict(
                required=True,
                type='str',
                updatable=False,
                disposition='/'
            ),
            api_id=dict(
                type='raw'
            ),
            notes=dict(
                type='str'
            ),
            release_id=dict(
                required=True,
                type='str',
                updatable=False,
                disposition='/'
            ),
            service_name=dict(
                required=True,
                type='str',
                updatable=False,
                disposition='/'
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group = None
        self.service_name = None
        self.api_id = None
        self.release_id = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMApiRelease, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                supports_check_mode=True,
                                                supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()):
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.parameters[key] = kwargs[key]

        if self.parameters.get('api_id') is not None:
            self.parameters['api_id'] = self.normalize_resource_id(
                self.parameters['api_id'],
                '/subscriptions/{{ subscription_id }}/resourceGroups/{{ resource_group }}/providers/Microsoft.ApiManagement/service/{{ service_name }}/apis/{{ name }}')

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(ApiManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        old_response = self.get_apirelease()

        if not old_response:
            self.log("Api Release instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Api Release instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.results['old'] = old_response
                self.results['new'] = self.parameters
                if not self.idempotency_check(old_response, self.parameters):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Api Release instance")

            self.results['changed'] = True
            if self.check_mode:
                return self.results

            response = self.create_update_apirelease()

            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Api Release instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_apirelease()
        else:
            self.log("Api Release instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'created_date_time': response.get('created_date_time', None),
                'updated_date_time': response.get('updated_date_time', None),
                'id': response.get('id', None),
                'name': response.get('name', None),
                'type': response.get('type', None)
            })
        return self.results

    def create_update_apirelease(self):
        '''
        Creates or updates Api Release with the specified configuration.

        :return: deserialized Api Release instance state dictionary
        '''
        self.log("Creating / Updating the Api Release instance {0}".format(self.name))

        try:
            if self.to_do == Actions.Create:
                response = self.mgmt_client.api_release.create_or_update(resource_group_name=self.resource_group,
                                                                         service_name=self.service_name,
                                                                         api_id=self.api_id,
                                                                         release_id=self.release_id,
                                                                         parameters=self.parameters)
            else:
                response = self.mgmt_client.api_release.update(resource_group_name=self.resource_group,
                                                               service_name=self.service_name,
                                                               api_id=self.api_id,
                                                               release_id=self.release_id,
                                                               parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        except CloudError as exc:
            self.log('Error attempting to create the Api Release instance.')
            self.fail("Error creating the Api Release instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_apirelease(self):
        '''
        Deletes specified Api Release instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Api Release instance {0}".format(self.name))
        try:
            response = self.mgmt_client.api_release.delete(resource_group_name=self.resource_group,
                                                           service_name=self.service_name,
                                                           api_id=self.api_id,
                                                           release_id=self.release_id)
        except CloudError as e:
            self.log('Error attempting to delete the Api Release instance.')
            self.fail("Error deleting the Api Release instance: {0}".format(str(e)))

        if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
            response = self.get_poller_result(response)
        return True

    def get_apirelease(self):
        '''
        Gets the properties of the specified Api Release
        :return: deserialized Api Release instance state dictionary
        '''
        self.log("Checking if the Api Release instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.api_release.get(resource_group_name=self.resource_group,
                                                        service_name=self.service_name,
                                                        api_id=self.api_id,
                                                        release_id=self.release_id)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Api Release instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Api Release instance.')
        if found is True:
            return response.as_dict()
        return False


def main():
    """Main execution"""
    AzureRMApiRelease()


if __name__ == '__main__':
    main()
