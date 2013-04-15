from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from abita.development.interfaces import IManageDevWork
from abita.development.interfaces import IRate
from plone.app.layout.viewlets.common import ViewletBase
from zope.annotation.interfaces import IAnnotations


class RatePerTenMinutesViewlet(ViewletBase):
    """Rate per ten minutes Viewlet Class."""

    index = ViewPageTemplateFile('viewlets/rate.pt')

    def update(self):
        super(RatePerTenMinutesViewlet, self).update()
        form = self.request.form
        if form.get('form.button.Update', None) is not None:
            try:
                rate = float(form.get('rate', ''))
                IAnnotations(self.context)['abita.development.rate'] = rate
                return self.render()
            except ValueError:
                pass

    def available(self):
        """Return True if the context provides IManageDevWork interface."""
        return IManageDevWork.providedBy(self.context)

    def rate(self):
        return IRate(self.context)()
