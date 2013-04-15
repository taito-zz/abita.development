from abita.development.tests.base import IntegrationTestCase
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

import mock


class TestDevelopmentWorkView(IntegrationTestCase):
    """TestCase testing DevelopmentWorkView class."""

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def createFolder(self):
        folder = self.portal[self.portal.invokeFactory('Folder', 'folder')]
        folder.reindexObject()
        return folder

    def createView(self):
        from abita.development.browser.template import DevelopmentWorkView
        from zope.publisher.browser import TestRequest
        return DevelopmentWorkView(self.createFolder(), TestRequest())

    def test_view__subclass(self):
        from abita.development.browser.template import DevelopmentWorkView
        from Products.Five.browser import BrowserView
        self.assertTrue(issubclass(DevelopmentWorkView, BrowserView))

    def test_view__instance(self):
        from abita.development.browser.template import DevelopmentWorkView
        view = self.createView()
        self.assertTrue(isinstance(view, DevelopmentWorkView))

    def test_view__total_time(self):
        view = self.createView()
        view.total_minutes = mock.Mock(return_value=30.0)
        self.assertEqual(view.total_time(), '30 minutes')
