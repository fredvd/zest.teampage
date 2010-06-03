"""
Product to present teammembers on homepage

$Id: teammember.py 37606 2010-06-03 12:08:13Z maurits $
"""

__authors__ = """Joris Slob <j.slob@zestsoftware.nl>,
                 Mark van Lent <m.vanlent@zestsoftware.nl>""",
__docformat__ = 'text/restructured'
__revision__ = "$Revision: 37606 $"

from DateTime import DateTime
from zope.interface import implements

from Products.ATContentTypes.content.schemata import ATContentTypeSchema
from Products.ATContentTypes.content.base import ATCTContent

from zest.teampage.interfaces import ITeamMember
from zest.teampage.config import PROJECTNAME

from zest.teampage import ZestTeamPageMessageFactory as _

try:
    from Products.LinguaPlone import public as atapi
except ImportError:
    # No multilingual support
    from Products.Archetypes import atapi

schema = ATContentTypeSchema.copy() + \
         atapi.Schema((
            atapi.StringField(
                name='surname',
                searchable=True,
                languageIndependent=True,
                widget=atapi.StringWidget(
                    label=_(u'label_surname', default=u'Surname'),
                )
            ),
            atapi.StringField(
                name='email',
                languageIndependent=True,
                widget=atapi.StringWidget(
                    label=_(u'label_email', default=u'Email'),
                )
            ),
            atapi.ImageField(
                name='portrait_intro',
                languageIndependent=True,
                schemata=u'pictures',
                original_size=(213, 135),
                sizes={'normal': (213, 135),
                         'thumb': (128, 128),
                         'portrait_intro': (213, 135)},
                widget=atapi.ImageWidget(
                    label=_(u'label_portrait_intro',
                        default=u'Introduction portrait'),
                    description=_(
                    u'help_portrait_intro',
                    default=u'Image used for the introduction portlet on ' +
                    u'the homepage. Image size should be 213 x 135 pixels.'),
                )
            ),
            atapi.ImageField(
                name='portrait',
                original_size=(512, 512),
                languageIndependent=True,
                schemata=u'pictures',
                sizes={'normal': (512, 512),
                         'thumb': (128, 128),
                         'portrait_small': (91, 64)},
                widget=atapi.ImageWidget(
                    label=_(u'label_portrait', default=u'Portrait'),
                    description=_(u'help_portrait',
                        default=u'Used in the team member listing. ' +
                                u'Image size should be 91 x 64 pixels.'),
                )
            ),
            atapi.ImageField(
                name='portrait_hover',
                original_size=(512, 512),
                languageIndependent=True,
                schemata=u'pictures',
                sizes={'normal': (512, 512),
                         'thumb': (128, 128),
                         'portrait_hover': (197, 295)},
                widget=atapi.ImageWidget(
                    label=_(u'label_portrait_hover',
                            default=u'Hover portrait'),
                    description=_(
                    u'help_portrait_hover',
                    default=u'Used in the team member listing for the ' +
                    u'large image when you hover over a team member. ' +
                    u'Image size should be 197 x 295 pixels.'),
                )
            ),
            atapi.ImageField(
                name='portrait_large',
                original_size=(512, 512),
                schemata=u'pictures',
                languageIndependent=True,
                sizes={'normal': (512, 512),
                         'thumb': (128, 128),
                         'portrait_large': (240, 360)},
                widget=atapi.ImageWidget(
                    label=_(u'label_portrait_large',
                            default=u'Large portrait'),
                    description=_(u'help_portrait_large',
                        default=u'Used in individual team member page as a ' +
                                u'large photo for every person. ' +
                                u'Image size should be 240 x 360 pixels.'),
                )
            ),
            atapi.StringField(
                name='function',
                searchable=True,
                widget=atapi.StringWidget(
                    label=_(u'label_function', default=u'Function'),
                )
            ),
            atapi.TextField(
                name='specialization',
                searchable=True,
                widget=atapi.TextAreaWidget(
                    label=_(u'label_specialization',
                              default=u'Specialization'),
                )
            ),
            atapi.DateTimeField(
                name='birthdate',
                languageIndependent=True,
                widget=atapi.CalendarWidget(
                    show_hm=False,
                    label=_(u'label_birthdate', default=u'Date of birth'),
                )
            ),
            atapi.TextField(
                name='personal',
                searchable=True,
                allowable_content_types=('text/plain',
                                         'text/structured',
                                         'text/html', ),
                widget=atapi.RichWidget(
                    allow_file_upload=False,
                    label=_(u'label_personal', default=u'Personal'),
                ),
                default_output_type='text/html',
            ),
            atapi.LinesField(
                name='hobbies',
                searchable=True,
                widget=atapi.LinesWidget(
                    label=_(u'label_hobbies', default=u'Hobbies'),
                    description=_(u'help_hobbies',
                                    default=u'Each hobby on a seperate line'),
                )
            ),
            atapi.StringField(
                'external_blog',
                required=False,
                searchable=False,
                widget=atapi.StringWidget(
                    label=_(u"label_external_blog", default=u"External Blog"),
                    description=_(
                    u"help_external_blog",
                    u"Fill in the URL to the RSS feed of your own blog")
                 ),
            ),
            atapi.StringField(
                'twitter_link',
                required=False,
                searchable=False,
                widget=atapi.StringWidget(
                    label=_(u"label_twitter_link", default=u"Twitter Link"),
                    description=_(u"help_twitter_link",
                                  u"Fill in the URL to your twitter page")
                 ),
             ),
            atapi.StringField(
                'linkedin_link',
                required=False,
                searchable=False,
                widget=atapi.StringWidget(
                    label=_(u"label_linkedin_link", default=u"LinkedIn Link"),
                    description=_(u"help_linkedin_link",
                                  u"Fill in the URL to your LinkedIn page")
                 ),
            ),
            atapi.BooleanField(
                name='freelance',
                languageIndependent=True,
                widget=atapi.BooleanWidget(
                    label=_(u'label_freelance', default=u'Freelance'),
                )
            ),
         ))

schema['title'].widget.label = _(u'label_firstname', default=u'First name')
schema['title'].languageIndependent = True
schema['description'].schemata = 'default'
schema['description'].widget.label = _(u'label_teammember_description',
    default=u'Introduction text')
schema['description'].widget.description = _(u'help_teammember_description',
    default=u'A short text meant as introduction.')
schema.moveField('portrait_intro', after='freelance')
schema.moveField('description', after='freelance')
schema['relatedItems'].schemata = 'metadata'


class TeamMember(ATCTContent):
    """
    """
    __implements__ = (ATCTContent.__implements__, )
    implements(ITeamMember)
    schema = schema
    _at_rename_after_creation = True

    def getAge(self):
        """Return the age of the team member."""
        birthdate = self.getBirthdate()
        if birthdate is None:
            return None
        today = DateTime()
        age = today.year() - birthdate.year()
        # Apply correction when before birthday.
        if (today.month() < birthdate.month() or
            (today.month() == birthdate.month() and
             today.day() < birthdate.day())):
            age = age - 1
        return age


atapi.registerType(TeamMember, PROJECTNAME)
