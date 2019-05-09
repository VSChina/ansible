# Copyright (c) 2016 Matt Davis, <mdavis@ansible.com>
#                    Chris Houseknecht, <house@redhat.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from ansible.module_utils.azure_rm_common import AzureRMModuleBase
import re
from ansible.module_utils.common.dict_transformations import _camel_to_snake, _snake_to_camel


class AzureRMModuleBaseExt(AzureRMModuleBase):

    def inflate_parameters(self, spec, body, level):
        if isinstance(body, list):
            for item in body:
                self.inflate_parameters(spec, item, level)
            return
        for name in spec.keys():
            # first check if option was passed
            param = body.get(name)
            if not param:
                continue
            # check if pattern needs to be used
            pattern = spec[name].get('pattern', None)
            if pattern:
                if pattern == 'camelize':
                    param = _snake_to_camel(param, True)
                else:
                    param = self.normalize_resource_id(param, pattern)
                    body[name] = param
            disposition = spec[name].get('disposition', '*')
            if level == 0 and not disposition.startswith('/'):
                continue
            if disposition == '/':
                disposition = '/*'
            parts = disposition.split('/')
            if parts[0] == '':
                # should fail if level is > 0?
                parts.pop(0)
            target_dict = body
            elem = body.pop(name)
            while len(parts) > 1:
                target_dict = target_dict.setdefault(parts.pop(0), {})
            targetName = parts[0] if parts[0] != '*' else name
            target_dict[targetName] = elem
            if spec[name].get('options'):
                self.inflate_parameters(spec[name].get('options'), target_dict[targetName], level + 1)

    def normalize_resource_id(self, value, pattern):
        '''
        Return a proper resource id string..

        :param resource_id: It could be a resource name, resource id or dict containing parts from the pattern.
        :param pattern: pattern of resource is, just like in Azure Swagger
        '''
        pattern_parts = pattern.split('/')
        for i in range(len(pattern_parts)):
            x = re.sub('[{} ]+', '', pattern_parts[i], 2)
            if len(x) < len(pattern_parts[i]):
                pattern_parts[i] = '{' + re.sub('([a-z0-9])([A-Z])', r'\1_\2', x).lower() + '}'

        if isinstance(value, str):
            value_parts = value.split('/')
            if len(value_parts) == 1:
                value_dict = {}
                value_dict['name'] = value
            else:
                if len(value_parts) != len(pattern_parts):
                    return None
                value_dict = {}
                for i in range(len(value_parts)):
                    if pattern_parts[i].startswith('{'):
                        value_dict[pattern_parts[i][1:-1]] = value_parts[i]
                    elif value_parts[i].lower() != pattern_parts[i].lower():
                        return None
        elif isinstance(value, dict):
            value_dict = value
        else:
            return None

        if not value_dict.get('subscription_id'):
            value_dict['subscription_id'] = self.subscription_id
        if not value_dict.get('resource_group'):
            value_dict['resource_group'] = self.resource_group

        for i in range(len(pattern_parts)):
            if pattern_parts[i].startswith('{'):
                value = value_dict.get(pattern_parts[i][1:-1], None)
                if not value:
                    return None
                pattern_parts[i] = value

        return "/".join(pattern_parts)

    def idempotency_check(self, old_params, new_params):
        '''
        Return True if something changed. Function will use fields from module_arg_spec to perform dependency checks.
        :param old_params: old parameters dictionary, body from Get request.
        :param new_params: new parameters dictionary, unpacked module parameters.
        '''
        modifiers = {}
        result = {}
        self.create_compare_modifiers(self.module.argument_spec, '', modifiers)
        self.results['modifiers'] = modifiers
        return self.default_compare(modifiers, new_params, old_params, '', self.results)

    def create_compare_modifiers(self, arg_spec, path, result):
        for k in arg_spec.keys():
            o = arg_spec[k]
            updatable = o.get('updatable', True)
            comparison = o.get('comparison', 'default')
            disposition = o.get('disposition', '*')
            if disposition == '/':
                disposition = '/*'
            p = (path +
                 ('/' if len(path) > 0 else '') +
                 disposition.replace('*', k) +
                 ('/*' if o['type'] == 'list' else ''))
            if comparison != 'default' or not updatable:
                result[p] = {'updatable': updatable, 'comparison': comparison}
            if o.get('options'):
                self.create_compare_modifiers(o.get('options'), p, result)

    def default_compare(self, modifiers, new, old, path, result):
        '''
            Default dictionary comparison.
            This function will work well with most of the Azure resources.
            It correctly handles "location" comparison.

            Value handling:
                - if "new" value is None, it will be taken from "old" dictionary if "incremental_update"
                  is enabled.
            List handling:
                - if list contains "name" field it will be sorted by "name" before comparison is done.
                - if module has "incremental_update" set, items missing in the new list will be copied
                  from the old list

            Warnings:
                If field is marked as non-updatable, appropriate warning will be printed out and
                "new" structure will be updated to old value.

            :modifiers: Optional dictionary of modifiers, where key is the path and value is dict of modifiers
            :param new: New version
            :param old: Old version

            Returns True if no difference between structures has been detected.
            Returns False if difference was detected.
        '''
        if new is None:
            return True
        elif isinstance(new, dict):
            if not isinstance(old, dict):
                result['compare'] = 'changed [' + path + '] old dict is null'
                return False
            for k in new.keys():
                if not self.default_compare(modifiers, new.get(k), old.get(k, None), path + '/' + k, result):
                    return False
            return True
        elif isinstance(new, list):
            if not isinstance(old, list) or len(new) != len(old):
                result['compare'] = 'changed [' + path + '] length is different or null'
                return False
            if isinstance(old[0], dict):
                key = None
                if 'id' in old[0] and 'id' in new[0]:
                    key = 'id'
                elif 'name' in old[0] and 'name' in new[0]:
                    key = 'name'
                else:
                    key = next(iter(old[0]))
                    new = sorted(new, key=lambda x: x.get(key, None))
                    old = sorted(old, key=lambda x: x.get(key, None))
            else:
                new = sorted(new)
                old = sorted(old)
            for i in range(len(new)):
                if not self.default_compare(modifiers, new[i], old[i], path, result):
                    return False
            return True
        else:
            updatable = modifiers.get(path, {}).get('updatable', True)
            comparison = modifiers.get(path, {}).get('comparison', 'default')
            if comparison == 'default' and (path == '/location' or path.endswith('locationName')):
                comparison = 'location'
            if comparison == 'location':
                new = new.replace(' ', '').lower()
                old = old.replace(' ', '').lower()
            elif comparison == 'insensitive':
                new = new.lower()
                old = old.lower()
            elif comparison == 'ignore':
                return True
            if str(new) == str(old):
                result['compare'] = result.get('compare', '') + "(" + str(new) + ":" + str(old) + ")"
                return True
            else:
                result['compare'] = 'changed [' + path + '] ' + str(new) + ' != ' + str(old)
                if updatable:
                    return False
                else:
                    # XXX change new value to old
                    self.module.warn("property '" + path + "' cannot be updated (" + str(old) + "->" + str(new) + ")")
                    return True
