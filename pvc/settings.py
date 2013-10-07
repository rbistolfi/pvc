# coding: utf-8


import os


MONGO_HOST = os.environ.get("mongo")
SERVER_NAME = os.environ.get("hostname")
URL_PREFIX = "api"
API_VERSION = "1"
RESOURCE_METHODS = ['GET', 'POST', 'DELETE']
ITEM_METHODS = ['GET', 'PATCH', 'DELETE']


package_schema = {
    # Schema definition, based on Cerberus grammar. Check the Cerberus project
    # (https://github.com/nicolaiarocci/cerberus) for details.
    'name': {
        'type': 'string',
        'minlength': 0,
        'maxlength': 100,
    },
    'description': {
        'type': 'string',
        'minlength': 0,
        'maxlength': 1000,
    },
    'category': {
        'type': 'string',
        'minlength': 0,
        'maxlength': 10,
    },
    'packages': {
        'type': 'list',
        'schema': {
            'arch': {
                'type': 'string',
                'minlength': 0,
                'maxlength': 10,
            },
            'build': {
                'type': 'string',
                'minlength': 0,
                'maxlength': 10,
            },
            'repository': {
                'type': 'string',
                'minlength': 0,
                'maxlength': 10,
            },
            'required': {
                'type': 'string',
                'minlength': 0,
                'maxlength': 10000,
            },
            'conflicts': {
                'type': 'string',
                'minlength': 0,
                'maxlength': 10000,
            },
            'suggests': {
                'type': 'string',
                'minlength': 0,
                'maxlength': 10000,
            },
            'release': {
                'type': 'string',
                'minlength': 0,
                'maxlength': 10,
            },
            'version': {
                'type': 'string',
                'minlength': 0,
                'maxlength': 10,
            },
            'filename': {
                'type': 'string',
                'minlength': 0,
                'maxlength': 100,
                'required': True,
            },
            'url': {
                'type': 'string',
                'minlength': 0,
                'maxlength': 1000,
            },
            'md5': {
                'type': 'string',
                'minlength': 0,
                'maxlength': 50,
            },
            'size compressed': {
                'type': 'string',
                'minlength': 0,
                'maxlength': 100,
            },
            'size uncompressed': {
                'type': 'string',
                'minlength': 0,
                'maxlength': 100,
            },
        }
    }
}


package = {
    # 'title' tag used in item links. Defaults to the resource title minus
    # the final, plural 's' (works fine in most cases but not for 'people')
    'item_title': 'package',

    # by default the standard item entry point is defined as
    # '/people/<ObjectId>/'. We leave it untouched, and we also enable an
    # additional read-only entry point. This way consumers can also perform
    # GET requests at '/package/<lastname>/'.
    'additional_lookup': {
        'url': '[\w]+',
        'field': 'name'
    },

    # We choose to override global cache-control directives for this resource.
    'cache_control': 'max-age=10,must-revalidate',
    'cache_expires': 10,

    # most global settings can be overridden at resource level
    'resource_methods': ['GET', 'POST', 'DELETE'],

    'schema': package_schema
}


DOMAIN = {
    'package': package,
}
