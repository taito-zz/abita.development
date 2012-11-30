from Products.CMFCore.utils import getToolByName

import logging

logger = logging.getLogger(__name__)

PROFILE_ID = 'profile-abita.development:default'


def reimport_registry(context):
    """Reimport registry"""
    setup = getToolByName(context, 'portal_setup')
    logger.info('Reimporting registry.')
    setup.runImportStepFromProfile(
        PROFILE_ID, 'plone.app.registry', run_dependencies=False, purge_old=False)
