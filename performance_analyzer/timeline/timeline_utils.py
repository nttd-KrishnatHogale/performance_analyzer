def print_event(event):

    print("=" * 60)

    print(event.component)

    print(event.metric)

    print(event.start_time)

    print(event.peak_time)

    print(event.recovery_time)

    print(event.peak_value)

    print(event.duration_seconds)