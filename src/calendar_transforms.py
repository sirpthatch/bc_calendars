import click
import ics

bp_event_mapping = {
    "LS Monday-A":("Spanish/PE (A Week)","sneakers"),
    "LS Tuesday-A":("Swim (A Week)","swim suit"),
    "LS Wednesday-A":("Art/Spanish/Science (A Week)","art clothing"),
    "LS Thursday-A":("PE (A Week)","sneakers"),
    "LS Friday-A":("Dance/Spanish (A Week)","easy on/off shoes"),
    "LS Monday-B":("Art/Science (B Week)","art clothing"),
    "LS Tuesday-B":("Swim/Spanish (B Week)","swim suit"),
    "LS Wednesday-B":("Art/Science (B Week)","art clothing"),
    "LS Thursday-B":("PE (B Week)","sneakers"),
    "LS Friday-B":("Spanish/Dance (B Week)","easy on/off shoes")
}

miles_event_mapping = {
    "LS Monday-A":("Art/Science (A Week)","art clothing"),
    "LS Tuesday-A":("Spanish/Dance (A Week)","easy on/off shoes"),
    "LS Wednesday-A":("PE/Spanish (A Week)","sneakers"),
    "LS Thursday-A":("Art/Science (A Week)","art clothing"),
    "LS Friday-A":("Swim (A Week)","swim suit"),
    "LS Monday-B":("Spanish/PE (B Week)","sneakers"),
    "LS Tuesday-B":("PE (B Week)","sneakers"),
    "LS Wednesday-B":("Spanish/Dance (B Week)","easy on/off shoes"),
    "LS Thursday-B":("Art/Science (B Week)","art clothing"),
    "LS Friday-B":("Swim (B Week)","swim suit")
}

event_mapping = miles_event_mapping

@click.group()
def cli():
    pass

@cli.command("transform")
@click.argument('input_ics', type=click.Path(exists=True))
@click.argument('output_location', type=click.Path())
def transform(input_ics, output_location):
    """Transform a calendar.ics file and save to output location."""
    click.echo(f"Transforming {input_ics} and saving to {output_location}")

    with open(input_ics, 'r') as f:
        with open(output_location,'w') as w:
            orig_calendar = ics.Calendar(f.read())
            new_calendar = ics.Calendar()

            for event in sorted(orig_calendar.events, key=lambda x:x.begin):
                if "LS" not in event.name:
                    click.echo(f"---excluding {event.name}")
                    continue

                new_event = ics.Event()

                new_event.begin = event.begin
                new_event.end = event.begin
                new_event.make_all_day()

                if event.name in event_mapping:
                    (name, description) = event_mapping[event.name]
                    new_event.name = name
                    new_event.description = description
                else:
                    new_event.name = event.name
                    new_event.description = event.description
    
                click.echo(f"{new_event.name} - {new_event.begin} - {new_event.end} - {new_event.description}")
                new_calendar.events.add(new_event)

            # Write the new calendar to output_location
            w.write(str(new_calendar))
            click.echo(f"Number of events: {len(new_calendar.events)}")


@cli.command("inspect")
@click.argument('input_ics', type=click.Path(exists=True))
def inspect(input_ics):
    """Inspect a calendar.ics file and print event names and dates."""
    with open(input_ics, 'r') as f:
        calendar = ics.Calendar(f.read())
        for event in sorted(calendar.events, key=lambda x: x.begin):
            click.echo(f"{event.name} - {event.begin.date()}")


if __name__ == '__main__':
    cli()