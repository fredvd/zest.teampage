from zope.interface import Interface
from zope.viewlet.interfaces import IViewletManager


class ITeamMember(Interface):
    """Interface for TeamMember content type."""


class ITeamMemberView(Interface):
    """Interface for the TeamMember view."""

    def getFullName():
        """Return the full name of the team member."""

    def getAge():
        """Return the age of the team member."""

    def getHobbies():
        """Return the hobies of the team member."""

    def get_random_teammember():
        """Return the url of the introduction page of a random team member."""

    def get_image_tag(field):
        """Generatie image tag for ``field`` using api of the ImageField."""

    def get_zest_blog_items(author):
        """ This return an aggregated list of blog items from the Zest blog
        """


class ITeamMemberManager(IViewletManager):
    """A viewlet manager for the team member viewlet."""
