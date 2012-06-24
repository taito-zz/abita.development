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

    def get_record_rate(self):
        from zope.component import getUtility
        from plone.registry.interfaces import IRegistry
        registry = getUtility(IRegistry)
        return registry.records.get('abita.development.rate')

    def test_registry_record__rate__field__instance(self):
        record = self.get_record_rate()
        from plone.registry.field import Float
        self.assertIsInstance(record.field, Float)

    def test_registry_record__rate__field__title(self):
        record = self.get_record_rate()
        self.assertEqual(record.field.title, u'Default Rate')

    def test_registry_record__rate__field__description(self):
        record = self.get_record_rate()
        self.assertEqual(record.field.description, u'Default rate per 10 minutes.')

    def test_registry_record__rate__value(self):
        record = self.get_record_rate()
        self.assertEqual(record.value, 6.0)

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

    def test_uninstall__registry_rate(self):
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        installer.uninstallProducts(['abita.development'])
        from zope.component import getUtility
        from plone.registry.interfaces import IRegistry
        registry = getUtility(IRegistry)
        self.assertRaises(
            KeyError,
            lambda: registry['abita.development.rate']
        )
