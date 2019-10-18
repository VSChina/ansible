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
module: azure_rm_applicationpackage
version_added: "2.9"
short_description: Manage Azure ApplicationPackage instance.
description:
    - Create, update and delete instance of Azure Application Package.

options:
    resource_group:
        description:
        - The name of the resource group that contains the Batch account.
        required: true
        type: str
    account_name:
        description:
        - The name of the Batch account.
        required: true
        type: str
    application_name:
        description:
        - The name of the application. This must be unique within the account.
        required: true
        type: str
    version_name:
        description:
        - The version of the application.
        required: true
        type: str
    state:
        description:
        - Assert the state of the Application Package.
        - Use 'present' to create or update a Application Package and 'absent' to delete it.
        default: present
        choices:
        - present
        - absent

extends_documentation_fragment:
    - azure

author:
    - audevbot
'''


RETURN = '''
state:
    description:
    - The current state of the application package.
    returned: always
    type: str
format:
    description:
    - The format of the application package, if the package is active.
    returned: always
    type: str
storage_url:
    description:
    - The URL for the application package in Azure Storage.
    returned: always
    type: str
storage_url_expiry:
    description:
    - The UTC time at which the Azure Storage URL will expire.
    returned: always
    type: str
last_activation_time:
    description:
    - The time at which the package was last activated, if the package is active.
    returned: always
    type: str
id:
    description:
    - The ID of the resource.
    returned: always
    type: str
etag:
    description:
    - The ETag of the resource, used for concurrency statements.
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
    from azure.mgmt.batch import BatchManagementClient
except ImportError:
    # This is handled in azure_rm_common
    pass


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMApplicationPackage(AzureRMModuleBaseExt):
    """Configuration class for an Azure RM Application Package resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                required=True,
                type='str'
            ),
            account_name=dict(
                required=True,
                type='str',
                updatable=False,
                disposition='/'
            ),
            application_name=dict(
                required=True,
                type='str',
                updatable=False,
                disposition='/'
            ),
            version_name=dict(
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
        self.account_name = None
        self.application_name = None
        self.version_name = None
        self.parameters = dict()

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMApplicationPackage, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                        supports_check_mode=True,
                                                        supports_tags=False)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()):
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.parameters[key] = kwargs[key]


        response = None

        self.mgmt_client = self.get_mgmt_svc_client(BatchManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        old_response = self.get_applicationpackage()

        if not old_response:
            self.log("Application Package instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Application Package instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.results['old'] = old_response
                self.results['new'] = self.parameters
                if not self.idempotency_check(old_response, self.parameters):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Application Package instance")

            self.results['changed'] = True
            if self.check_mode:
                return self.results

            response = self.create_update_applicationpackage()

            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Application Package instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_applicationpackage()
        else:
            self.log("Application Package instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'state': response.get('state', None),
                'format': response.get('format', None),
                'storage_url': response.get('storage_url', None),
                'storage_url_expiry': response.get('storage_url_expiry', None),
                'last_activation_time': response.get('last_activation_time', None),
                'id': response.get('id', None),
                'etag': response.get('etag', None)
            })
        return self.results

    def create_update_applicationpackage(self):
        '''
        Creates or updates Application Package with the specified configuration.

        :return: deserialized Application Package instance state dictionary
        '''
        self.log("Creating / Updating the Application Package instance {0}".format(self.name))

        try:
            response = self.mgmt_client.application_package.create(resource_group_name=self.resource_group,
                                                                   account_name=self.account_name,
                                                                   application_name=self.application_name,
                                                                   version_name=self.version_name,
                                                                   parameters=self.parameters)
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        except CloudError as exc:
            self.log('Error attempting to create the Application Package instance.')
            self.fail("Error creating the Application Package instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_applicationpackage(self):
        '''
        Deletes specified Application Package instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Application Package instance {0}".format(self.name))
        try:
            response = self.mgmt_client.application_package.delete(resource_group_name=self.resource_group,
                                                                   account_name=self.account_name,
                                                                   application_name=self.application_name,
                                                                   version_name=self.version_name)
        except CloudError as e:
            self.log('Error attempting to delete the Application Package instance.')
            self.fail("Error deleting the Application Package instance: {0}".format(str(e)))

        if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
            response = self.get_poller_result(response)
        return True

    def get_applicationpackage(self):
        '''
        Gets the properties of the specified Application Package
        :return: deserialized Application Package instance state dictionary
        '''
        self.log("Checking if the Application Package instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.application_package.get(resource_group_name=self.resource_group,
                                                                account_name=self.account_name,
                                                                application_name=self.application_name,
                                                                version_name=self.version_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Application Package instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Application Package instance.')
        if found is True:
            return response.as_dict()
        return False


def main():
    """Main execution"""
    AzureRMApplicationPackage()


if __name__ == '__main__':
    main()
