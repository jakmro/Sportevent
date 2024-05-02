from datetime import timedelta
from events.models import Event


def event_overlap(form, current_event):
    repeat_every_n_days = form.cleaned_data['repeat_every_n_days']
    facility_events = Event.objects.filter(facility=form.cleaned_data['facility'])

    for event in facility_events:
        if event == current_event:
            continue

        start_datetime = form.cleaned_data['start_datetime']
        end_datetime = form.cleaned_data['end_datetime']

        event_start_datetime = event.start_datetime
        event_end_datetime = event.end_datetime

        if repeat_every_n_days and start_datetime < event_end_datetime:
            day_diff = (event_end_datetime - start_datetime).days
            to_add = day_diff // repeat_every_n_days * repeat_every_n_days
            start_datetime += timedelta(days=to_add)
            end_datetime += timedelta(days=to_add)

        if event.repeat_every_n_days and event_start_datetime < end_datetime:
            day_diff = (end_datetime - event_start_datetime).days
            to_add = day_diff // event.repeat_every_n_days * event.repeat_every_n_days
            event_start_datetime += timedelta(days=to_add)
            event_end_datetime += timedelta(days=to_add)

        if start_datetime < event_end_datetime and end_datetime > event_start_datetime:
            return True

        if repeat_every_n_days and event.repeat_every_n_days:
            diff_tracker = set()

            while True:
                diff = start_datetime - event_start_datetime

                if diff in diff_tracker:
                    return False

                diff_tracker.add(diff)

                if start_datetime < event_start_datetime:
                    start_datetime += timedelta(days=repeat_every_n_days)
                    end_datetime += timedelta(days=repeat_every_n_days)
                else:
                    event_start_datetime += timedelta(days=event.repeat_every_n_days)
                    event_end_datetime += timedelta(days=event.repeat_every_n_days)

                if start_datetime < event_end_datetime and end_datetime > event_start_datetime:
                    return True

    return False
