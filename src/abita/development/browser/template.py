from Acquisition import aq_inner
from Products.ATContentTypes.interfaces.event import IATEvent
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from abita.development.interfaces import IRate
from datetime import timedelta
from decimal import Decimal
from decimal import ROUND_HALF_UP
from plone.app.contentlisting.interfaces import IContentListing
from plone.memoize.view import memoize
from plone.memoize.view import memoize_contextless
from plone.registry.interfaces import IRegistry
from zope.component import getUtility


class DevelopmentWorkView(BrowserView):
    """View for development work"""

    __call__ = ViewPageTemplateFile('templates/development-work.pt')

    def title(self):
        return self.context.Title()

    def description(self):
        return self.context.Description()

    @memoize
    def items(self):
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        query = {
            'path': {
                'depth': 1,
                'query': '/'.join(context.getPhysicalPath()),
            },
            'object_provides': [IATEvent.__identifier__, ],
            'sort_on': 'end',
            'sort_order': 'descending',
        }
        res = []
        toLocalizedTime = context.restrictedTraverse('@@plone').toLocalizedTime
        for item in IContentListing(catalog(query)):
            res.append({
                'title': item.Title(),
                'description': item.Description(),
                'url': item.getURL(),
                'date': toLocalizedTime(item.start),
                'start': toLocalizedTime(item.start, time_only=True),
                'end': toLocalizedTime(item.end, time_only=True),
                'duration': self.minutes(item),
            })
        return res

    @memoize
    def total_minutes(self):
        minutes = 0.0
        for item in self.items():
            minutes += item['duration']
        return minutes

    def total_time(self):
        hours = int(self.total_minutes() // 60)
        minutes = int((self.total_minutes() / 60 - hours) * 60)
        if hours:
            return '{} hours {} minutes'.format(hours, minutes)
        else:
            return '{} minutes'.format(minutes)

    def rate(self):
        return IRate(self.context)()

    def vat(self):
        return getUtility(IRegistry)['abita.development.vat']

    def total_without_vat(self):
        price = self.total_minutes() * self.rate() / 10
        return self.pricing(price)

    def total_vat(self):
        price = self.total_minutes() * self.rate() / 10 * self.vat() / 100
        return self.pricing(price)

    def total_with_vat(self):
        price = self.total_minutes() * self.rate() / 10 * (100.0 + self.vat()) / 100
        return self.pricing(price)

    @memoize_contextless
    def pricing(self, price):
        price = Decimal(
            str(price)).quantize(Decimal('.001'), rounding=ROUND_HALF_UP)
        price = Decimal(
            price).quantize(Decimal('.01'), rounding=ROUND_HALF_UP)
        return '{} EUR'.format(price)

    @memoize_contextless
    def minutes(self, item):
        difference = timedelta(item.end - item.start)
        total_seconds = difference.total_seconds()
        return int(total_seconds / 60)
