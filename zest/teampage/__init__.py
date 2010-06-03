from Products.Archetypes import atapi
from Products.CMFCore.permissions import AddPortalContent
from Products.CMFCore import utils as cmfutils

from zope.i18nmessageid import MessageFactory

from config import PROJECTNAME

ZestTeamPageMessageFactory = MessageFactory(u'zest.teampage')


def initialize(context):
    """Intializer called when used as a Zope 2 product."""
    # imports packages and types for registration
    import content

    # Initialize portal content
    content_types, constructors, ftis = atapi.process_types(
        atapi.listTypes(PROJECTNAME),
        PROJECTNAME)

    cmfutils.ContentInit(
        PROJECTNAME + ' Content',
        content_types=content_types,
        permission=AddPortalContent,
        extra_constructors=constructors,
        fti=ftis,
        ).initialize(context)
