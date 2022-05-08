from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

PREFERENCE_MENSA = 1
PREFERENCE_FIRST_FLOOR = 2
PREFERENCE_NO_PREF = 0

PREFERENCES = (
    (PREFERENCE_MENSA, "Mensa"),
    (PREFERENCE_FIRST_FLOOR, "First Floor"),
    (PREFERENCE_NO_PREF, "No preference"),
)


class Exhibitor(models.Model):
    owner = models.ForeignKey(
        User, editable=False, related_name="exhibitors", on_delete=models.CASCADE
    )
    createDate = models.DateField(auto_now_add=True, editable=False)
    modifyDate = models.DateField(auto_now=True, editable=False)
    projectName = models.CharField(max_length=128, verbose_name=_("Project name"))
    logo = models.ImageField(
        blank=True, upload_to="exhibitors/logos", verbose_name=_("Project logo")
    )
    homepage = models.URLField(blank=True, verbose_name=_("Project homepage url"))

    descriptionDE = models.TextField(
        blank=True, verbose_name=_("Description text of your project (German)")
    )
    descriptionEN = models.TextField(
        blank=True, verbose_name=_("Description text of your project (English)")
    )

    boothPreferedLocation = models.PositiveIntegerField(
        choices=PREFERENCES,
        verbose_name=_("Do you have a preferred location for your booth?"),
        default=PREFERENCE_NO_PREF,
    )
    boothNumTables = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name=_("How many tables do you need (roughly 1.20m x 0.80m)?"),
    )
    boothNumChairs = models.PositiveIntegerField(
        blank=True, null=True, verbose_name=_("How many chairs do you need?")
    )
    boothComment = models.TextField(
        blank=True,
        verbose_name=_(
            "Here you have the chance to leave us further comments regarding your booth:"
        ),
    )

    participants = models.ManyToManyField(
        User,
        blank=True,
        editable=False,
        related_name="exhibitorparticipation",
        through="ExhibitorParticipants",
    )
    accepted = models.BooleanField(default=False, editable=False)

    year = models.PositiveIntegerField(
        editable=False, verbose_name=_("Conference year this exhibitor belongs to")
    )

    def has_read_permission(self, user):
        return (
            ExhibitorParticipants.objects.filter(user=user).count() > 0
            or user == self.owner
        )

    def has_write_permission(self, user):
        return (
            ExhibitorParticipants.objects.filter(user=user, isAdmin=True).count() > 0
            or user == self.owner
        )


class ExhibitorParticipants(models.Model):
    project = models.ForeignKey(Exhibitor, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    isAdmin = models.BooleanField(default=False)
