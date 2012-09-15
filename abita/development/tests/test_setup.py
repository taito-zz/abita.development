from Products.CMFCore.utils import getToolByName
from abita.development.tests.base import IntegrationTestCase


class TestCase(IntegrationTestCase):
    """TestCase for Plone setup."""

    def setUp(self):
        self.portal = self.layer['portal']

    def test_is_abita_development_installed(self):
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        self.failUnless(installer.isProductInstalled('abita.development'))

    def test_actions__object_buttons__manage_dev_work__title(self):
        actions = getToolByName(self.portal, 'portal_actions')
        action = getattr(actions, 'object_buttons').manage_dev_work
        self.assertEqual(action.title, 'Manage Development Work')

    def test_actions__object_buttons__manage_dev_work__description(self):
        actions = getToolByName(self.portal, 'portal_actions')
        action = getattr(actions, 'object_buttons').manage_dev_work
        self.assertEqual(action.description, 'Manage amount of development work.')

    def test_actions__object_buttons__manage_dev_work__url_expr(self):
        actions = getToolByName(self.portal, 'portal_actions')
        action = getattr(actions, 'object_buttons').manage_dev_work
        self.assertEqual(
            action.getProperty('url_expr'),
            'string:${globals_view/getCurrentObjectUrl}/@@manage-dev-work')

    def test_actions__object_buttons__manage_dev_work__available_expr(self):
        actions = getToolByName(self.portal, 'portal_actions')
        action = getattr(actions, 'object_buttons').manage_dev_work
        self.assertEqual(
            action.getProperty('available_expr'),
            'python: object.restrictedTraverse("is-dev-work-unmanaged")()')

    def test_actions__object_buttons__manage_dev_work__permissions(self):
        actions = getToolByName(self.portal, 'portal_actions')
        action = getattr(actions, 'object_buttons').manage_dev_work
        self.assertEqual(action.getProperty('permissions'), ('Manage portal',))

    def test_actions__object_buttons__manage_dev_work__visible(self):
        actions = getToolByName(self.portal, 'portal_actions')
        action = getattr(actions, 'object_buttons').manage_dev_work
        self.assertTrue(action.getProperty('visible'))

    def test_actions__object_buttons__unmanage_dev_work__title(self):
        actions = getToolByName(self.portal, 'portal_actions')
        action = getattr(actions, 'object_buttons').unmanage_dev_work
        self.assertEqual(action.title, 'Unmanage Development Work')

    def test_actions__object_buttons__unmanage_dev_work__description(self):
        actions = getToolByName(self.portal, 'portal_actions')
        action = getattr(actions, 'object_buttons').unmanage_dev_work
        self.assertEqual(action.description, 'Unmanage amount of development work.')

    def test_actions__object_buttons__unmanage_dev_work__url_expr(self):
        actions = getToolByName(self.portal, 'portal_actions')
        action = getattr(actions, 'object_buttons').unmanage_dev_work
        self.assertEqual(
            action.getProperty('url_expr'),
            'string:${globals_view/getCurrentObjectUrl}/@@unmanage-dev-work')

    def test_actions__object_buttons__unmanage_dev_work__available_expr(self):
        actions = getToolByName(self.portal, 'portal_actions')
        action = getattr(actions, 'object_buttons').unmanage_dev_work
        self.assertEqual(
            action.getProperty('available_expr'),
            'python: object.restrictedTraverse("is-dev-work-managed")()')

    def test_actions__object_buttons__unmanage_dev_work__permissions(self):
        actions = getToolByName(self.portal, 'portal_actions')
        action = getattr(actions, 'object_buttons').unmanage_dev_work
        self.assertEqual(action.getProperty('permissions'), ('Manage portal',))

    def test_actions__object_buttons__unmanage_dev_work__visible(self):
        actions = getToolByName(self.portal, 'portal_actions')
        action = getattr(actions, 'object_buttons').unmanage_dev_work
        self.assertTrue(action.getProperty('visible'))

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

    def test_uninstall__actions__object_buttons__manage_dev_work(self):
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        installer.uninstallProducts(['abita.development'])
        actions = getToolByName(self.portal, 'portal_actions')
        self.assertRaises(
            AttributeError, lambda: getattr(actions, 'object_buttons').manage_dev_work)

    def test_uninstall__actions__object_buttons__unmanage_dev_work(self):
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        installer.uninstallProducts(['abita.development'])
        actions = getToolByName(self.portal, 'portal_actions')
        self.assertRaises(
            AttributeError, lambda: getattr(actions, 'object_buttons').unmanage_dev_work)

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
