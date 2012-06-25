from Products.ATContentTypes.interfaces.folder import IATFolder
from abita.development.interfaces import IRate
from five import grok
from plone.registry.interfaces import IRegistry
from zope.annotation.interfaces import IAnnotations
from zope.component import getUtility


class Rate(grok.Adapter):

    grok.provides(IRate)
    grok.context(IATFolder)

    def __call__(self):
        registry = getUtility(IRegistry)
        name = 'abita.development.rate'
        annotations = IAnnotations(self.context).get(name)
        if annotations:
            return annotations
        else:
            return registry[name]