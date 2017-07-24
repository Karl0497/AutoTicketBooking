# AutoTicketBooking
Fully automated movie tickets booking system (For Events Cinemas NZ)

# What does this do?
It books movie tickets for you. Works for every Event cinema in NZ.
By using Selenium Webdriver, this script simulates real user booking tickets.

# How does it work?
First, it logs you in, shows you a list of now showing movies. You choose, then it lets you select the time session and number of tickets, after which, everything is automated, it will:
- get you the most suitable tickets, 
- choose the "ideal" seats,
- enter your credit card details and complete the order. For security reason, Card Security Code will need to be entered manually.

## How does it choose the right seats?
Cinema's layout is visualised as a point system. The closer a seat to the center, both vertically and horizontally, the more points it has. A seat value is calculated as row value + column value, so in a cinema of 11 x 11 seats, the one at (6, 6) will be the best.


To use this:
- Update your information in config.py
- Get Selenium.
- "Headless" mode is available, set it to False to see the script work with a browser open (in main.py).

# DISCLAIMER
- I do not collect your information through the script.
- I am not responsible for any issue related to your account or credit card.



