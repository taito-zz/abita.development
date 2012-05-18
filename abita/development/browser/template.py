from Acquisition import aq_inner
from Products.ATContentTypes.interfaces.document import IATDocument
from Products.ATContentTypes.interfaces.event import IATEvent
from Products.ATContentTypes.interfaces.folder import IATFolder
from Products.CMFCore.utils import getToolByName
from abita.development.browser.interfaces import IAbitaDevelopmentLayer
from datetime import timedelta
from decimal import Decimal
from decimal import ROUND_HALF_UP
from five import grok
from plone.app.contentlisting.interfaces import IContentListing
from zope.component import getMultiAdapter


grok.templatedir('templates')


class DevelopmentWorkView(grok.View):

    grok.context(IATFolder)
    grok.layer(IAbitaDevelopmentLayer)
    grok.name('development-work')
    grok.require('cmf.ManagePortal')
    grok.template('development-work')

    def items(self):
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        query = {
            'path': {
                'depth': 1,
                'query': '/'.join(context.getPhysicalPath()),
            },
            'object_provides': [
                IATEvent.__identifier__,
            ],
            'sort_on': 'end',
            'sort_order': 'descending',
        }
        ploneview = getMultiAdapter(
            (context, self.request),
            name=u'plone'
        )
        res = []
        for item in IContentListing(catalog(query)):
            difference = timedelta(item.end - item.start)
            days = difference.days
            minutes = days * 24 * 60
            seconds = difference.seconds
            if seconds:
                minutes += seconds / 60
            res.append(
                {
                    'title': item.Title(),
                    'description': item.Description(),
                    'start': ploneview.toLocalizedTime(item.start, long_format=True),
                    'end': ploneview.toLocalizedTime(item.end, long_format=True),
                    'duration': int(minutes),
                }
            )
        return res

    def total_minutes(self):
        minutes = 0.0
        for item in self.items():
            minutes += item['duration']
        return minutes

    def total_time(self):
        hours = int(self.total_minutes() // 60)
        minutes = int((self.total_minutes() / 60 - hours) * 60)
        if hours:
            return '{0} hours {1} minutes'.format(hours, minutes)
        else:
            return '{0} minutes'.format(minutes)

    def total_without_alv(self):
        price = self.total_minutes() * 5 / 10
        return self.pricing(price)

    def total_alv(self):
        price = self.total_minutes() * 5 / 10 * 0.23
        return self.pricing(price)

    def total_with_alv(self):
        price = self.total_minutes() * 5 / 10 * 1.23
        return self.pricing(price)

    def pricing(self, price):
        price = Decimal(str(price)).quantize(Decimal('.001'), rounding=ROUND_HALF_UP)
        price = Decimal(price).quantize(Decimal('.01'), rounding=ROUND_HALF_UP)
        return '{0} EUR'.format(price)
