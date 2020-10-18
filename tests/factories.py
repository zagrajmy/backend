from datetime import timedelta
from math import ceil

import factory
from django.contrib.sites.models import Site
from django.utils import timezone
from django.utils.timezone import get_default_timezone
from factory.django import DjangoModelFactory

from chronology.models import Proposal, TimeSlot
from crowd.models import User
from notice_board.models import Guild, Meeting, Sphere

NOW = timezone.now()


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    auth0_id = factory.Faker("md5")
    date_joined = factory.Faker(
        "date_time_between",
        start_date="-100d",
        end_date="-50d",
        tzinfo=get_default_timezone(),
    )
    email = factory.Faker("email")
    first_name = factory.Faker("first_name")
    is_active = True
    is_staff = False
    is_superuser = False
    last_login = factory.Faker(
        "date_time_between",
        start_date="-7d",
        end_date="-1d",
        tzinfo=get_default_timezone(),
    )
    last_name = factory.Faker("last_name")
    locale = "pl"
    password = factory.Faker("password")
    username = factory.Faker("email")


class SiteFactory(DjangoModelFactory):
    class Meta:
        model = Site

    name = factory.Faker("dga")
    domain = factory.Faker("dga")


class SphereFactory(DjangoModelFactory):
    class Meta:
        model = Sphere

    is_open = factory.Faker("boolean")
    name = factory.Faker("text", max_nb_chars=10)
    site = factory.SubFactory(SiteFactory)


class MeetingFactory(DjangoModelFactory):
    class Meta:
        model = Meeting

    description = factory.Faker("text")
    end_time = factory.Faker(
        "date_time_between",
        start_date="+6d",
        end_date="+7d",
        tzinfo=get_default_timezone(),
    )
    location = factory.Faker("city")
    meeting_url = factory.Faker("url")
    name = factory.Faker("text", max_nb_chars=20)
    organizer = factory.SubFactory(UserFactory)
    publication_time = factory.Faker(
        "date_time_between",
        start_date="+2d",
        end_date="+3d",
        tzinfo=get_default_timezone(),
    )
    sphere = factory.SubFactory(SphereFactory)
    start_time = factory.Faker(
        "date_time_between",
        start_date="+4d",
        end_date="+5d",
        tzinfo=get_default_timezone(),
    )


class GuildFactory(DjangoModelFactory):
    class Meta:
        model = Guild

    description = factory.Faker("text")
    name = factory.Faker("text", max_nb_chars=20)
    is_public = factory.Faker("boolean")


class FestivalFactory(DjangoModelFactory):
    class Meta:
        model = "chronology.Festival"

    sphere = factory.SubFactory(SphereFactory)
    end_time = factory.Faker(
        "date_time_between",
        start_date="+10d",
        end_date="+12d",
        tzinfo=get_default_timezone(),
    )
    name = factory.Faker("text", max_nb_chars=20)
    start_proposal = factory.Faker(
        "date_time_between",
        start_date="+1d",
        end_date="+3d",
        tzinfo=get_default_timezone(),
    )
    end_proposal = factory.Faker(
        "date_time_between",
        start_date="+3d",
        end_date="+7d",
        tzinfo=get_default_timezone(),
    )
    start_publication = factory.Faker(
        "date_time_between",
        start_date="+4d",
        end_date="+6d",
        tzinfo=get_default_timezone(),
    )
    start_time = factory.Faker(
        "date_time_between",
        start_date="+7d",
        end_date="+9d",
        tzinfo=get_default_timezone(),
    )
    slug = factory.Faker("slug")

    @classmethod
    def _after_postgeneration(cls, instance, create, results=None):
        start, end = instance.start_time, instance.end_time
        if start and end:
            time_slots_count = max(ceil((end - start).seconds / (60 * 240)), 1)

            for i in range(time_slots_count):
                time_slot = TimeSlot.objects.create(
                    festival=instance,
                    start_time=start + timedelta(minutes=i * 240),
                    end_time=start + timedelta(minutes=(i + 1) * 240),
                )
            if time_slot.end_time != end:
                time_slot.end_time = end
                time_slot.save()


class HelperFactory(DjangoModelFactory):
    class Meta:
        model = "chronology.Helper"

    festival = factory.SubFactory(FestivalFactory)
    user = factory.SubFactory(UserFactory)


class WaitListFactory(DjangoModelFactory):
    class Meta:
        model = "chronology.WaitList"

    festival = factory.SubFactory(FestivalFactory)
    name = factory.Faker("text", max_nb_chars=10)
    slug = factory.Faker("slug")


class ProposalFactory(DjangoModelFactory):
    class Meta:
        model = "chronology.Proposal"

    city = factory.Faker("city")
    club = factory.Faker("city")
    description = factory.Faker("text")
    duration_minutes = factory.Faker("pyint", min_value=1, max_value=8)
    meeting = factory.SubFactory(MeetingFactory)
    name = factory.Faker("text", max_nb_chars=20)
    needs = factory.Faker("text")
    phone = factory.Faker("phone_number")
    speaker_name = factory.Faker("name")
    speaker_user = factory.SubFactory(UserFactory)
    topic = factory.Faker("text", max_nb_chars=15)
    waitlist = factory.SubFactory(WaitListFactory)

    @classmethod
    def _adjust_kwargs(cls, **kwargs):
        kwargs["duration_minutes"] *= 30
        return kwargs

    @classmethod
    def _after_postgeneration(cls, instance, create, results=None):
        if not instance.time_slots.count():
            festival = instance.waitlist.festival

            instance.time_slots.add(festival.time_slots.first())


class RoomFactory(DjangoModelFactory):
    class Meta:
        model = "chronology.Room"

    name = factory.Faker("text", max_nb_chars=10)
    festival = factory.SubFactory(FestivalFactory)
    slug = factory.Faker("slug")


class AgendaItemFactory(DjangoModelFactory):
    class Meta:
        model = "chronology.AgendaItem"

    room = factory.SubFactory(RoomFactory)
    meeting = factory.SubFactory(MeetingFactory)

    @classmethod
    def _adjust_kwargs(cls, **kwargs):
        try:
            kwargs["meeting"].proposal
        except Proposal.DoesNotExist:
            kwargs["meeting"].proposal = ProposalFactory(
                waitlist__festival=kwargs["room"].festival, meeting=kwargs["meeting"]
            )
            kwargs["meeting"].save()
        return kwargs


FACTORIES = {
    "agendaitem": AgendaItemFactory,
    "festival": FestivalFactory,
    "guild": GuildFactory,
    "helper": HelperFactory,
    "meeting": MeetingFactory,
    "proposal": ProposalFactory,
    "room": RoomFactory,
    "sphere": SphereFactory,
    "user": UserFactory,
    "waitlist": WaitListFactory,
}
