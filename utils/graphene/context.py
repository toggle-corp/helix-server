from django.utils.functional import cached_property

from apps.event.dataloaders import EventReviewCountLoader
from apps.crisis.dataloaders import CrisisReviewCountLoader


class GQLContext:
    def __init__(self, request):
        self.request = request

    @cached_property
    def user(self):
        return self.request.user

    @cached_property
    def event_event_review_count_dataloader(self):
        return EventReviewCountLoader()

    @cached_property
    def crisis_crisis_review_count_dataloader(self):
        return CrisisReviewCountLoader()
