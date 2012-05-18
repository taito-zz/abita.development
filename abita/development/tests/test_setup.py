from abita.development.tests.base import IntegrationTestCase
from Products.CMFCore.utils import getToolByName


class TestCase(IntegrationTestCase):
    """TestCase for Plone setup."""

    def setUp(self):
        self.portal = self.layer['portal']

    def test_is_abita_development_installed(self):
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        self.failUnless(installer.isProductInstalled('abita.development'))

    def test_browserlayer(self):
        from abita.development.browser.interfaces import IAbitaDevelopmentLayer
        from plone.browserlayer import utils
        self.failUnless(IAbitaDevelopmentLayer in utils.registered_layers())

    def test_uninstall__package(self):
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        installer.uninstallProducts(['abita.development'])
        self.failIf(installer.isProductInstalled('abita.development'))

    def test_uninstall__browserlayer(self):
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        installer.uninstallProducts(['abita.development'])
        from abita.development.browser.interfaces import IAbitaDevelopmentLayer
        from plone.browserlayer import utils
        self.failIf(IAbitaDevelopmentLayer in utils.registered_layers())
