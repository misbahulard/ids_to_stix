def find(key, dictionary):
    for k, v in dictionary.iteritems():
        if k == key:
            yield v
        elif isinstance(v, dict):
            for result in find(key, v):
                yield result
        elif isinstance(v, list):
            for d in v:
                for result in find(key, d):
                    yield result


example = {'app_url': '', 'models': [
    {'perms': {'add': True, 'change': True, 'delete': True}, 'add_url': '/admin/cms/news/add/',
     'admin_url': '/admin/cms/news/', 'name': ''}], 'has_module_perms': True, 'name': u'CMS'}

observable = {"type": "observed-data", "id": "observed-data--1452f8f2-3d85-4df3-b137-5005c7f5ea6b",
              "created": "2018-04-13T01:03:43.279Z", "modified": "2018-04-13T01:03:43.279Z",
              "first_observed": "2018-04-13T01:03:43.279105Z", "last_observed": "2018-04-13T01:03:43.279105Z",
              "number_observed": 1, "objects": {"0": {"type": "ipv4-addr", "value": "10.0.2.16"},
                                                "1": {"type": "ipv4-addr", "value": "173.194.70.94"},
                                                "2": {"type": "network-traffic", "src_ref": "0", "dst_ref": "1",
                                                      "src_port": 49165, "dst_port": 80, "protocols": ["ipv4", "tcp"]}}}

# x = list(find('models', example))
# print x

# y = list(find('created', observable))
# print y
