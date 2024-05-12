from django.utils import timezone
from datetime import timedelta
from .models import Event, Meeting


def validate_event_form(self, form):
    start_datetime = form.cleaned_data['start_datetime']
    end_datetime = form.cleaned_data['end_datetime']

    if start_datetime < timezone.now():
        form.add_error('start_datetime', 'Events cannot start in the past.')
        return self.form_invalid(form)

    if start_datetime > end_datetime:
        form.add_error('start_datetime', 'Start datetime must be less than or equal to End datetime.')
        return self.form_invalid(form)

    min_people_no = form.cleaned_data['min_people_no']
    max_people_no = form.cleaned_data['max_people_no']
    if min_people_no > max_people_no:
        form.add_error('min_people_no', 'Min people no must be less than or equal to Max people no.')
        return self.form_invalid(form)

    meeting_count = form.cleaned_data['meeting_count']
    repeat_every_n_days = form.cleaned_data['repeat_every_n_days']

    if meeting_count == 1 and repeat_every_n_days:
        form.add_error(
            'meeting_count',
            'Meeting count must be greater than 1 for an event to repeat.'
        )
        return self.form_invalid(form)

    if meeting_count > 1 and not repeat_every_n_days:
        form.add_error(
            'repeat_every_n_days',
            'Event must be repeating to satisfy the meeting count condition.'
        )
        return self.form_invalid(form)

    facility_events = Event.objects.filter(facility=form.cleaned_data['facility'])
    facility_meetings = Meeting.objects.filter(event__in=facility_events)

    start = start_datetime
    end = end_datetime

    for _ in range(meeting_count):
        for meeting in facility_meetings:
            if start < meeting.end_datetime and end > meeting.start_datetime:
                form.add_error(
                    None,
                    'There is already an event at this time at this place.'
                )
                return self.form_invalid(form)

        if repeat_every_n_days:
            start += timedelta(days=repeat_every_n_days)
            end += timedelta(days=repeat_every_n_days)


def add_meetings(self, form):
    start_datetime = form.cleaned_data['start_datetime']
    end_datetime = form.cleaned_data['end_datetime']
    meeting_count = form.cleaned_data['meeting_count']
    repeat_every_n_days = form.cleaned_data['repeat_every_n_days']

    start = start_datetime
    end = end_datetime

    for _ in range(meeting_count):
        Meeting.objects.create(event_id=self.object.id, start_datetime=start, end_datetime=end)
        if repeat_every_n_days:
            start += timedelta(days=repeat_every_n_days)
            end += timedelta(days=repeat_every_n_days)
