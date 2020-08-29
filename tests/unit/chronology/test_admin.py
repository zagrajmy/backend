# pylint: disable=redefined-outer-name,protected-access
from unittest.mock import Mock

import pytest
from django.utils.text import slugify

from chronology.admin import ProposalAdmin
from chronology.models import Proposal
from notice_board.models import Meeting
from tests.factories import MeetingFactory, ProposalFactory, SphereFactory, UserFactory


@pytest.fixture
def proposal_admin():
    return ProposalAdmin(model=Proposal, admin_site=Mock())


@pytest.fixture
def request_with_user():
    current_user = UserFactory()
    request = Mock()
    request.user = current_user
    return request


@pytest.mark.django_db
def test_accept_proposals(proposal_admin, request_with_user):
    proposals = []
    for i in range(10):
        proposal = ProposalFactory()
        if i % 2 == 0:
            proposal.meeting = None
            proposal.save()
            proposals.append(proposal)

    proposal_admin.accept_proposals(
        request=request_with_user, queryset=Proposal.objects.order_by("id")
    )

    for proposal in Proposal.objects.filter(id__in=[p.id for p in proposals]):
        _assert_new_meeting(proposal)
    request_with_user._messages.add.assert_called_once_with(
        20, "Total processed: 10, accepted: 5", ""
    )


@pytest.mark.django_db
def test_accept_proposals_default_user(proposal_admin, request_with_user):
    proposal = ProposalFactory(meeting=None, speaker_user=None)

    proposal_admin.accept_proposals(
        request=request_with_user, queryset=Proposal.objects.order_by("id")
    )

    proposal = Proposal.objects.last()
    _assert_new_meeting(proposal, organizer=request_with_user.user)


@pytest.mark.django_db
def test_accept_proposals_duplicate_slug(proposal_admin, request_with_user):
    sphere = SphereFactory()
    MeetingFactory(slug="slug-123", sphere=sphere)

    proposal = ProposalFactory(
        meeting=None,
        name="Slug 123",
        waitlist__festival__sphere=sphere,
    )

    proposal_admin.accept_proposals(
        request=request_with_user, queryset=Proposal.objects.order_by("id")
    )

    proposal = Proposal.objects.last()
    _assert_new_meeting(proposal, slug="slug-123-1")


@pytest.mark.django_db
def test_accept_proposals_duplicate_slug_cutting(proposal_admin, request_with_user):
    proposal = ProposalFactory(meeting=None, name="q" * 56)

    proposal_admin.accept_proposals(
        request=request_with_user, queryset=Proposal.objects.order_by("id")
    )

    proposal = Proposal.objects.last()
    _assert_new_meeting(proposal, slug="q" * 48)


@pytest.mark.django_db
def test_accept_proposals_duplicate_slug_cutting_duplicate(
    proposal_admin, request_with_user
):
    sphere = SphereFactory()
    MeetingFactory(slug="q" * 48, sphere=sphere)

    proposal = ProposalFactory(
        meeting=None,
        name="q" * 56,
        waitlist__festival__sphere=sphere,
    )

    proposal_admin.accept_proposals(
        request=request_with_user, queryset=Proposal.objects.order_by("id")
    )

    proposal = Proposal.objects.last()
    _assert_new_meeting(proposal, slug="q" * 48 + "-1")


def _assert_new_meeting(proposal, **kwargs):
    meeting = Meeting.objects.get(name=proposal.name)
    assert meeting.description == proposal.description
    assert proposal.meeting == meeting
    assert meeting.name == proposal.name
    assert meeting.organizer == kwargs.get("organizer", proposal.speaker_user)
    assert meeting.publication_time == proposal.waitlist.festival.start_publication
    assert meeting.slug == kwargs.get("slug", slugify(proposal.name)[:48])
    assert meeting.sphere == proposal.waitlist.festival.sphere
