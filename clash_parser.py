import requests
import yaml


class Clash_Parser:
    def __init__(self, url):
        self.profile, self.headers = self.get_profile(url)
        self.groups = self.get_group_name()
        self.proxies = self.get_proxy_name()

    def get_profile(self, url):
        response = requests.get(url)
        headers = response.headers
        return yaml.load(response.content, Loader=yaml.FullLoader), headers

    def dump_profile(self):
        return yaml.dump(self.profile, allow_unicode=True)

    def prepend_rules(self, rules):
        if isinstance(rules, list):
            rules.extend(self.profile["rules"])
            self.profile["rules"] = rules
        else:
            raise Exception("param: rules should be a list")

    def append_proxy_groups(self, groups):
        if isinstance(groups, list):
            self.profile["proxy-groups"].extend(groups)
            self.groups = self.get_group_name()
        else:
            raise Exception("param: groups should be a list")

    def get_group_name(self):
        return [group["name"] for group in self.profile["proxy-groups"]]

    def group_name_filter(self, keywords):
        group_name_list = []
        if isinstance(keywords, list):
            for keyword in keywords:
                for group in self.groups:
                    if keyword in group:
                        group_name_list.append(group)
            return group_name_list

        else:
            raise Exception("param: keywords should be a list")

    def get_proxy_name(self):
        return [proxy["name"] for proxy in self.profile["proxies"]]

    def proxy_name_filter(self, include=None, exclude=None):
        proxy_name_list = []
        if include is not None:
            if isinstance(include, list):
                for include_key in include:
                    for proxy in self.proxies:
                        if include_key in proxy:
                            proxy_name_list.append(proxy)
            else:
                raise Exception("param: include should be a list")
        if exclude is not None:
            include_proxy_name_list = proxy_name_list[:]
            proxy_name_list = []
            if isinstance(exclude, list):
                for exclude_key in exclude:
                    for include_proxy in include_proxy_name_list:
                        if exclude_key not in include_proxy:
                            proxy_name_list.append(include_proxy)
            else:
                raise Exception("param: exclude should be a list")
        return proxy_name_list

    def find_group_index(self, group):
        group_name_list = [proxy["name"] for proxy in self.profile["proxy-groups"]]
        return group_name_list.index(group)

    def set_proxies_in_group(self, in_group_proxies):
        for group in in_group_proxies:
            profile_group = self.profile["proxy-groups"][
                self.find_group_index(group["name"])
            ]
            profile_group["proxies"] = []
            proxies = profile_group["proxies"]
            if "proxies" in group.keys():
                proxies.extend(self.proxy_name_filter(**group["proxies"]))
            if "groups" in group.keys():
                proxies.extend(self.group_name_filter(group["groups"]))
