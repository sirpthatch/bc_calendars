Calendar link:
https://api.veracross.com/bcs/subscribe/0F1C3A67-F297-4626-A8C7-6C7B1F71944C.ics?uid=658E8E41-5CE5-4786-81A0-1DD981559461

curl -o calendar.ics "https://api.veracross.com/bcs/subscribe/0F1C3A67-F297-4626-A8C7-6C7B1F71944C.ics?uid=658E8E41-5CE5-4786-81A0-1DD981559461"

(Located as "My Household Calendar" on https://portals.veracross.com/bcs/parent/calendar/subscribe/mine, selecting for google subscription)


Notes:
* Last used to generate calendars for the 2025 school year (1st grade)
* School moved from 6 day schedule to A/B weeks
* The top of the calendar_transforms file contains a mapping between the days of the week for each A/B week and the specials for those days
* Right now it generates a calendar for the full year - it looks like the specials are only going to be set for the first semeester
* After creating the calendar, you can import it into a google calendar.  I imported it into a separate dedidcated google calendar, and then separately shared that calendar with folks - I can modify that calendar in the future to fix the days that are changing (i.e. in next semester)