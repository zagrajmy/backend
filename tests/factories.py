import factory
from django.contrib.sites.models import Site
from django.utils import timezone
from django.utils.timezone import get_default_timezone
from factory.django import DjangoModelFactory

from crowd.models import User
from notice_board.models import Guild, Meeting, Sphere

NOW = timezone.now()


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker("email")


class SiteFactory(DjangoModelFactory):
    class Meta:
        model = Site

    name = factory.Faker("dga")
    domain = factory.Faker("dga")


class SphereFactory(DjangoModelFactory):
    class Meta:
        model = Sphere

    name = "sphere"
    site = factory.SubFactory(SiteFactory)


class MeetingFactory(DjangoModelFactory):
    class Meta:
        model = Meeting

    organizer = factory.SubFactory(UserFactory)
    sphere = factory.SubFactory(SphereFactory)


class GuildFactory(DjangoModelFactory):
    class Meta:
        model = Guild

    name = "club"


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
    name = "festival"
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


class TimeSlotFactory(DjangoModelFactory):
    class Meta:
        model = "chronology.TimeSlot"

    festival = factory.SubFactory(FestivalFactory)
    start_time = factory.Faker(
        "date_time_between",
        start_date="+1d",
        end_date="+3d",
        tzinfo=get_default_timezone(),
    )
    end_time = factory.Faker(
        "date_time_between",
        start_date="+4d",
        end_date="+6d",
        tzinfo=get_default_timezone(),
    )


class HelperFactory(DjangoModelFactory):
    class Meta:
        model = "chronology.Helper"

    festival = factory.SubFactory(FestivalFactory)
    user = factory.SubFactory(UserFactory)


class WaitListFactory(DjangoModelFactory):
    class Meta:
        model = "chronology.WaitList"

    festival = factory.SubFactory(FestivalFactory)


class ProposalFactory(DjangoModelFactory):
    class Meta:
        model = "chronology.Proposal"

    city = factory.Faker("city")
    club = factory.Faker("city")
    description = factory.Faker("text")
    duration_minutes = factory.Faker("pyint", min_value=25)
    meeting = factory.SubFactory(MeetingFactory)
    name = factory.Faker("sentence")
    needs = factory.Faker("text")
    other_contact = factory.Faker("words")
    other_data = factory.Faker("text")
    phone = factory.Faker("phone_number")
    speaker_name = factory.Faker("name")
    speaker_user = factory.SubFactory(UserFactory)
    topic = factory.Faker("word")
    waitlist = factory.SubFactory(WaitListFactory)


class RoomFactory(DjangoModelFactory):
    class Meta:
        model = "chronology.Room"

    name = "Room21"
    festival = factory.SubFactory(FestivalFactory)


class AgendaItemFactory(DjangoModelFactory):
    class Meta:
        model = "chronology.AgendaItem"

    room = factory.SubFactory(RoomFactory)


FACTORIES = {
    "agendaitem": AgendaItemFactory,
    "festival": FestivalFactory,
    "guild": GuildFactory,
    "helper": HelperFactory,
    "meeting": MeetingFactory,
    "proposal": ProposalFactory,
    "room": RoomFactory,
    "sphere": SphereFactory,
    "timeslot": TimeSlotFactory,
    "user": UserFactory,
    "waitlist": WaitListFactory,
}
