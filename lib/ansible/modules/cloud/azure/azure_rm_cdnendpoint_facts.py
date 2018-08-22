#!/usr/bin/python
#
# Copyright (c) 2018 Hai Cao, <t-haicao@microsoft.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: azure_rm_cdnendpoint_facts

version_added: "2.7"

short_description: Get Azure CDN endpoint facts

description:
    - Get facts for a specific Azure CDN endpoint or all Azure CDN endpoints.

options:
    name:
        description:
            - Limit results to a specific Azure CDN endpoint.
    resource_group:
        description:
            - The resource group to search for the desired Azure CDN endpoint
    tags:
        description:
            - Limit results by providing a list of tags. Format tags as 'key' or 'key:value'.

extends_documentation_fragment:
    - azure

author:
    - "Hai Cao <t-haicao@microsoft.com>"
'''

EXAMPLES = '''
'''

RETURN = '''
cdnendpoints:
    description: List of Azure CDN endpoints.
    returned: always
    type: complex
    contains:
        resource_group:
            description:
                - Name of a resource group where the Azure CDN endpoint exists.
            returned: always
            type: str
            sample: testGroup
        name:
            description:
                - Name of the Azure CDN endpoint.
            returned: always
            type: str
            sample: Testing
        state:
            description:
                - The state of the Azure CDN endpoint.
            type: str
            sample: present
        location:
            description:
                - Location of the Azure CDN endpoint.
            type: str
            sample: WestUS
        id:
            description
                - ID of the Azure CDN endpoint.
            type: str
            sample: /subscriptions/XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX/resourcegroups/cdntest/providers/Microsoft.Cdn/profiles/cdntest
        provisioning_state:
            description:
                - Provisioning status of the profile.
            type: str
            sample: Succeeded
        resource_state:
            description:
                - Resource status of the profile.
            type: str
            sample: Active
        sku:
            description:
                - The pricing tier (defines a CDN provider, feature list and rate) of the Azure CDN endpoint.
            type: str
            sample: Standard_Verizon
        type:
            description:
                - The type of the Azure CDN endpoint.
            type: str
            sample: Microsoft.Cdn/profiles
        tags:
            description:
                - The tags of the Azure CDN endpoint.
            type: list
            sample: [
                {"foo": "bar"}
            ]
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from azure.mgmt.cdn.models import ErrorResponseException
    from azure.common import AzureHttpError
except:
    # handled in azure_rm_common
    pass

import re

AZURE_OBJECT_CLASS = 'endpoints'


class AzureRMCdnendpointFacts(AzureRMModuleBase):
    """Utility class to get Azure Azure CDN endpoint facts"""

    def __init__(self):

        self.module_args = dict(
            name=dict(type='str'),
            resource_group=dict(
                type='str',
                required=True
            ),
            profile_name=dict(
                type='str',
                required=True
            ),
            tags=dict(type='list')
        )

        self.results = dict(
            changed=False,
            cdnendpoints=[]
        )

        self.name = None
        self.resource_group = None
        self.profile_name = None
        self.tags = None

        super(AzureRMCdnendpointFacts, self).__init__(
            derived_arg_spec=self.module_args,
            supports_tags=False,
            facts_module=True
        )

    def exec_module(self, **kwargs):

        for key in self.module_args:
            setattr(self, key, kwargs[key])

        if self.name:
            self.results['cdnendpoints'] = self.get_item()
        else:
            self.results['cdnendpoints'] = self.list_by_profile()

        return self.results

    def get_item(self):
        """Get a single Azure Azure CDN endpoint"""

        self.log('Get properties for {0}'.format(self.name))

        item = None
        result = []

        try:
            item = self.cdn_management_client.endpoints.get(
                self.resource_group, self.profile_name, self.name)
        except ErrorResponseException:
            pass

        if item and self.has_tags(item.tags, self.tags):
            result = [self.serialize_cdnendpoint(item)]

        return result

    def list_by_profile(self):
        """Get all Azure Azure CDN endpoints within an Azure CDN profile"""

        self.log('List all Azure CDN endpoints within an Azure CDN profile')

        try:
            response = self.cdn_management_client.endpoints.list_by_profile(
                self.resource_group, self.profile_name)
        except AzureHttpError as exc:
            self.fail('Failed to list all items - {0}'.format(str(exc)))

        results = []
        for item in response:
            if self.has_tags(item.tags, self.tags):
                results.append(self.serialize_cdnendpoint(item))

        return results

    def serialize_cdnendpoint(self, cdnendpoint):
        '''
        Convert a Azure CDN endpoint object to dict.
        :param cdn: Azure CDN endpoint object
        :return: dict
        '''
        result = self.serialize_obj(cdnendpoint, AZURE_OBJECT_CLASS)

        new_result = {}
        new_result['id'] = cdnendpoint.id
        new_result['resource_group'] = re.sub('\\/.*', '', re.sub('.*resourcegroups\\/', '', result['id']))
        new_result['profile_name'] = re.sub('\\/.*', '', re.sub('.*profiles\\/', '', result['id']))
        new_result['name'] = cdnendpoint.name
        new_result['type'] = cdnendpoint.type
        new_result['location'] = cdnendpoint.location
        new_result['state'] = 'present'
        new_result['resource_state'] = cdnendpoint.resource_state
        new_result['provisioning_state'] = cdnendpoint.provisioning_state
        new_result['query_string_caching_behavior'] = cdnendpoint.query_string_caching_behavior
        new_result['is_compression_enabled'] = cdnendpoint.is_compression_enabled
        new_result['is_http_allowed'] = cdnendpoint.is_http_allowed
        new_result['is_https_allowed'] = cdnendpoint.is_https_allowed
        new_result['content_types_to_compress'] = cdnendpoint.content_types_to_compress
        new_result['origin_host_header'] = cdnendpoint.origin_host_header
        new_result['origin_path'] = cdnendpoint.origin_path
        new_result['tags'] = cdnendpoint.tags
        return new_result


def main():
    """Main module execution code path"""

    AzureRMCdnendpointFacts()


if __name__ == '__main__':
    main()
