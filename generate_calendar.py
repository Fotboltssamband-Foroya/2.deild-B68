import requests
from ics import Calendar, Event
from datetime import datetime
import pytz

# API endpoint
url = "https://comet.fsf.fo/data-backend/api/public/areports/run/0/25/?API_KEY=866d8bcc142a87e21f64f0d8febb3a61c81f45e3c7b5151b08d50a8d8613120088f3b3521b6b53746a54623a5b6f1249b23e2aaac845387df6ba2edc1f03e07c"
response = requests.get(url)
data = response.json()

calendar = Calendar()
tz = pytz.timezone('Atlantic/Faroe')

for match in data.get('results', []):
    timestamp = match.get("matchDate")
    if not timestamp:
        continue

    description = match.get("matchDescription", "Ókend dystur")
    location = match.get("facility", "Ókend leikvøllur")
    match_status = match.get("matchStatus", "")
    round_number = match.get("round", "")
    competition = match.get("competitionType", "")

    start = datetime.fromtimestamp(timestamp / 1000, tz)

    event = Event()
    event.name = description
    event.begin = start
    event.duration = {"hours": 2}
    event.location = location
    event.description = (
        f"🏆 {competition}\n"
        f"🔁 Umfar: {round_number}\n"
        f"📊 Støða: {match_status}"
    )

    calendar.events.add(event)

with open('b68_2deild.ics', 'w', encoding='utf-8') as f:
    f.write(str(calendar))
