import factory
from django.utils import timezone

from crowd.models import User
from notice_board.models import Guild, Meeting, Sphere


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker("email")


class SphereFactory(factory.DjangoModelFactory):
    class Meta:
        model = Sphere

    name = "sphere"


class MeetingFactory(factory.DjangoModelFactory):
    class Meta:
        model = Meeting

    organizer = factory.SubFactory(UserFactory)
    sphere = factory.SubFactory(SphereFactory)


class GuildFactory(factory.DjangoModelFactory):
    class Meta:
        model = Guild

    name = "club"


class FestivalFactory(factory.DjangoModelFactory):
    class Meta:
        model = "chronology.Festival"

    sphere = factory.SubFactory(SphereFactory)
    end_time = timezone.now()
    name = "festival"
    start_proposal = timezone.now()
    start_publication = timezone.now()
    start_time = timezone.now()


class TimeSlotFactory(factory.DjangoModelFactory):
    class Meta:
        model = "chronology.TimeSlot"

    end_time = factory.Faker("date_time_this_century")
    festival = factory.SubFactory(FestivalFactory)
    start_time = factory.Faker("date_time_this_century")


class HelperFactory(factory.DjangoModelFactory):
    class Meta:
        model = "chronology.Helper"

    festival = factory.SubFactory(FestivalFactory)
    user = factory.SubFactory(UserFactory)


class WaitListFactory(factory.DjangoModelFactory):
    class Meta:
        model = "chronology.WaitList"

    festival = factory.SubFactory(FestivalFactory)


class ProposalFactory(factory.DjangoModelFactory):
    class Meta:
        model = "chronology.Proposal"

    city = factory.Faker("city")
    club = factory.Faker("city")
    meeting = factory.SubFactory(MeetingFactory)
    needs = factory.Faker("text")
    other_contact = factory.Faker("words")
    other_data = factory.Faker("text")
    phone = factory.Faker("phone_number")
    waitlist = factory.SubFactory(WaitListFactory)


class RoomFactory(factory.DjangoModelFactory):
    class Meta:
        model = "chronology.Room"

    name = "Room21"
    festival = factory.SubFactory(FestivalFactory)


class AgendaItemFactory(factory.DjangoModelFactory):
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
