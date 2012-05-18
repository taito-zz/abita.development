from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from abita.development.tests.base import IntegrationTestCase

import mock


class TestDevelopmentWorkView(IntegrationTestCase):
    """TestCase testing DevelopmentWorkView class."""

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_templatedir(self):
        from abita.development.browser import template
        self.assertEqual(
            getattr(template, 'grokcore.view.directive.templatedir'),
            'templates'
        )

    def createFolder(self):
        folder = self.portal[
            self.portal.invokeFactory('Folder', 'folder')
        ]
        folder.reindexObject()
        return folder

    def createView(self):
        from abita.development.browser.template import DevelopmentWorkView
        from zope.publisher.browser import TestRequest
        return DevelopmentWorkView(self.createFolder(), TestRequest())

    def test_view__subclass(self):
        from abita.development.browser.template import DevelopmentWorkView
        from five import grok
        self.assertTrue(issubclass(DevelopmentWorkView, grok.View))

    def test_view__instance(self):
        from abita.development.browser.template import DevelopmentWorkView
        view = self.createView()
        self.assertTrue(isinstance(view, DevelopmentWorkView))

    def test_view__context(self):
        view = self.createView()
        from Products.ATContentTypes.interfaces.folder import IATFolder
        self.assertEqual(
            getattr(view, 'grokcore.component.directive.context'),
            IATFolder
        )

    def test_view__layer(self):
        view = self.createView()
        from abita.development.browser.interfaces import IAbitaDevelopmentLayer
        self.assertEqual(
            getattr(view, 'grokcore.view.directive.layer'),
            IAbitaDevelopmentLayer
        )

    def test_view__name(self):
        view = self.createView()
        self.assertEqual(
            getattr(view, 'grokcore.component.directive.name'),
            'development-work'
        )

    def test_view__require(self):
        view = self.createView()
        self.assertEqual(
            getattr(view, 'grokcore.security.directive.require'),
            ['cmf.ManagePortal']
        )

    def test_view__template(self):
        view = self.createView()
        self.assertEqual(
            getattr(view, 'grokcore.view.directive.template'),
            'development-work'
        )

    def test_view__total_time(self):
        view = self.createView()
        view.total_minutes = mock.Mock(return_value=30.0)
        self.assertEqual(
            view.total_time(),
            '30 minutes'
        )
