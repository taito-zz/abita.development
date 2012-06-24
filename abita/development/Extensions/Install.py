from Products.CMFCore.utils import getToolByName


def uninstall(self):

    setup_tool = getToolByName(self, 'portal_setup')
    setup_tool.runAllImportStepsFromProfile(
        'profile-abita.development:uninstall'
    )
    setup_tool.setBaselineContext('profile-Products.CMFPlone:plone')
    return "Ran all uninstall steps."
