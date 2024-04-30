from datetime import timedelta

from events.models import Event


def event_overlap(self, form, current_event):
    is_cyclic = form.cleaned_data['is_cyclic']
    facility_events = Event.objects.filter(facility=form.cleaned_data['facility'])

    for event in facility_events:
        if event == current_event:
            continue

        start_datetime = form.cleaned_data['start_datetime']
        end_datetime = form.cleaned_data['end_datetime']

        event_start_datetime = event.start_datetime
        event_end_datetime = event.end_datetime

        if is_cyclic and start_datetime < event_end_datetime:
            day_diff = (event_end_datetime - start_datetime).days
            to_add = day_diff // 7 * 7
            start_datetime += timedelta(days=to_add)
            end_datetime += timedelta(days=to_add)

        if event.is_cyclic and event_start_datetime < end_datetime:
            day_diff = (end_datetime - event_start_datetime).days
            to_add = day_diff // 7 * 7
            event_start_datetime += timedelta(days=to_add)
            event_end_datetime += timedelta(days=to_add)

        if start_datetime < event_end_datetime and end_datetime > event_start_datetime:
            return True

    return False
