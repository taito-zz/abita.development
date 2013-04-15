from Products.ATContentTypes.interfaces.folder import IATFolder
from abita.development.interfaces import IRate
from plone.registry.interfaces import IRegistry
from zope.annotation.interfaces import IAnnotations
from zope.component import adapts
from zope.component import getUtility
from zope.interface import implements


class Rate(object):

    adapts(IATFolder)
    implements(IRate)

    def __init__(self, context):
        self.context = context

    def __call__(self):
        registry = getUtility(IRegistry)
        name = 'abita.development.rate'
        annotations = IAnnotations(self.context).get(name)
        if annotations:
            return annotations
        else:
            return registry[name]
