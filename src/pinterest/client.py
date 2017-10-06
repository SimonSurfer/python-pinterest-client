import importlib
import requests
import warnings
import logging
import urllib
import re


class PintClient(object):
    API_BASEURL = 'https://api.pinterest.com'

    def __init__(self, access_token, version='1'):
        self.access_token = access_token
        self.version = version
        self.spec = self._get_spec()
        self.logger = logging.getLogger('pinterest.client')

    def __getattr__(self, item):
        if item not in ['boards', 'pins', 'users']:
            raise ValueError('%s is not a valid namespace' % item)

        return type(''.join(['Pint', item.title()]), (PintNamespace,), {})(self, item)

    @property
    def endpoint(self):
        return '{base}/v{version}'.format(
            base=self.API_BASEURL,
            version=self.version,
        )

    @property
    def me(self):
        return PintMe(PintNamespace(self, 'me'), '')

    def _get_spec(self):
        try:
            return importlib.import_module('pinterest.spec.v{version}'.format(version=self.version))
        except ImportError:
            warnings.warn('API specification does not exist: %s' % self.version, ImportWarning)
            return {}

    def req(self, resource, method='get', payload=None, returning=None, **kwargs):
        urlparams = {
            'access_token': self.access_token,
            'fields': ','.join(returning or ['id'])
        }
        if method == 'get':
            kwargs.update({
                'params': payload
            })
        else:
            kwargs.update({
                'json': payload
            })

        request_url = '{endpoint}/{resource}'.format(endpoint=self.endpoint, resource=resource)
        self.logger.debug('Making request: %s', request_url)
        response = requests.request(
            method=method,
            url=request_url + '?{params}'.format(params=urllib.urlencode(urlparams)),
            **kwargs
        )
        if not response.ok:
            raise RuntimeError('Api request failed [%s], %s' % (response.status_code, response.content))

        self.logger.debug('Request successful: %s', response.json())
        return response.json().get('data', {})


class PintNamespace(object):

    def __init__(self, client, slug, name=None):
        self.client = client
        self.slug = slug
        self.name = name or slug.title()
        self._meta = getattr(self.client.spec, self.slug.upper())
        self.logger = logging.getLogger('pinterest.ns.{namespace}'.format(namespace=self.slug))

    @property
    def singular(self):
        return re.sub(r's$', '', self.name)

    def create(self, **data):
        data = self._req(resource=self.slug+'/', method='post', payload=data)
        self.logger.info('%s created', self.name)
        return self._make_object(**data)

    def get(self, id):
        self.logger.debug('Retrieving %s[%s]', self.name, id)
        return PintObject(self, id).fetch()

    def _req(self, resource, method='get', payload=None):
        return self.client.req(resource=resource, method=method, payload=payload, returning=self._get_fields())

    def _get_fields(self):
        return getattr(self.client.spec, self.slug.upper()).get('fields')

    def _make_object(self, **data):
        return PintObject(self, data.get('id'), **data)


class PintObject(object):

    def __init__(self, namespace, uid, **attributes):
        self.namespace = namespace
        self.uid = uid
        self.logger = logging.getLogger('pinterest.ns.{namespace}.object'.format(
            namespace=self.namespace.slug
        ))
        for attribute, value in attributes.items():
            setattr(self, attribute, value)
            self.logger.debug('Attribute %s set to: %s', attribute, value)

    def __repr__(self):
        return '<{name}:{id}>'.format(name=self.namespace.singular, id=self.id)

    def __getattr__(self, item):
        if item.startswith('get_'):
            l = item[len('get_'):]
            if l not in self.namespace._meta.get('lists'):
                raise ValueError('%s has no list %s', self, l)

            return lambda: self.client.req('{resource_uri}/{sublist}'.format(
                resource_uri=self.resource_uri,
                sublist=l),
            )

    @property
    def resource_uri(self):
        return '{ns}/{uid}'.format(ns=self.namespace.slug, uid=self.uid).rstrip('/')

    @property
    def client(self):
        return self.namespace.client

    def fetch(self):
        for attribute, value in self.client.req(self.resource_uri, returning=self.namespace._get_fields()).items():
            setattr(self, attribute, value)

        return self

    def update(self, **kwargs):
        raise NotImplemented('Update is not yet supported. Please check later')

    def delete(self):
        raise NotImplemented('Delete is not yet supported. Please check later')


class PintMe(PintObject):
    pass
