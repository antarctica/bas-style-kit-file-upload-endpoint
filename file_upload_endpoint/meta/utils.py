from copy import deepcopy


def get_cerberus_schema(schema: dict) -> dict:
    """
    Generates a valid Cerberus validation schema from an application schema

    Cerberus is a Python validation library, http://docs.python-cerberus.org, it uses a schema mapping (dict) to define
    validation requirements. This mapping is validated against an internal schema defined by Cerberus, which does not
    allow additional keys/fields.

    To aid in reporting errors to end-users, this API requires some additional information about each validation
    requirement, such as where the 'field' is a request parameter, query parameter, header, body field, etc. As this
    information relates directly to each validation requirement they are added to the same validation schema.

    This extended schema is invalid when used with Cerberus due to the extra keys, therefore a version needs to be made
    without these additions. To prevent maintaining two schemas, this function creates a Cerberus compatible schema
    from an extended schema.

    :type schema: dict
    :param schema: Extended (application) validation schema

    :rtype dict
    :return: Cerberus compatible validation schema
    """
    cerberus_schema = deepcopy(schema)

    for field in schema.keys():
        del(cerberus_schema[field]['request_type'])

    return cerberus_schema
