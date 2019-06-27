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

ANSIBLE_METADATA = {'metadata_version': '1.1', 'status': ['preview'], 'supported_by': 'community'}


DOCUMENTATION = '''
---
module: azure_rm_batchaccount_info
version_added: "2.9"
short_description: Gather info for Azure Batch Account
description:
    - Gather info for Azure Batch Account.

options:
    resource_group:
        description:
        - The name of the resource group in which to create the Batch Account.
        required: true
        type: str
    name:
        description:
        - The name of the Batch Account.
        type: str
    tags:
        description:
        - Limit results by providing a list of tags. Format tags as 'key' or 'key:value'.
        type: list

extends_documentation_fragment:
    - azure
    
author:
    - "Junyi Yi (@JunyiYi)"
'''

EXAMPLES = '''
  - name: Get instance of Batch Account
    azure_rm_batchaccount_info:
        resource_group: MyResourceGroup
        name: mybatchaccount

  - name: List instances of Batch Account
    azure_rm_batchaccount_info:
        resource_group: MyResourceGroup
'''

RETURN = '''
items:
    description: List of items
    returned: always
    type: complex
    contains:
        id:
            description:
            - The ID of the Batch account.
            returned: always
            type: str
            sample: "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/myResourceGroup/providers/Microsoft.Batch/batchAccounts/mybatchaccount"
        resource_group:
            description:
            - The name of the resource group in which to create the Batch Account.
            returned: always
            type: str
        name:
            description:
            - The name of the Batch Account.
            returned: always
            type: str
        location:
            description:
            - Specifies the supported Azure location where the resource exists.
            returned: always
            type: str
        account_endpoint:
            description:
            - The account endpoint used to interact with the Batch service.
            returned: always
            type: str
            sample: sampleacct.westus.batch.azure.com
        auto_storage_account:
            description:
            - Existing storage account with which to associate the Batch Account.
            returned: always
            type: str
            sample:
              "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/myResourceGroup/providers/Microsoft.Storage/storageAccounts/mystorageaccount"
        key_vault:
            description:
            - Existing key vault with which to associate the Batch Account.
            returned: always
            type: str
            sample: "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/myResourceGroup/providers/Microsoft.KeyVault/vaults/myKeyVault"
        pool_allocation_mode:
            description:
            - The pool acclocation mode of the Batch Account.
            returned: always
            type: str
        tags:
            description:
            - Resource tags.
            returned: always
            type: list
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.batch import BatchManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMBatchAccountInfo(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(resource_group=dict(required=True, type='str'), name=dict(type='str'), tags=dict(type='list'))
        # store the results of the module operation
        self.results = dict(changed=False)
        self.mgmt_client = None
        self.resource_group = None
        self.name = None
        self.tags = None
        super(AzureRMBatchAccountInfo, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(BatchManagementClient, base_url=self._cloud_environment.endpoints.resource_manager)

        if self.resource_group is not None and self.name is not None:
            self.results['items'] = self.get()
        elif self.resource_group is not None:
            self.results['items'] = self.list_by_resource_group()
        else:
            self.results['items'] = self.list_by_subscription()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.batch_account.get(resource_group_name=self.resource_group, account_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get info for Batch Account.')

        if response and self.has_tags(response.tags, self.tags):
            results.append(self.format_response(response))

        return results

    def list_by_resource_group(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.batch_account.list_by_resource_group(resource_group_name=self.resource_group)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get info for Batch Account.')

        if response is not None:
            for item in response:
                if self.has_tags(item.tags, self.tags):
                    results.append(self.format_response(item))

        return results

    def list_by_subscription(self):
        response = None
        results = []
        try:
            response = self.mgmt_client.batch_account.list()
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get info for Batch Account.')

        if response is not None:
            for item in response:
                if self.has_tags(item.tags, self.tags):
                    results.append(self.format_response(item))

        return results

    def format_response(self, item):
        d = item.as_dict()
        d = {
            'id': d['id'],
            'resource_group': self.resource_group,
            'name': d['name'],
            'location': d['location'],
            'account_endpoint': d['account_endpoint'],
            'auto_storage_account': d['auto_storage']['storage_account_id'],
            'key_vault': d['key_vault_reference']['id'],
            'pool_allocation_mode': d['pool_allocation_mode'],
            'tags': d['tags'],
        }
        return d


def main():
    AzureRMBatchAccountInfo()


if __name__ == "__main__":
    main()
