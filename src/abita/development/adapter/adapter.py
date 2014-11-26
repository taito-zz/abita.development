from collective.base.adapter import Adapter
from plone.registry.interfaces import IRegistry
from zope.annotation.interfaces import IAnnotations
from zope.component import getUtility


class Rate(Adapter):

    def __call__(self):
        registry = getUtility(IRegistry)
        name = 'abita.development.rate'
        annotations = IAnnotations(self.context).get(name)
        if annotations:
            return annotations
        else:
            return registry[name]
