#!/usr/bin/python
#
# Copyright (C) 2019 Junyi Yi (@JunyiYi)
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
module: azure_rm_batchaccount
version_added: "2.9"
short_description: Manages a Batch Account on Azure.
description:
    - Create, update and delete instance of Azure Batch Account.

options:
    resource_group:
        description:
        - The name of the resource group in which to create the Batch Account.
        required: true
        type: str
    name:
        description:
        - The name of the Batch Account.
        required: true
        type: str
    location:
        description:
        - Specifies the supported Azure location where the resource exists.
        type: str
    auto_storage_account:
        description:
        - Existing storage account with which to associate the Batch Account.
        - It can be the storage account name which is in the same resource group.
        - "It can be the storage account ID. e.g.,
          /subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/myResourceGroup/providers/Microsoft.Storage/storageAccounts/mystorageaccount."
        - It can be a dict which contains C(name) and C(resource_group) of the storage account.
        type: raw
    key_vault:
        description:
        - Existing key vault with which to associate the Batch Account.
        - It can be the key vault name which is in the same resource group.
        - "It can be the key vault ID. e.g.,
          /subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/myResourceGroup/providers/Microsoft.KeyVault/vaults/myKeyVault."
        - It can be a dict which contains C(name) and C(resource_group) of the key vault.
        type: raw
    pool_allocation_mode:
        description:
        - The pool acclocation mode of the Batch Account.
        default: batch_service
        type: str
        choices:
        - batch_service
        - user_subscription
    state:
        description:
        - Assert the state of the Batch Account.
        - Use 'present' to create or update a Batch Account and 'absent' to delete it.
        default: present
        choices:
        - present
        - absent

extends_documentation_fragment:
    - azure
    - azure_tags

author:
    - "Junyi Yi (@JunyiYi)"
'''

EXAMPLES = '''
  - name: Create Batch Account
    azure_rm_batchaccount:
        resource_group: MyResourceGroup
        name: mybatchaccount
        location: eastus
        auto_storage_account:
          name: mystorageaccountname
        pool_allocation_mode: batch_service
'''

RETURN = '''
id:
    description:
    - The ID of the Batch account.
    returned: always
    type: str
    sample: "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/myResourceGroup/providers/Microsoft.Batch/batchAccounts/mybatchaccount"
account_endpoint:
    description:
    - The account endpoint used to interact with the Batch service.
    returned: always
    type: str
    sample: sampleacct.westus.batch.azure.com
'''

import time
from ansible.module_utils.azure_rm_common import normalize_location_name
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


class AzureRMBatchAccount(AzureRMModuleBaseExt):
    """Configuration class for an Azure RM Batch Account resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                required=True,
                type='str'
            ),
            name=dict(
                required=True,
                type='str'
            ),
            location=dict(
                type='str',
                updatable=False,
                disposition='/'
            ),
            auto_storage_account=dict(
                type='raw'
            ),
            key_vault=dict(
                type='raw',
                updatable=False,
                disposition='/'
            ),
            pool_allocation_mode=dict(
                default='batch_service',
                type='str',
                choices=['batch_service', 'user_subscription'],
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
        self.name = None
        self.batch_account = dict()
        self.tags = None

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.to_do = Actions.NoAction

        super(AzureRMBatchAccount, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                  supports_check_mode=True,
                                                  supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.batch_account[key] = kwargs[key]

        resource_group = self.get_resource_group(self.resource_group)
        if self.batch_account.get('location') is None:
            self.batch_account['location'] = resource_group.location
        if self.batch_account.get('auto_storage_account') is not None:
            self.batch_account['auto_storage'] = {
                'storage_account_id': self.normalize_resource_id(
                    self.batch_account.pop('auto_storage_account'),
                    '/subscriptions/{subscription_id}/resourceGroups/{resource_group}/providers/Microsoft.Storage/storageAccounts/{name}')
            }
        if self.batch_account.get('key_vault') is not None:
            id = self.normalize_resource_id(
                self.batch_account.pop('key_vault'),
                '/subscriptions/{subscription_id}/resourceGroups/{resource_group}/providers/Microsoft.KeyVault/vaults/{name}')
            url = 'https://' + id.split('/').pop() + '.vault.azure.net/'
            self.batch_account['key_vault_reference'] = {
                'id': id,
                'url': url
            }
        self.batch_account['pool_allocation_mode'] = _snake_to_camel(self.batch_account['pool_allocation_mode'], True)

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(BatchManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        old_response = self.get_batchaccount()

        if not old_response:
            self.log("Batch Account instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Batch Account instance already exists")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.results['old'] = old_response
                self.results['new'] = self.batch_account
                if not self.idempotency_check(old_response, self.batch_account):
                    self.to_do = Actions.Update

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the Batch Account instance")

            self.results['changed'] = True
            if self.check_mode:
                return self.results

            response = self.create_update_batchaccount()

            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("Batch Account instance deleted")
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_batchaccount()
        else:
            self.log("Batch Account instance unchanged")
            self.results['changed'] = False
            response = old_response

        if self.state == 'present':
            self.results.update({
                'id': response.get('id', None),
                'account_endpoint': response.get('account_endpoint', None)
            })
        return self.results

    def create_update_batchaccount(self):
        '''
        Creates or updates Batch Account with the specified configuration.

        :return: deserialized Batch Account instance state dictionary
        '''
        self.log("Creating / Updating the Batch Account instance {0}".format(self.name))

        try:
            if self.to_do == Actions.Create:
                response = self.mgmt_client.batch_account.create(resource_group_name=self.resource_group,
                                                                 account_name=self.name,
                                                                 parameters=self.batch_account)
            else:
                response = self.mgmt_client.batch_account.update(resource_group_name=self.resource_group,
                                                                 account_name=self.name,
                                                                 tags=self.tags,
                                                                 auto_storage=self.batch_account.get('auto_storage'))
            if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)
        except CloudError as exc:
            self.log('Error attempting to create the Batch Account instance.')
            self.fail("Error creating the Batch Account instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_batchaccount(self):
        '''
        Deletes specified Batch Account instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Batch Account instance {0}".format(self.name))
        try:
            response = self.mgmt_client.batch_account.delete(resource_group_name=self.resource_group,
                                                             account_name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete the Batch Account instance.')
            self.fail("Error deleting the Batch Account instance: {0}".format(str(e)))

        if isinstance(response, LROPoller) or isinstance(response, AzureOperationPoller):
            response = self.get_poller_result(response)
        return True

    def get_batchaccount(self):
        '''
        Gets the properties of the specified Batch Account
        :return: deserialized Batch Account instance state dictionary
        '''
        self.log("Checking if the Batch Account instance {0} is present".format(self.name))
        found = False
        try:
            response = self.mgmt_client.batch_account.get(resource_group_name=self.resource_group,
                                                          account_name=self.name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Batch Account instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Batch Account instance.')
        if found is True:
            return response.as_dict()
        return False


def main():
    """Main execution"""
    AzureRMBatchAccount()


if __name__ == '__main__':
    main()
