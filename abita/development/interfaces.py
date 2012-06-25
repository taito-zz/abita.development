from zope.interface import Interface


class IManageDevWork(Interface):
    """Marker interface to imply that folder is in managing dev work."""


class IRate(Interface):
    """Adapter interface to IATFolder"""

    def __call__():
        """Returns rate."""
