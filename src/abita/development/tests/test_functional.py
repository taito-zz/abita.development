from DateTime import DateTime
from Products.CMFCore.utils import getToolByName
from abita.development.tests.base import FUNCTIONAL_TESTING
from hexagonit.testing.browser import Browser
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.testing import layered
from zope.testing import renormalizing

import doctest
import manuel.codeblock
import manuel.doctest
import manuel.testing
import re
import transaction
import unittest

FLAGS = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
CHECKER = renormalizing.RENormalizing([
    # Normalize the generated UUID values to always compare equal.
    (re.compile(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'), '<UUID>'),
])


def setUp(self):
    layer = self.globs['layer']
    browser = Browser(layer['app'])
    portal = layer['portal']
    self.globs.update({
        'TEST_USER_NAME': TEST_USER_NAME,
        'TEST_USER_PASSWORD': TEST_USER_PASSWORD,
        'browser': browser,
        'portal': portal,
    })
    browser.setBaseUrl(portal.absolute_url())

    browser.handleErrors = True
    portal.error_log._ignored_exceptions = ()

    setRoles(portal, TEST_USER_ID, ['Manager'])

    folder = portal[portal.invokeFactory('Folder', 'folder', title='Folder',
        description="Description of Folder")]
    folder.reindexObject()
    self.globs['folder_url'] = folder.absolute_url()

    ids = [1, 2]
    for oid in ids:
        obj = folder[
            folder.invokeFactory(
                'Event',
                'event0{0}'.format(oid),
                title='Event0{0}'.format(oid),
                description='Description of Event0{0}'.format(oid),
                startDate=DateTime() + oid - 1,
                endDate=DateTime() + oid,
            )
        ]
        obj.reindexObject()
    event03 = folder[
        folder.invokeFactory(
            'Event',
            'event03',
            title='Event03',
            description='Description of Event03',
            startDate=DateTime('2012/5/6 10:30:00 am'),
            endDate=DateTime('2012/5/6 11:50:00 am'),
        )
    ]
    event03.reindexObject()

    user2 = 'test_user_2_'
    regtool = getToolByName(portal, 'portal_registration')
    regtool.addMember(user2, user2)
    setRoles(portal, user2, ['Site Administrator'])
    self.globs['user2'] = user2

    transaction.commit()


def DocFileSuite(testfile, flags=FLAGS, setUp=setUp, layer=FUNCTIONAL_TESTING):
    """Returns a test suite configured with a test layer.

    :param testfile: Path to a doctest file.
    :type testfile: str

    :param flags: Doctest test flags.
    :type flags: int

    :param setUp: Test set up function.
    :type setUp: callable

    :param layer: Test layer
    :type layer: object

    :rtype: `manuel.testing.TestSuite`
    """
    m = manuel.doctest.Manuel(optionflags=flags, checker=CHECKER)
    m += manuel.codeblock.Manuel()

    return layered(
        manuel.testing.TestSuite(m, testfile, setUp=setUp, globs=dict(layer=layer)),
        layer=layer)


def test_suite():
    return unittest.TestSuite([DocFileSuite('functional/browser.txt')])
