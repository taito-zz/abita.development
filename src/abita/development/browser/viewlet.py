from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from abita.development.browser.interfaces import IRatePerTenMinutesViewlet
from abita.development.interfaces import IManageDevWork
from abita.development.interfaces import IRate
from collective.base.viewlet import Viewlet
from zope.annotation.interfaces import IAnnotations
from zope.interface import implements


class RatePerTenMinutesViewlet(Viewlet):
    """Rate per ten minutes Viewlet Class."""
    implements(IRatePerTenMinutesViewlet)
    index = ViewPageTemplateFile('viewlets/rate.pt')

    def update(self):
        form = self.request.form
        if form.get('form.button.Update', None) is not None:
            try:
                rate = float(form.get('rate', ''))
                IAnnotations(self.context)['abita.development.rate'] = rate
                return self.render()
            except ValueError:
                pass

    def available(self):
        """Return True if the context provides IManageDevWork interface"""
        return IManageDevWork.providedBy(self.context)

    def rate(self):
        """Return rate"""
        return IRate(self.context)()
