import json
import prettytable
import textwrap
import six

def print_dict(d, dict_property="Property", dict_value="Value", wrap=0):
    pt = prettytable.PrettyTable([dict_property, dict_value], caching=False)
    pt.align = 'l'
    for k, v in sorted(d.items()):
        # convert dict to str to check length
        if isinstance(v, (dict, list)):
            # v = jsonutils.dumps(v)
            v = json.dumps(v)
        if wrap > 0:
            v = textwrap.fill(str(v), wrap)
        # if value has a newline, add in multiple rows
        # e.g. fault with stacktrace
        if v and isinstance(v, six.string_types) and r'\n' in v:
            lines = v.strip().split(r'\n')
            col1 = k
            for line in lines:
                pt.add_row([col1, line])
                col1 = ''
        else:
            if v is None:
                v = '-'
            pt.add_row([k, v])

    # result = encodeutils.safe_encode(pt.get_string())
    result = pt.get_string()

    if six.PY3:
        result = result.decode()

    print(result)


def print_list(objs, fields, formatters={}, sortby_index=None):
    '''
    give the fields of objs to be printed.
    :param objs:
    :param fields: the fields to be printed
    :param formatters:
    :param sortby_index:
    :return:
    '''
    if sortby_index is None:
        sortby = None
    else:
        sortby = fields[sortby_index]
    mixed_case_fields = ['serverId']
    pt = prettytable.PrettyTable([f for f in fields], caching=False)
    pt.align = 'l'

    for o in objs:
        row = []
        for field in fields:
            if field in formatters:
                row.append(formatters[field](o))
            else:
                if field in mixed_case_fields:
                    field_name = field.replace(' ', '_')
                # else:
                # field_name = field.lower().replace(' ', '_')
                field_name = field
                data = o.get(field_name, '')
                if data is None:
                    data = '-'
                row.append(data)
        pt.add_row(row)

    if sortby is not None:
        result = pt.get_string(sortby=sortby)
    else:
        result = pt.get_string()

    if six.PY3:
        result = result.decode()

    print(result)

