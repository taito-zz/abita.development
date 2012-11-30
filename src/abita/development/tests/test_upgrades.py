from abita.development.tests.base import IntegrationTestCase


class TestCase(IntegrationTestCase):
    """TestCase for upgrade steps."""

    def setUp(self):
        self.portal = self.layer['portal']

    def test_reimport_registry(self):
        from zope.component import getUtility
        from plone.registry.interfaces import IRegistry
        registry = getUtility(IRegistry)
        registry['abita.development.rate'] = 2.0
        del registry.records['abita.development.vat']

        self.assertEqual(registry['abita.development.rate'], 2.0)
        with self.assertRaises(KeyError):
            registry['abita.development.vat']

        from abita.development.upgrades import reimport_registry
        reimport_registry(self.portal)

        self.assertEqual(registry['abita.development.rate'], 7.0)
        self.assertEqual(registry['abita.development.vat'], 23.0)
