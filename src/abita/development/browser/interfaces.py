from collective.base.interfaces import IBaseView
from collective.base.interfaces import IViewlet
from zope.interface import Interface


class IAbitaDevelopmentLayer(Interface):
    """Marker interface for browserlayer."""


class IRatePerTenMinutesViewlet(IViewlet):
    """Viewlet interface"""

    def available():
        """Return True if the context provides IManageDevWork interface"""

    def rate():
        """Return rate"""


class IDevelopmentWorkView(IBaseView):
    """View interface"""
