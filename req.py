import requests

BASE_URL = "http://127.0.0.1:8000"  # Change to your running FastAPI server URL


def add_event():
    print("Enter event details:")
    print("Format: title,event_type,location,event_date(YYYY-MM-DD),organizer_contact,reminder(True/False)")
    details = input(">>> ")
    try:
        title, event_type, location, event_date, organizer_contact, reminder = details.split(",")
        reminder = reminder.strip().lower() == "true"

        payload = {
            "title": title.strip(),
            "event_type": event_type.strip(),
            "location": location.strip(),
            "event_date": event_date.strip(),
            "organizer_contact": organizer_contact.strip(),
            "reminder": reminder
        }

        response = requests.post(f"{BASE_URL}/events/", json=payload)

        if response.status_code == 201:
            print("Event added successfully with ID:", response.json().get("id"))
        else:
            print("Failed to add event:", response.json())
    except ValueError:
        print("Invalid input format. Please provide all fields separated by commas.")


def list_all_events():
    response = requests.get(f"{BASE_URL}/events/")
    if response.status_code == 200:
        events = response.json()
        if not events:
            print("No events found.")
        for event in events:
            print(event)
    else:
        print("Error fetching events:", response.json())


def get_event_by_id():
    event_id = input("Enter event ID: ").strip()
    if not event_id.isdigit():
        print("Event ID must be an integer.")
        return
    response = requests.get(f"{BASE_URL}/events/{event_id}")
    if response.status_code == 200:
        print(response.json())
    else:
        print("Event not found.")


def update_event():
    event_id = input("Enter event ID to update: ").strip()
    if not event_id.isdigit():
        print("Event ID must be an integer.")
        return
    print("Enter fields to update (leave blank to skip):")
    title = input("Title: ").strip()
    event_type = input("Event Type: ").strip()
    location = input("Location: ").strip()
    event_date = input("Event Date (YYYY-MM-DD): ").strip()
    organizer_contact = input("Organizer Contact: ").strip()
    reminder = input("Reminder (True/False): ").strip()

    payload = {}
    if title:
        payload["title"] = title
    if event_type:
        payload["event_type"] = event_type
    if location:
        payload["location"] = location
    if event_date:
        payload["event_date"] = event_date
    if organizer_contact:
        payload["organizer_contact"] = organizer_contact
    if reminder.lower() in ["true", "false"]:
        payload["reminder"] = reminder.lower() == "true"

    if not payload:
        print("No fields to update.")
        return

    response = requests.put(f"{BASE_URL}/events/{event_id}", json=payload)
    if response.status_code == 200:
        print("Event updated:", response.json())
    else:
        print("Failed to update event:", response.json())


def delete_event():
    event_id = input("Enter event ID to delete: ").strip()
    if not event_id.isdigit():
        print("Event ID must be an integer.")
        return
    response = requests.delete(f"{BASE_URL}/events/{event_id}")
    if response.status_code == 200:
        print(response.json().get("message"))
    else:
        print("Failed to delete event:", response.json())


def list_upcoming_events():
    response = requests.get(f"{BASE_URL}/events/upcoming")
    if response.status_code == 200:
        events = response.json()
        if not events:
            print("No upcoming events.")
        for event in events:
            print(event)
    else:
        print("Error fetching upcoming events:", response.json())


def get_events_by_type():
    event_type = input("Enter event type to filter by: ").strip()
    response = requests.get(f"{BASE_URL}/events/type/{event_type}")
    if response.status_code == 200:
        events = response.json()
        if not events:
            print(f"No events found for type '{event_type}'.")
        for event in events:
            print(event)
    else:
        print("Error fetching events by type:", response.json())


def main():
    while True:
        print("\nChoose an option:")
        print("1. Add Event")
        print("2. List All Events")
        print("3. Get Event by ID")
        print("4. Update Event")
        print("5. Delete Event")
        print("6. List Upcoming Events")
        print("7. Get Events by Type")
        print("0. Exit")

        choice = input(">>> ").strip()
        if choice == "1":
            add_event()
        elif choice == "2":
            list_all_events()
        elif choice == "3":
            get_event_by_id()
        elif choice == "4":
            update_event()
        elif choice == "5":
            delete_event()
        elif choice == "6":
            list_upcoming_events()
        elif choice == "7":
            get_events_by_type()
        elif choice == "0":
            print("Exiting.")
            break
        else:
            print("Invalid choice, try again.")


if __name__ == "__main__":
    main()
