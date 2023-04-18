# bruteforce_password_seleniun
Python script to retrieve password by bruteforce list on a website.

# Usage

Configure following variables before starting the script:

browser_select = "chrome", can be also used with Firefox by setting "firefox"

username = "username@domain.com"

password = "password"

login_url = "https://www.website.com/login"

By default, 4 digits pin list is used with 4_digits_pin_list.txt but can be alternatively changed with pin ordered by statistics 4_digits_pin_list_ordered_by_stats.txt

# Usage
python bruteforce.py
