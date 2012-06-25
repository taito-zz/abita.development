from Products.ATContentTypes.interfaces.document import IATDocument
from Products.ATContentTypes.interfaces.event import IATEvent
from Products.ATContentTypes.interfaces.folder import IATFolder
from Products.Five.browser import BrowserView
from abita.development.interfaces import IManageDevWork
from zope.interface import alsoProvides
from zope.interface import noLongerProvides


class Miscellaneous(BrowserView):

    def manage_dev_work(self):
        alsoProvides(self.context, IManageDevWork)
        self.context.reindexObject(idxs=['object_provides'])
        self.context.setLayout('@@development-work')
        url = self.context.absolute_url()
        return self.request.response.redirect(url)

    def unmanage_dev_work(self):
        noLongerProvides(self.context, IManageDevWork)
        self.context.reindexObject(idxs=['object_provides'])
        url = self.context.absolute_url()
        return self.request.response.redirect(url)

    def is_dev_work_managed(self):
        return IATFolder.providedBy(self.context) and IManageDevWork.providedBy(self.context)

    def is_dev_work_unmanaged(self):
        return IATFolder.providedBy(self.context) and not IManageDevWork.providedBy(self.context)
