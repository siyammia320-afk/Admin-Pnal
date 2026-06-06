import requests
import time
import threading
import re
import json
import os
import random
import string
from datetime import datetime, timedelta
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# ==================== কনফিগারেশন ====================
TELEGRAM_TOKEN = "8649024139:AAHH_d9BJTzYSnOGUEM7QIarc1czMMV_aTM"
ADMIN_ID = 7787612625

XMNIT_BASE_URL = "https://x.mnitnetwork.com"
LOG_GROUP_ID = "-1003538330629"
OTP_GROUP_URL = "https://t.me/power_otp_botx"

# ==================== লগইন তথ্য ====================
LOGIN_EMAIL = "minhajurrahmanrabbi20@gmail.com"
LOGIN_PASSWORD = "minhajur_rahman_rabbi_"
AUTH_TOKEN = None

# ==================== মেইল ডোমেইন ====================
MAIL_DOMAIN = "ARAFAT.BD"

# ==================== এডমিন সেট করা পাসওয়ার্ড (ডিফল্ট) ====================
ADMIN_SET_PASSWORD = "Admin@123456"  # এডমিন এখানে পাসওয়ার্ড সেট করবেন

# ==================== Monkey Patch ====================
def ibtn(text, callback_data=None, url=None, style=None):
    b = InlineKeyboardButton(text=text, callback_data=callback_data, url=url)
    if style: b.style = style
    return b

def rbtn(text, style=None):
    b = KeyboardButton(text=text)
    if style: b.style = style
    return b

# ==================== কান্ট্রি ফ্ল্যাগ এবং কোড ম্যাপ (প্রিফিক্স অনুযায়ী) ====================
COUNTRY_FLAGS = {
    "AD": "🇦🇩", "AE": "🇦🇪", "AF": "🇦🇫", "AG": "🇦🇬", "AI": "🇦🇮", "AL": "🇦🇱",
    "AM": "🇦🇲", "AO": "🇦🇴", "AQ": "🇦🇶", "AR": "🇦🇷", "AS": "🇦🇸", "AT": "🇦🇹",
    "AU": "🇦🇺", "AW": "🇦🇼", "AX": "🇦🇽", "AZ": "🇦🇿", "BA": "🇧🇦", "BB": "🇧🇧",
    "BD": "🇧🇩", "BE": "🇧🇪", "BF": "🇧🇫", "BG": "🇧🇬", "BH": "🇧🇭", "BI": "🇧🇮",
    "BJ": "🇧🇯", "BL": "🇧🇱", "BM": "🇧🇲", "BN": "🇧🇳", "BO": "🇧🇴", "BQ": "🇧🇶",
    "BR": "🇧🇷", "BS": "🇧🇸", "BT": "🇧🇹", "BV": "🇧🇻", "BW": "🇧🇼", "BY": "🇧🇾",
    "BZ": "🇧🇿", "CA": "🇨🇦", "CC": "🇨🇨", "CD": "🇨🇩", "CF": "🇨🇫", "CG": "🇨🇬",
    "CH": "🇨🇭", "CI": "🇨🇮", "CK": "🇨🇰", "CL": "🇨🇱", "CM": "🇨🇲", "CN": "🇨🇳",
    "CO": "🇨🇴", "CR": "🇨🇷", "CU": "🇨🇺", "CV": "🇨🇻", "CW": "🇨🇼", "CX": "🇨🇽",
    "CY": "🇨🇾", "CZ": "🇨🇿", "DE": "🇩🇪", "DJ": "🇩🇯", "DK": "🇩🇰", "DM": "🇩🇲",
    "DO": "🇩🇴", "DZ": "🇩🇿", "EC": "🇪🇨", "EE": "🇪🇪", "EG": "🇪🇬", "EH": "🇪🇭",
    "ER": "🇪🇷", "ES": "🇪🇸", "ET": "🇪🇹", "FI": "🇫🇮", "FJ": "🇫🇯", "FK": "🇫🇰",
    "FM": "🇫🇲", "FO": "🇫🇴", "FR": "🇫🇷", "GA": "🇬🇦", "GB": "🇬🇧", "GD": "🇬🇩",
    "GE": "🇬🇪", "GF": "🇬🇫", "GG": "🇬🇬", "GH": "🇬🇭", "GI": "🇬🇮", "GL": "🇬🇱",
    "GM": "🇬🇲", "GN": "🇬🇳", "GP": "🇬🇵", "GQ": "🇬🇶", "GR": "🇬🇷", "GS": "🇬🇸",
    "GT": "🇬🇹", "GU": "🇬🇺", "GW": "🇬🇼", "GY": "🇬🇾", "HK": "🇭🇰", "HM": "🇭🇲",
    "HN": "🇭🇳", "HR": "🇭🇷", "HT": "🇭🇹", "HU": "🇭🇺", "ID": "🇮🇩", "IE": "🇮🇪",
    "IL": "🇮🇱", "IM": "🇮🇲", "IN": "🇮🇳", "IO": "🇮🇴", "IQ": "🇮🇶", "IR": "🇮🇷",
    "IS": "🇮🇸", "IT": "🇮🇹", "JE": "🇯🇪", "JM": "🇯🇲", "JO": "🇯🇴", "JP": "🇯🇵",
    "KE": "🇰🇪", "KG": "🇰🇬", "KH": "🇰🇭", "KI": "🇰🇮", "KM": "🇰🇲", "KN": "🇰🇳",
    "KP": "🇰🇵", "KR": "🇰🇷", "KW": "🇰🇼", "KY": "🇰🇾", "KZ": "🇰🇿", "LA": "🇱🇦",
    "LB": "🇱🇧", "LC": "🇱🇨", "LI": "🇱🇮", "LK": "🇱🇰", "LR": "🇱🇷", "LS": "🇱🇸",
    "LT": "🇱🇹", "LU": "🇱🇺", "LV": "🇱🇻", "LY": "🇱🇾", "MA": "🇲🇦", "MC": "🇲🇨",
    "MD": "🇲🇩", "ME": "🇲🇪", "MF": "🇲🇫", "MG": "🇲🇬", "MH": "🇲🇭", "MK": "🇲🇰",
    "ML": "🇲🇱", "MM": "🇲🇲", "MN": "🇲🇳", "MO": "🇲🇴", "MP": "🇲🇵", "MQ": "🇲🇶",
    "MR": "🇲🇷", "MS": "🇲🇸", "MT": "🇲🇹", "MU": "🇲🇺", "MV": "🇲🇻", "MW": "🇲🇼",
    "MX": "🇲🇽", "MY": "🇲🇾", "MZ": "🇲🇿", "NA": "🇳🇦", "NC": "🇳🇨", "NE": "🇳🇪",
    "NF": "🇳🇫", "NG": "🇳🇬", "NI": "🇳🇮", "NL": "🇳🇱", "NO": "🇳🇴", "NP": "🇳🇵",
    "NR": "🇳🇷", "NU": "🇳🇺", "NZ": "🇳🇿", "OM": "🇴🇲", "PA": "🇵🇦", "PE": "🇵🇪",
    "PF": "🇵🇫", "PG": "🇵🇬", "PH": "🇵🇭", "PK": "🇵🇰", "PL": "🇵🇱", "PM": "🇵🇲",
    "PN": "🇵🇳", "PR": "🇵🇷", "PS": "🇵🇸", "PT": "🇵🇹", "PW": "🇵🇼", "PY": "🇵🇾",
    "QA": "🇶🇦", "RE": "🇷🇪", "RO": "🇷🇴", "RS": "🇷🇸", "RU": "🇷🇺", "RW": "🇷🇼",
    "SA": "🇸🇦", "SB": "🇸🇧", "SC": "🇸🇨", "SD": "🇸🇩", "SE": "🇸🇪", "SG": "🇸🇬",
    "SH": "🇸🇭", "SI": "🇸🇮", "SJ": "🇸🇯", "SK": "🇸🇰", "SL": "🇸🇱", "SM": "🇸🇲",
    "SN": "🇸🇳", "SO": "🇸🇴", "SR": "🇸🇷", "SS": "🇸🇸", "ST": "🇸🇹", "SV": "🇸🇻",
    "SX": "🇸🇽", "SY": "🇸🇾", "SZ": "🇸🇿", "TC": "🇹🇨", "TD": "🇹🇩", "TF": "🇹🇫",
    "TG": "🇹🇬", "TH": "🇹🇭", "TJ": "🇹🇯", "TK": "🇹🇰", "TL": "🇹🇱", "TM": "🇹🇲",
    "TN": "🇹🇳", "TO": "🇹🇴", "TR": "🇹🇷", "TT": "🇹🇹", "TV": "🇹🇻", "TW": "🇹🇼",
    "TZ": "🇹🇿", "UA": "🇺🇦", "UG": "🇺🇬", "UM": "🇺🇲", "US": "🇺🇸", "UY": "🇺🇾",
    "UZ": "🇺🇿", "VA": "🇻🇦", "VC": "🇻🇨", "VE": "🇻🇪", "VG": "🇻🇬", "VI": "🇻🇮",
    "VN": "🇻🇳", "VU": "🇻🇺", "WF": "🇼🇫", "WS": "🇼🇸", "YE": "🇾🇪", "YT": "🇾🇹",
    "ZA": "🇿🇦", "ZM": "🇿🇲", "ZW": "🇿🇼"
}

COUNTRY_NAMES = {
    "AD": "Andorra", "AE": "United Arab Emirates", "AF": "Afghanistan", "AG": "Antigua and Barbuda",
    "AI": "Anguilla", "AL": "Albania", "AM": "Armenia", "AO": "Angola", "AQ": "Antarctica",
    "AR": "Argentina", "AS": "American Samoa", "AT": "Austria", "AU": "Australia", "AW": "Aruba",
    "AX": "Aland Islands", "AZ": "Azerbaijan", "BA": "Bosnia and Herzegovina", "BB": "Barbados",
    "BD": "Bangladesh", "BE": "Belgium", "BF": "Burkina Faso", "BG": "Bulgaria", "BH": "Bahrain",
    "BI": "Burundi", "BJ": "Benin", "BL": "Saint Barthelemy", "BM": "Bermuda", "BN": "Brunei Darussalam",
    "BO": "Bolivia", "BQ": "Bonaire", "BR": "Brazil", "BS": "Bahamas", "BT": "Bhutan",
    "BV": "Bouvet Island", "BW": "Botswana", "BY": "Belarus", "BZ": "Belize", "CA": "Canada",
    "CC": "Cocos Islands", "CD": "Congo DR", "CF": "Central African Republic", "CG": "Congo Republic",
    "CH": "Switzerland", "CI": "Ivory Coast", "CK": "Cook Islands", "CL": "Chile", "CM": "Cameroon",
    "CN": "China", "CO": "Colombia", "CR": "Costa Rica", "CU": "Cuba", "CV": "Cape Verde",
    "CW": "Curacao", "CX": "Christmas Island", "CY": "Cyprus", "CZ": "Czech Republic", "DE": "Germany",
    "DJ": "Djibouti", "DK": "Denmark", "DM": "Dominica", "DO": "Dominican Republic", "DZ": "Algeria",
    "EC": "Ecuador", "EE": "Estonia", "EG": "Egypt", "EH": "Western Sahara", "ER": "Eritrea",
    "ES": "Spain", "ET": "Ethiopia", "FI": "Finland", "FJ": "Fiji", "FK": "Falkland Islands",
    "FM": "Micronesia", "FO": "Faroe Islands", "FR": "France", "GA": "Gabon", "GB": "United Kingdom",
    "GD": "Grenada", "GE": "Georgia", "GF": "French Guiana", "GG": "Guernsey", "GH": "Ghana",
    "GI": "Gibraltar", "GL": "Greenland", "GM": "Gambia", "GN": "Guinea", "GP": "Guadeloupe",
    "GQ": "Equatorial Guinea", "GR": "Greece", "GS": "South Georgia", "GT": "Guatemala", "GU": "Guam",
    "GW": "Guinea-Bissau", "GY": "Guyana", "HK": "Hong Kong", "HM": "Heard Island", "HN": "Honduras",
    "HR": "Croatia", "HT": "Haiti", "HU": "Hungary", "ID": "Indonesia", "IE": "Ireland", "IL": "Israel",
    "IM": "Isle of Man", "IN": "India", "IO": "British Indian Ocean Territory", "IQ": "Iraq",
    "IR": "Iran", "IS": "Iceland", "IT": "Italy", "JE": "Jersey", "JM": "Jamaica", "JO": "Jordan",
    "JP": "Japan", "KE": "Kenya", "KG": "Kyrgyzstan", "KH": "Cambodia", "KI": "Kiribati",
    "KM": "Comoros", "KN": "Saint Kitts and Nevis", "KP": "North Korea", "KR": "South Korea",
    "KW": "Kuwait", "KY": "Cayman Islands", "KZ": "Kazakhstan", "LA": "Laos", "LB": "Lebanon",
    "LC": "Saint Lucia", "LI": "Liechtenstein", "LK": "Sri Lanka", "LR": "Liberia", "LS": "Lesotho",
    "LT": "Lithuania", "LU": "Luxembourg", "LV": "Latvia", "LY": "Libya", "MA": "Morocco",
    "MC": "Monaco", "MD": "Moldova", "ME": "Montenegro", "MF": "Saint Martin", "MG": "Madagascar",
    "MH": "Marshall Islands", "MK": "North Macedonia", "ML": "Mali", "MM": "Myanmar", "MN": "Mongolia",
    "MO": "Macao", "MP": "Northern Mariana Islands", "MQ": "Martinique", "MR": "Mauritania",
    "MS": "Montserrat", "MT": "Malta", "MU": "Mauritius", "MV": "Maldives", "MW": "Malawi",
    "MX": "Mexico", "MY": "Malaysia", "MZ": "Mozambique", "NA": "Namibia", "NC": "New Caledonia",
    "NE": "Niger", "NF": "Norfolk Island", "NG": "Nigeria", "NI": "Nicaragua", "NL": "Netherlands",
    "NO": "Norway", "NP": "Nepal", "NR": "Nauru", "NU": "Niue", "NZ": "New Zealand", "OM": "Oman",
    "PA": "Panama", "PE": "Peru", "PF": "French Polynesia", "PG": "Papua New Guinea", "PH": "Philippines",
    "PK": "Pakistan", "PL": "Poland", "PM": "Saint Pierre and Miquelon", "PN": "Pitcairn",
    "PR": "Puerto Rico", "PS": "Palestine", "PT": "Portugal", "PW": "Palau", "PY": "Paraguay",
    "QA": "Qatar", "RE": "Reunion", "RO": "Romania", "RS": "Serbia", "RU": "Russia", "RW": "Rwanda",
    "SA": "Saudi Arabia", "SB": "Solomon Islands", "SC": "Seychelles", "SD": "Sudan", "SE": "Sweden",
    "SG": "Singapore", "SH": "Saint Helena", "SI": "Slovenia", "SJ": "Svalbard", "SK": "Slovakia",
    "SL": "Sierra Leone", "SM": "San Marino", "SN": "Senegal", "SO": "Somalia", "SR": "Suriname",
    "SS": "South Sudan", "ST": "Sao Tome and Principe", "SV": "El Salvador", "SX": "Sint Maarten",
    "SY": "Syria", "SZ": "Eswatini", "TC": "Turks and Caicos Islands", "TD": "Chad", "TF": "French Southern Territories",
    "TG": "Togo", "TH": "Thailand", "TJ": "Tajikistan", "TK": "Tokelau", "TL": "Timor-Leste",
    "TM": "Turkmenistan", "TN": "Tunisia", "TO": "Tonga", "TR": "Turkey", "TT": "Trinidad and Tobago",
    "TV": "Tuvalu", "TW": "Taiwan", "TZ": "Tanzania", "UA": "Ukraine", "UG": "Uganda",
    "UM": "US Minor Outlying Islands", "US": "United States", "UY": "Uruguay", "UZ": "Uzbekistan",
    "VA": "Vatican City", "VC": "Saint Vincent and the Grenadines", "VE": "Venezuela", "VG": "Virgin Islands British",
    "VI": "Virgin Islands US", "VN": "Vietnam", "VU": "Vanuatu", "WF": "Wallis and Futuna",
    "WS": "Samoa", "YE": "Yemen", "YT": "Mayotte", "ZA": "South Africa", "ZM": "Zambia", "ZW": "Zimbabwe"
}

# প্রিফিক্স থেকে কান্ট্রি শর্ট কোড ম্যাপিং
PREFIX_TO_COUNTRY = {
    "1": "US", "7": "RU", "20": "EG", "27": "ZA", "30": "GR", "31": "NL", "32": "BE",
    "33": "FR", "34": "ES", "36": "HU", "39": "IT", "40": "RO", "41": "CH", "43": "AT",
    "44": "GB", "45": "DK", "46": "SE", "47": "NO", "48": "PL", "49": "DE", "51": "PE",
    "52": "MX", "53": "CU", "54": "AR", "55": "BR", "56": "CL", "57": "CO", "58": "VE",
    "60": "MY", "61": "AU", "62": "ID", "63": "PH", "64": "NZ", "65": "SG", "66": "TH",
    "81": "JP", "82": "KR", "84": "VN", "86": "CN", "90": "TR", "91": "IN", "92": "PK",
    "93": "AF", "94": "LK", "95": "MM", "98": "IR", "211": "SS", "212": "MA", "213": "DZ",
    "216": "TN", "218": "LY", "220": "GM", "221": "SN", "222": "MR", "223": "ML", "224": "GN",
    "225": "CI", "226": "BF", "227": "NE", "228": "TG", "229": "BJ", "230": "MU", "231": "LR",
    "232": "SL", "233": "GH", "234": "NG", "235": "TD", "236": "CF", "237": "CM", "238": "CV",
    "239": "ST", "240": "GQ", "241": "GA", "242": "CG", "243": "CD", "244": "AO", "245": "GW",
    "246": "IO", "247": "AC", "248": "SC", "249": "SD", "250": "RW", "251": "ET", "252": "SO",
    "253": "DJ", "254": "KE", "255": "TZ", "256": "UG", "257": "BI", "258": "MZ", "260": "ZM",
    "261": "MG", "262": "RE", "263": "ZW", "264": "NA", "265": "MW", "266": "LS", "267": "BW",
    "268": "SZ", "269": "KM", "290": "SH", "291": "ER", "297": "AW", "298": "FO", "299": "GL",
    "350": "GI", "351": "PT", "352": "LU", "353": "IE", "354": "IS", "355": "AL", "356": "MT",
    "357": "CY", "358": "FI", "359": "BG", "370": "LT", "371": "LV", "372": "EE", "373": "MD",
    "374": "AM", "375": "BY", "376": "AD", "377": "MC", "378": "SM", "379": "VA", "380": "UA",
    "381": "RS", "382": "ME", "383": "XK", "385": "HR", "386": "SI", "387": "BA", "389": "MK",
    "420": "CZ", "421": "SK", "423": "LI", "500": "FK", "501": "BZ", "502": "GT", "503": "SV",
    "504": "HN", "505": "NI", "506": "CR", "507": "PA", "508": "PM", "509": "HT", "590": "GP",
    "591": "BO", "592": "GY", "593": "EC", "594": "GF", "595": "PY", "596": "MQ", "597": "SR",
    "598": "UY", "599": "CW", "670": "TL", "672": "NF", "673": "BN", "674": "NR", "675": "PG",
    "676": "TO", "677": "SB", "678": "VU", "679": "FJ", "680": "PW", "681": "WF", "682": "CK",
    "683": "NU", "685": "WS", "686": "KI", "687": "NC", "688": "TV", "689": "PF", "690": "TK",
    "691": "FM", "692": "MH", "850": "KP", "852": "HK", "853": "MO", "855": "KH", "856": "LA",
    "880": "BD", "886": "TW", "960": "MV", "961": "LB", "962": "JO", "963": "SY", "964": "IQ",
    "965": "KW", "966": "SA", "967": "YE", "968": "OM", "970": "PS", "971": "AE", "972": "IL",
    "973": "BH", "974": "QA", "975": "BT", "976": "MN", "977": "NP", "992": "TJ", "993": "TM",
    "994": "AZ", "995": "GE", "996": "KG", "998": "UZ"
}

def get_country_info_from_range(range_code):
    """রেঞ্জ কোড থেকে কান্ট্রি তথ্য বের করে (যেমন: 880XXXXXXX থেকে 880)"""
    range_str = str(range_code).replace("X", "").strip()
    for length in range(4, 0, -1):
        prefix = range_str[:length]
        if prefix in PREFIX_TO_COUNTRY:
            country_code = PREFIX_TO_COUNTRY[prefix]
            country_name = COUNTRY_NAMES.get(country_code, "Unknown")
            flag = COUNTRY_FLAGS.get(country_code, "🌍")
            return country_code, country_name, flag
    return "XX", "Unknown", "🌍"

def format_range_with_flag(range_code):
    """রেঞ্জের সাথে ফ্ল্যাগ যোগ করে (যেমন: 🇧🇩 880XXXXXXX)"""
    country_code, country_name, flag = get_country_info_from_range(range_code)
    return f"{flag} {range_code}"

# ==================== র‍্যান্ডম মেইল জেনারেটর ====================
used_emails = set()

def generate_random_email():
    """ইউনিক র‍্যান্ডম মেইল জেনারেট করে"""
    while True:
        random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=12))
        email = f"{random_string}@{MAIL_DOMAIN}"
        if email not in used_emails:
            used_emails.add(email)
            return email

# ==================== XMNIT লগইন ====================
def xmnit_login():
    global AUTH_TOKEN
    login_url = f"{XMNIT_BASE_URL}/mapi/v1/mauth/login"
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 12) AppleWebKit/537.36",
        "Content-Type": "application/json",
        "Origin": XMNIT_BASE_URL,
        "Referer": f"{XMNIT_BASE_URL}/mauth/login",
        "x-requested-with": "mark.via.gp"
    }
    payload = {"email": LOGIN_EMAIL, "password": LOGIN_PASSWORD}
    
    try:
        response = requests.post(login_url, json=payload, headers=headers, timeout=15)
        if response.status_code == 200:
            data = response.json()
            AUTH_TOKEN = data.get("data", {}).get("token")
            if AUTH_TOKEN:
                print("✅ XMNIT Login Success!")
                return True
    except Exception as e:
        print(f"❌ Login Failed: {e}")
    return False

# ==================== XMNIT API ফাংশন ====================
def xmnit_get_live_ranges(service):
    global AUTH_TOKEN
    if not AUTH_TOKEN:
        xmnit_login()
    
    try:
        headers = {
            "mauthtoken": AUTH_TOKEN,
            "User-Agent": "Mozilla/5.0 (Linux; Android 12) AppleWebKit/537.36",
            "x-requested-with": "mark.via.gp"
        }
        response = requests.get(f"{XMNIT_BASE_URL}/mapi/v1/mdashboard/console/info", headers=headers, timeout=15)
        
        if response.status_code == 401:
            xmnit_login()
            headers["mauthtoken"] = AUTH_TOKEN
            response = requests.get(f"{XMNIT_BASE_URL}/mapi/v1/mdashboard/console/info", headers=headers, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            logs = data.get("data", {}).get("logs", [])
            ranges = []
            for log in logs:
                app_name = log.get("app_name", "").lower()
                if service.lower() in app_name:
                    rng = log.get("range")
                    if rng:
                        range_str = str(rng).upper().strip()
                        if not range_str.endswith('X'):
                            digits_only = re.sub(r'[^0-9]', '', range_str)
                            if digits_only:
                                if len(digits_only) >= 10:
                                    prefix = digits_only[:5] if len(digits_only) >= 11 else digits_only[:4]
                                    range_str = prefix + "XXXXXX"
                                else:
                                    range_str = digits_only + "XXXXX"
                        ranges.append(range_str)
            ranges = list(dict.fromkeys(ranges))
            ranges_with_flags = [(format_range_with_flag(r), r) for r in ranges]
            ranges_with_flags.sort(key=lambda x: x[0])
            return [(r[1], r[0]) for r in ranges_with_flags]
    except Exception as e:
        print(f"Ranges error: {e}")
    return []

def get_combined_fb_ig_ranges():
    fb_data = xmnit_get_live_ranges("facebook")
    ig_data = xmnit_get_live_ranges("instagram")
    all_ranges = {}
    for rng, display in fb_data:
        all_ranges[rng] = display
    for rng, display in ig_data:
        if rng not in all_ranges:
            all_ranges[rng] = display
    sorted_items = sorted(all_ranges.items(), key=lambda x: x[1])
    return [(rng, display) for rng, display in sorted_items]

def xmnit_fetch_number(range_code):
    global AUTH_TOKEN
    if not AUTH_TOKEN:
        xmnit_login()
    
    url = f"{XMNIT_BASE_URL}/mapi/v1/mdashboard/getnum/number"
    headers = {
        "mauthtoken": AUTH_TOKEN,
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Linux; Android 12) AppleWebKit/537.36",
        "Origin": XMNIT_BASE_URL,
        "x-requested-with": "mark.via.gp"
    }
    payload = {"range": range_code, "is_national": False, "remove_plus": False}
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=15)
        
        if response.status_code == 401:
            xmnit_login()
            headers["mauthtoken"] = AUTH_TOKEN
            response = requests.post(url, json=payload, headers=headers, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            number_data = data.get("data", {})
            number = number_data.get("full_number") or number_data.get("number")
            
            if number:
                return str(number).replace("+", "").strip()
    except Exception as e:
        print(f"Fetch error: {e}")
    return None

def xmnit_check_otp():
    global AUTH_TOKEN
    results = []
    if not AUTH_TOKEN:
        xmnit_login()
    
    today = datetime.now().strftime("%Y-%m-%d")
    try:
        headers = {
            "mauthtoken": AUTH_TOKEN,
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Linux; Android 12) AppleWebKit/537.36",
            "x-requested-with": "mark.via.gp"
        }
        response = requests.get(f"{XMNIT_BASE_URL}/mapi/v1/mdashboard/getnum/info?date={today}&page=1&search=&status=success", headers=headers, timeout=15)
        
        if response.status_code == 401:
            xmnit_login()
            headers["mauthtoken"] = AUTH_TOKEN
            response = requests.get(f"{XMNIT_BASE_URL}/mapi/v1/mdashboard/getnum/info?date={today}&page=1&search=&status=success", headers=headers, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            numbers_list = data.get("data", {}).get("numbers", [])
            active = get_active_numbers()
            
            for item in numbers_list:
                number = item.get("number", "")
                message = item.get("message", "")
                app_name = item.get("app_name", "")
                
                if str(number) in active:
                    service = "Facebook/Instagram"
                    
                    otp = extract_otp_from_text(message)
                    if otp != "N/A":
                        results.append({
                            "phone": number,
                            "message": message,
                            "otp": otp,
                            "service": service,
                            "range": active[str(number)].get("range", "")
                        })
    except Exception as e:
        print(f"OTP error: {e}")
    return results

# ==================== OTP এক্সট্রাক্ট ====================
def extract_otp_from_text(text):
    text = str(text)
    clean_text = re.sub(r'[-\s\.]', '', text)
    
    patterns = [
        r'FB[-]?(\d{5,6})',
        r'code[:\s]*(\d{4,8})',
        r'otp[:\s]*(\d{4,8})',
        r'(\d{8})', r'(\d{7})', r'(\d{6})', r'(\d{5})', r'(\d{4})',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, clean_text, re.IGNORECASE)
        if match:
            otp = match.group(1)
            if len(otp) >= 4:
                return otp
    
    digits = re.findall(r'\d+', clean_text)
    for digit in digits:
        if len(digit) >= 4:
            return digit
    return "N/A"

def mask_number_for_group(phone):
    phone_str = str(phone)
    if len(phone_str) >= 10:
        return phone_str[:4] + "*******" + phone_str[-4:]
    return phone_str[:4] + "*******"

def mask_number(phone):
    phone_str = str(phone)
    if len(phone_str) >= 10:
        return phone_str[:7] + "XXX" + phone_str[-2:]
    return phone_str

# ==================== ডাটাবেস ====================
USER_DB = "xmnit_users.json"
USER_DATA_DB = "xmnit_user_data.json"
SETTINGS_DB = "xmnit_settings.json"
WITHDRAWALS_DB = "xmnit_withdrawals.json"
ACTIVE_NUMBERS_DB = "xmnit_active_numbers.json"
PENDING_ACCOUNTS_DB = "xmnit_pending_accounts.json"
USER_SUBMIT_LIMIT_DB = "xmnit_user_submit_limit.json"

def init_databases():
    files = {
        USER_DB: [],
        USER_DATA_DB: {},
        SETTINGS_DB: {"otp_price": 5.0, "min_withdraw": 50.0, "daily_limit": 10},
        WITHDRAWALS_DB: [],
        ACTIVE_NUMBERS_DB: {},
        PENDING_ACCOUNTS_DB: [],
        USER_SUBMIT_LIMIT_DB: {}
    }
    for file, default in files.items():
        if not os.path.exists(file):
            with open(file, "w") as f:
                json.dump(default, f)

init_databases()

def get_user_balance(user_id):
    with open(USER_DATA_DB, "r") as f:
        data = json.load(f)
    return data.get(str(user_id), {}).get("balance", 0.0)

def update_user_balance(user_id, amount):
    with open(USER_DATA_DB, "r") as f:
        data = json.load(f)
    uid = str(user_id)
    if uid not in data:
        data[uid] = {"balance": 0.0}
    data[uid]["balance"] = round(data[uid]["balance"] + amount, 2)
    with open(USER_DATA_DB, "w") as f:
        json.dump(data, f)

def get_all_users():
    with open(USER_DB, "r") as f:
        return json.load(f)

def add_user(user_id):
    with open(USER_DB, "r") as f:
        users = json.load(f)
    if user_id not in users:
        users.append(user_id)
        with open(USER_DB, "w") as f:
            json.dump(users, f)
    
    with open(USER_DATA_DB, "r") as f:
        data = json.load(f)
    if str(user_id) not in data:
        data[str(user_id)] = {"balance": 0.0}
        with open(USER_DATA_DB, "w") as f:
            json.dump(data, f)

def get_settings():
    with open(SETTINGS_DB, "r") as f:
        return json.load(f)

def save_settings(settings):
    with open(SETTINGS_DB, "w") as f:
        json.dump(settings, f)

def get_withdrawals():
    with open(WITHDRAWALS_DB, "r") as f:
        return json.load(f)

def save_withdrawals(withdraws):
    with open(WITHDRAWALS_DB, "w") as f:
        json.dump(withdraws, f)

def get_active_numbers():
    with open(ACTIVE_NUMBERS_DB, "r") as f:
        return json.load(f)

def save_active_numbers(numbers):
    with open(ACTIVE_NUMBERS_DB, "w") as f:
        json.dump(numbers, f)

def add_active_number(phone, chat_id, service, range_code):
    country_code, country_name, flag = get_country_info_from_range(range_code)
    
    data = get_active_numbers()
    data[str(phone)] = {
        "chat_id": chat_id,
        "service": service,
        "range": range_code,
        "country_code": country_code,
        "country_name": country_name,
        "country_flag": flag,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    save_active_numbers(data)

def remove_active_number(phone):
    data = get_active_numbers()
    if str(phone) in data:
        del data[str(phone)]
        save_active_numbers(data)

# ==================== অ্যাকাউন্ট সাবমিট লিমিট ফাংশন ====================
def get_user_today_submit_count(user_id):
    with open(USER_SUBMIT_LIMIT_DB, "r") as f:
        data = json.load(f)
    
    uid = str(user_id)
    today = datetime.now().strftime("%Y-%m-%d")
    
    if uid not in data:
        return 0
    
    if data[uid].get("date") != today:
        return 0
    
    return data[uid].get("count", 0)

def increment_user_submit_count(user_id):
    with open(USER_SUBMIT_LIMIT_DB, "r") as f:
        data = json.load(f)
    
    uid = str(user_id)
    today = datetime.now().strftime("%Y-%m-%d")
    
    if uid not in data or data[uid].get("date") != today:
        data[uid] = {"date": today, "count": 1}
    else:
        data[uid]["count"] += 1
    
    with open(USER_SUBMIT_LIMIT_DB, "w") as f:
        json.dump(data, f)

def can_user_submit(user_id):
    settings = get_settings()
    daily_limit = settings.get("daily_limit", 10)
    today_count = get_user_today_submit_count(user_id)
    return today_count < daily_limit

# ==================== পেন্ডিং অ্যাকাউন্ট ফাংশন ====================
def add_pending_account(user_id, number, email, password):
    pending = get_pending_accounts()
    account_id = len(pending) + 1
    pending.append({
        "id": account_id,
        "user_id": user_id,
        "number": number,
        "email": email,
        "password": password,
        "status": "pending",
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    save_pending_accounts(pending)
    return account_id

def get_pending_accounts():
    with open(PENDING_ACCOUNTS_DB, "r") as f:
        return json.load(f)

def save_pending_accounts(accounts):
    with open(PENDING_ACCOUNTS_DB, "w") as f:
        json.dump(accounts, f)

def approve_account(account_id):
    pending = get_pending_accounts()
    for acc in pending:
        if acc["id"] == account_id:
            acc["status"] = "approved"
            save_pending_accounts(pending)
            return acc
    return None

def reject_account(account_id):
    pending = get_pending_accounts()
    for acc in pending:
        if acc["id"] == account_id:
            acc["status"] = "rejected"
            save_pending_accounts(pending)
            return acc
    return None

# ==================== OTP নোটিফিকেশন ====================
def send_otp_notification(chat_id, phone, service, otp, message, price, country_name, flag, country_code):
    dm_msg = f"""✅ OTP RECEIVED!
━━━━━━━━━━━━━━━━━━━━
📱 Number: `{phone}`
🎯 Service: {service}
🌍 Country: {country_name} {flag}
━━━━━━━━━━━━━━━━━━━━
🔐 OTP Code: `{otp}`
━━━━━━━━━━━━━━━━━━━━
📩 Full SMS:
`{message[:200]}`
━━━━━━━━━━━━━━━━━━━━
💰 Income: +{price} BDT"""
    
    service_short = "FB" if "facebook" in service.lower() else "IG"
    masked_phone = mask_number_for_group(phone)
    group_msg = f"{flag} {country_code} {service_short} {masked_phone}"
    
    markup = InlineKeyboardMarkup()
    markup.add(ibtn(f"🔐 {otp}", callback_data=f"copy_otp_{otp}", style="primary"))
    
    try:
        bot.send_message(chat_id, dm_msg, parse_mode="Markdown")
        bot.send_message(LOG_GROUP_ID, group_msg, reply_markup=markup)
    except Exception as e:
        print(f"Send error: {e}")

def send_numbers_received_notification(chat_id, numbers, service_name, range_code):
    country_code, country_name, flag = get_country_info_from_range(range_code)
    
    numbers_text = "\n".join([f"✅ `{num}`" for num in numbers])
    
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        ibtn("📢 OTP GROUP", url=OTP_GROUP_URL, style="primary"),
        ibtn("🔄 Change Number", callback_data=f"change_number_{service_name}_{range_code}", style="success")
    )
    markup.add(ibtn("🔙 Back to Services", callback_data="back_to_services", style="danger"))
    
    msg = f"""🎯 Numbers Received!

{flag} {country_code}
{numbers_text}

🎯 Service: {service_name}
🌍 Country: {country_name} {flag}

💡 OTP will appear here automatically!
💰 Earn {get_settings()['otp_price']} BDT per OTP"""
    
    bot.send_message(chat_id, msg, parse_mode="Markdown", reply_markup=markup)

# ==================== কীবোর্ড ====================
def get_main_keyboard(user_id):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = [
        rbtn("🎲 GET NUMBER", style="primary"),
        rbtn("📩 MAIL", style="primary"),
        rbtn("📝 SUBMIT ACCOUNT", style="primary"),
        rbtn("💰 BALANCE", style="success"),
        rbtn("💳 WITHDRAWAL", style="success")
    ]
    if user_id == ADMIN_ID:
        buttons.append(rbtn("🛠 ADMIN PANEL", style="success"))
    
    markup.add(*buttons[:3])
    markup.add(*buttons[3:6])
    if len(buttons) > 6:
        markup.add(*buttons[6:])
    return markup

def get_admin_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = [
        rbtn("📢 BROADCAST", style="primary"),
        rbtn("📊 STATS", style="primary"),
        rbtn("⚙️ PRICE", style="success"),
        rbtn("📂 PENDING", style="success"),
        rbtn("📋 PENDING ACCOUNT", style="primary"),
        rbtn("🔢 LIMIT SET", style="primary"),
        rbtn("🔑 SET PASSWORD", style="primary"),
        rbtn("🔙 BACK", style="danger")
    ]
    markup.add(*buttons)
    return markup

def get_service_keyboard():
    markup = InlineKeyboardMarkup()
    markup.add(ibtn("📘 Facebook + Instagram", callback_data="srv_combined", style="primary"))
    markup.row(ibtn("🔙 Back", callback_data="main_menu", style="danger"))
    return markup

def get_range_keyboard(ranges_data, service_type):
    markup = InlineKeyboardMarkup()
    for i, (raw_range, display_text) in enumerate(ranges_data[:12]):
        style = "primary" if i % 2 == 0 else "success"
        markup.add(ibtn(display_text, callback_data=f"range_{service_type}_{raw_range}", style=style))
    
    markup.add(ibtn("🔄 Refresh", callback_data=f"refresh_{service_type}", style="primary"))
    markup.add(ibtn("🔙 Back to Services", callback_data="back_to_services", style="danger"))
    return markup

# ==================== বট হ্যান্ডলার ====================
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# অ্যাকাউন্ট সাবমিট করার জন্য টেম্প স্টোর
user_submit_data = {}

@bot.message_handler(commands=['start'])
def start(message):
    add_user(message.chat.id)
    if message.from_user.id == ADMIN_ID:
        bot.send_message(message.chat.id, "👋 Welcome Admin!\n🌍 Panel: X-MNIT\n✅ Service: Facebook + Instagram\n✅ 2 Numbers per request\n✅ Country flags on ranges", reply_markup=get_admin_keyboard())
    else:
        bal = get_user_balance(message.chat.id)
        bot.send_message(message.chat.id, 
            f"✨ Welcome {message.from_user.first_name}! ✨\n\n💰 Balance: {bal} BDT\n🌍 Panel: X-MNIT\n✅ Service: Facebook + Instagram\n✅ 2 Numbers per request",
            reply_markup=get_main_keyboard(message.chat.id))

@bot.message_handler(func=lambda m: m.text == "🎲 GET NUMBER")
def handle_get_number(message):
    bot.send_message(message.chat.id, "📱 Select Service:", reply_markup=get_service_keyboard())

@bot.message_handler(func=lambda m: m.text == "📩 MAIL")
def handle_mail(message):
    email = generate_random_email()
    msg_text = f"""📧 <b>Generated Email</b>

┏━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                            ┃
┃      <code>{email}</code>      ┃
┃                            ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━┛

<i>Tap the email to copy</i>"""
    
    bot.send_message(message.chat.id, msg_text, parse_mode="HTML")

@bot.message_handler(func=lambda m: m.text == "📝 SUBMIT ACCOUNT")
def handle_submit_account(message):
    user_id = message.chat.id
    
    # চেক লিমিট
    if not can_user_submit(user_id):
        settings = get_settings()
        bot.send_message(message.chat.id, f"❌ LIMIT OVER!\n\nYou can only submit {settings['daily_limit']} accounts per day.\nPlease try again tomorrow.")
        return
    
    user_submit_data[user_id] = {"step": "number"}
    msg = bot.send_message(message.chat.id, "📱 Please send your NUMBER:")
    bot.register_next_step_handler(msg, process_submit_number)

def process_submit_number(message):
    user_id = message.chat.id
    number = message.text.strip()
    
    if user_id not in user_submit_data:
        user_submit_data[user_id] = {}
    
    user_submit_data[user_id]["number"] = number
    user_submit_data[user_id]["step"] = "email"
    
    msg = bot.send_message(message.chat.id, "📧 Please send your EMAIL:")
    bot.register_next_step_handler(msg, process_submit_email)

def process_submit_email(message):
    user_id = message.chat.id
    email = message.text.strip()
    
    if user_id not in user_submit_data:
        user_submit_data[user_id] = {}
    
    user_submit_data[user_id]["email"] = email
    user_submit_data[user_id]["step"] = "password"
    
    msg = bot.send_message(message.chat.id, "🔐 Please send your PASSWORD:")
    bot.register_next_step_handler(msg, process_submit_password)

def process_submit_password(message):
    user_id = message.chat.id
    password = message.text.strip()
    
    if user_id not in user_submit_data:
        user_submit_data[user_id] = {}
    
    number = user_submit_data[user_id].get("number", "N/A")
    email = user_submit_data[user_id].get("email", "N/A")
    
    # সেভ করে দেওয়া (ইউজারের দেওয়া পাসওয়ার্ড সংরক্ষণ করা হচ্ছে)
    add_pending_account(user_id, number, email, password)
    increment_user_submit_count(user_id)
    
    # টেম্প ডাটা ক্লিয়ার
    del user_submit_data[user_id]
    
    # এডমিনকে নোটিফিকেশন
    bot.send_message(ADMIN_ID, f"📝 New Account Submitted!\nUser: {user_id}\nNumber: {number}\nEmail: {email}\nPassword: {password}")
    
    bot.send_message(message.chat.id, "✅ Account Submitted Successfully!\n\n⏳ Please wait for admin approval.\nYou can submit more accounts.")

@bot.message_handler(func=lambda m: m.text == "💰 BALANCE")
def handle_balance(message):
    bal = get_user_balance(message.chat.id)
    bot.send_message(message.chat.id, f"💰 Balance: `{bal}` BDT", parse_mode="Markdown")

@bot.message_handler(func=lambda m: m.text == "💳 WITHDRAWAL")
def handle_withdraw(message):
    bal = get_user_balance(message.chat.id)
    settings = get_settings()
    if bal < settings["min_withdraw"]:
        bot.send_message(message.chat.id, f"❌ Min withdraw: {settings['min_withdraw']} BDT\nYour balance: {bal} BDT")
    else:
        msg = bot.send_message(message.chat.id, "💳 Enter Bkash number:")
        bot.register_next_step_handler(msg, process_withdraw, bal)

@bot.message_handler(func=lambda m: m.text == "🔙 BACK")
def back_main(message):
    if message.from_user.id == ADMIN_ID:
        bot.send_message(message.chat.id, "🏠 Admin Menu", reply_markup=get_admin_keyboard())
    else:
        bot.send_message(message.chat.id, "🏠 Main Menu", reply_markup=get_main_keyboard(message.chat.id))

@bot.message_handler(func=lambda m: m.text == "🛠 ADMIN PANEL")
def admin_menu(message):
    if message.from_user.id == ADMIN_ID:
        bot.send_message(message.chat.id, "🛠 Admin Panel:", reply_markup=get_admin_keyboard())

def process_withdraw(message, amount):
    bkash = message.text.strip()
    if len(bkash) < 11 or not bkash.isdigit():
        bot.send_message(message.chat.id, "❌ Invalid Bkash number!")
        return
    
    withdrawals = get_withdrawals()
    req_id = len(withdrawals) + 1
    
    new_req = {
        "id": req_id,
        "user_id": message.chat.id,
        "bkash": bkash,
        "amount": amount,
        "status": "pending",
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    withdrawals.append(new_req)
    save_withdrawals(withdrawals)
    update_user_balance(message.chat.id, -amount)
    
    bot.send_message(message.chat.id, f"✅ Withdrawal Request Submitted!\n💰 Amount: {amount} BDT\n📱 Bkash: {bkash}")
    bot.send_message(ADMIN_ID, f"🔔 New Withdrawal!\nUser: {message.chat.id}\nAmount: {amount} BDT\nBkash: {bkash}")

# ==================== এডমিন হ্যান্ডলার ====================
@bot.message_handler(func=lambda m: m.from_user.id == ADMIN_ID and m.text in ["📢 BROADCAST", "📊 STATS", "⚙️ PRICE", "📂 PENDING", "📋 PENDING ACCOUNT", "🔢 LIMIT SET", "🔑 SET PASSWORD"])
def admin_buttons(message):
    if message.text == "📢 BROADCAST":
        msg = bot.send_message(message.chat.id, "📢 Send broadcast message:")
        bot.register_next_step_handler(msg, broadcast_msg)
    
    elif message.text == "📊 STATS":
        users = len(get_all_users())
        active = len(get_active_numbers())
        pending_accounts = len([a for a in get_pending_accounts() if a["status"] == "pending"])
        settings = get_settings()
        bot.send_message(message.chat.id, f"📊 STATS\n👥 Users: {users}\n📱 Active: {active}\n📝 Pending Accounts: {pending_accounts}\n💰 Price: {settings['otp_price']} BDT\n💳 Min: {settings['min_withdraw']} BDT\n🔢 Daily Limit: {settings['daily_limit']}")
    
    elif message.text == "⚙️ PRICE":
        msg = bot.send_message(message.chat.id, "💰 Enter new OTP price:")
        bot.register_next_step_handler(msg, edit_price)
    
    elif message.text == "📂 PENDING":
        pending = [w for w in get_withdrawals() if w["status"] == "pending"]
        if not pending:
            bot.send_message(message.chat.id, "📭 No pending withdrawals!")
            return
        for w in pending:
            markup = InlineKeyboardMarkup()
            markup.row(ibtn("✅ Approve", callback_data=f"approve_{w['id']}", style="success"), 
                      ibtn("❌ Reject", callback_data=f"reject_{w['id']}", style="danger"))
            bot.send_message(message.chat.id, f"📥 REQUEST #{w['id']}\nUser: {w['user_id']}\nAmount: {w['amount']} BDT\nBkash: {w['bkash']}", reply_markup=markup)
    
    elif message.text == "📋 PENDING ACCOUNT":
        pending_accounts = get_pending_accounts()
        pending_list = [a for a in pending_accounts if a["status"] == "pending"]
        
        if not pending_list:
            bot.send_message(message.chat.id, "📭 No pending accounts!")
            return
        
        # ইউজার অনুযায়ী গ্রুপ করুন
        user_accounts = {}
        for acc in pending_list:
            uid = acc["user_id"]
            if uid not in user_accounts:
                user_accounts[uid] = []
            user_accounts[uid].append(acc)
        
        for uid, accounts in user_accounts.items():
            user_info = f"👤 User: `{uid}`\n📝 Accounts: {len(accounts)}"
            markup = InlineKeyboardMarkup()
            markup.add(ibtn(f"View {uid}", callback_data=f"view_user_{uid}", style="primary"))
            bot.send_message(message.chat.id, user_info, parse_mode="Markdown", reply_markup=markup)
    
    elif message.text == "🔢 LIMIT SET":
        msg = bot.send_message(message.chat.id, f"📊 Current daily limit: {get_settings()['daily_limit']}\n\nEnter new daily limit (number of accounts per user per day):")
        bot.register_next_step_handler(msg, edit_limit)
    
    elif message.text == "🔑 SET PASSWORD":
        msg = bot.send_message(message.chat.id, f"🔐 Current admin password: `{ADMIN_SET_PASSWORD}`\n\nEnter new password (this will be sent to users when account is approved):")
        bot.register_next_step_handler(msg, edit_password)

def edit_password(message):
    global ADMIN_SET_PASSWORD
    try:
        new_password = message.text.strip()
        if len(new_password) < 4:
            bot.send_message(message.chat.id, "❌ Password must be at least 4 characters!")
            return
        ADMIN_SET_PASSWORD = new_password
        bot.send_message(message.chat.id, f"✅ Password updated successfully!\n\nNew password: `{ADMIN_SET_PASSWORD}`", parse_mode="Markdown")
    except:
        bot.send_message(message.chat.id, "❌ Invalid input!")

def edit_limit(message):
    try:
        limit = int(message.text.strip())
        if limit <= 0:
            bot.send_message(message.chat.id, "❌ Limit must be greater than 0!")
            return
        settings = get_settings()
        settings["daily_limit"] = limit
        save_settings(settings)
        bot.send_message(message.chat.id, f"✅ Daily limit set to {limit} accounts per user!")
    except:
        bot.send_message(message.chat.id, "❌ Invalid input! Please enter a number.")

def broadcast_msg(message):
    users = get_all_users()
    success = 0
    for uid in users:
        try:
            bot.send_message(uid, f"📢 BROADCAST\n\n{message.text}")
            success += 1
            time.sleep(0.05)
        except:
            pass
    bot.send_message(ADMIN_ID, f"✅ Sent to {success} users!")

def edit_price(message):
    try:
        price = float(message.text)
        settings = get_settings()
        settings["otp_price"] = price
        save_settings(settings)
        bot.send_message(message.chat.id, f"✅ OTP Price set to {price} BDT!")
    except:
        bot.send_message(message.chat.id, "❌ Invalid!")

# ==================== কলব্যাক হ্যান্ডলার ====================
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    chat_id = call.message.chat.id
    msg_id = call.message.message_id
    data = call.data
    
    if data.startswith("copy_otp_"):
        otp_code = data.split("_")[2]
        bot.answer_callback_query(call.id, f"✅ OTP Copied: {otp_code}", show_alert=True)
        return
    
    if data.startswith("view_user_"):
        user_id = int(data.split("_")[2])
        pending_accounts = get_pending_accounts()
        user_accounts = [a for a in pending_accounts if a["user_id"] == user_id and a["status"] == "pending"]
        
        if not user_accounts:
            bot.edit_message_text("No pending accounts for this user!", chat_id, msg_id)
            bot.answer_callback_query(call.id)
            return
        
        # প্রতিটি অ্যাকাউন্ট আলাদাভাবে দেখান
        for acc in user_accounts:
            acc_text = f"""📋 ACCOUNT #{acc['id']}
━━━━━━━━━━━━━━━━━━━━
📱 Number: `{acc['number']}`
📧 Email: `{acc['email']}`
🔐 User Password: `{acc['password']}`
━━━━━━━━━━━━━━━━━━━━
<i>Tap any text to copy</i>"""
            
            markup = InlineKeyboardMarkup(row_width=2)
            markup.add(
                ibtn("✅ APPROVE", callback_data=f"approve_acc_{acc['id']}", style="success"),
                ibtn("❌ REJECT", callback_data=f"reject_acc_{acc['id']}", style="danger")
            )
            bot.send_message(chat_id, acc_text, parse_mode="Markdown", reply_markup=markup)
        
        bot.delete_message(chat_id, msg_id)
        bot.answer_callback_query(call.id)
        return
    
    if data.startswith("approve_acc_"):
        account_id = int(data.split("_")[2])
        account = approve_account(account_id)
        
        if account:
            # ইউজারকে নোটিফিকেশন (এডমিন সেট করা পাসওয়ার্ড সহ)
            msg_text = f"""✅ <b>ACCOUNT APPROVED!</b>

━━━━━━━━━━━━━━━━━━━━
📱 Number: <code>{account['number']}</code>
🔐 Password: <code>{ADMIN_SET_PASSWORD}</code>
━━━━━━━━━━━━━━━━━━━━

<i>Tap any text to copy</i>"""
            
            try:
                bot.send_message(account["user_id"], msg_text, parse_mode="HTML")
            except:
                pass
            
            bot.edit_message_text(f"✅ Account #{account_id} approved and sent to user!\n\nPassword sent: {ADMIN_SET_PASSWORD}", chat_id, msg_id)
        else:
            bot.edit_message_text(f"❌ Account #{account_id} not found!", chat_id, msg_id)
        
        bot.answer_callback_query(call.id)
        return
    
    if data.startswith("reject_acc_"):
        account_id = int(data.split("_")[2])
        account = reject_account(account_id)
        
        if account:
            # ইউজারকে নোটিফিকেশন
            try:
                bot.send_message(account["user_id"], "❌ ACCOUNT NOT VERIFIED!\n\nYour submitted account has been rejected. Please submit valid account.")
            except:
                pass
            
            bot.edit_message_text(f"❌ Account #{account_id} rejected!", chat_id, msg_id)
        else:
            bot.edit_message_text(f"❌ Account #{account_id} not found!", chat_id, msg_id)
        
        bot.answer_callback_query(call.id)
        return
    
    if data == "main_menu":
        bot.delete_message(chat_id, msg_id)
        bot.send_message(chat_id, "🏠 Main Menu", reply_markup=get_main_keyboard(chat_id))
        bot.answer_callback_query(call.id)
        return
    
    if data == "back_to_services":
        bot.edit_message_text("📱 Select Service:", chat_id, msg_id, reply_markup=get_service_keyboard())
        bot.answer_callback_query(call.id)
        return
    
    if data.startswith("refresh_"):
        service_type = data.split("_")[1]
        ranges_data = get_combined_fb_ig_ranges()
        display_name = "Facebook + Instagram"
        
        if ranges_data:
            bot.edit_message_text(f"🔥 Live Ranges for {display_name}:", chat_id, msg_id, 
                                reply_markup=get_range_keyboard(ranges_data, service_type))
        else:
            bot.edit_message_text("❌ No ranges found!", chat_id, msg_id)
        bot.answer_callback_query(call.id)
        return
    
    if data == "srv_combined":
        ranges_data = get_combined_fb_ig_ranges()
        if ranges_data:
            bot.edit_message_text("🔥 Live Ranges for Facebook + Instagram:", chat_id, msg_id, 
                                reply_markup=get_range_keyboard(ranges_data, "combined"))
        else:
            bot.edit_message_text("❌ No ranges found!", chat_id, msg_id, reply_markup=get_service_keyboard())
        bot.answer_callback_query(call.id)
        return
    
    if data.startswith("range_"):
        parts = data.split("_")
        service_type = parts[1]
        range_code = parts[2]
        
        service_name = "Facebook/Instagram"
        
        bot.edit_message_text(f"⏳ Getting 2 numbers from {format_range_with_flag(range_code)}...", chat_id, msg_id, parse_mode="Markdown")
        
        numbers_found = []
        for i in range(2):
            number = xmnit_fetch_number(range_code)
            if number:
                numbers_found.append(number)
                add_active_number(number, chat_id, service_name, range_code)
            time.sleep(0.5)
        
        if numbers_found:
            bot.delete_message(chat_id, msg_id)
            send_numbers_received_notification(chat_id, numbers_found, service_name, range_code)
        else:
            new_ranges = get_combined_fb_ig_ranges()
            bot.edit_message_text(f"❌ No numbers available!\nTry another range.", chat_id, msg_id, 
                                reply_markup=get_range_keyboard(new_ranges, service_type))
        
        bot.answer_callback_query(call.id)
        return
    
    if data.startswith("change_number_"):
        parts = data.split("_")
        service_name = parts[2]
        range_code = parts[3]
        
        bot.delete_message(chat_id, msg_id)
        loading_msg = bot.send_message(chat_id, f"⏳ Getting 2 new numbers...")
        
        numbers_found = []
        for i in range(2):
            number = xmnit_fetch_number(range_code)
            if number:
                numbers_found.append(number)
                add_active_number(number, chat_id, service_name, range_code)
            time.sleep(0.5)
        
        bot.delete_message(chat_id, loading_msg.message_id)
        
        if numbers_found:
            send_numbers_received_notification(chat_id, numbers_found, service_name, range_code)
        else:
            bot.send_message(chat_id, "❌ No numbers available!", reply_markup=get_service_keyboard())
        
        bot.answer_callback_query(call.id)
        return
    
    if data.startswith("approve_"):
        req_id = int(data.split("_")[1])
        withdrawals = get_withdrawals()
        for w in withdrawals:
            if w["id"] == req_id:
                w["status"] = "approved"
                save_withdrawals(withdrawals)
                bot.edit_message_text(f"✅ Approved #{req_id}", chat_id, msg_id)
                try:
                    bot.send_message(w["user_id"], f"✅ Your withdrawal of {w['amount']} BDT has been approved!\nSent to: {w['bkash']}")
                except:
                    pass
                break
        bot.answer_callback_query(call.id)
        return
    
    if data.startswith("reject_"):
        req_id = int(data.split("_")[1])
        withdrawals = get_withdrawals()
        for w in withdrawals:
            if w["id"] == req_id:
                w["status"] = "rejected"
                save_withdrawals(withdrawals)
                update_user_balance(w["user_id"], w["amount"])
                bot.edit_message_text(f"❌ Rejected #{req_id}", chat_id, msg_id)
                try:
                    bot.send_message(w["user_id"], f"❌ Your withdrawal request of {w['amount']} BDT was rejected!\nAmount refunded to balance.")
                except:
                    pass
                break
        bot.answer_callback_query(call.id)
        return

# ==================== OTP মনিটর ====================
sent_otps = set()

def otp_monitor():
    global sent_otps
    print("🔄 X-MNIT OTP Monitor Started")
    while True:
        try:
            settings = get_settings()
            price = settings.get("otp_price", 5.0)
            otps = xmnit_check_otp()
            
            for otp_data in otps:
                phone = otp_data["phone"]
                key = f"{phone}_{otp_data['otp']}"
                
                if key not in sent_otps:
                    sent_otps.add(key)
                    active = get_active_numbers()
                    
                    if str(phone) in active:
                        a = active[str(phone)]
                        update_user_balance(a["chat_id"], price)
                        send_otp_notification(a["chat_id"], phone, a["service"], otp_data["otp"], 
                                             otp_data["message"], price, a["country_name"], 
                                             a["country_flag"], a["country_code"])
                        remove_active_number(phone)
                        print(f"📱 OTP Received: {phone} | {a['service']} | {otp_data['otp']}")
            
            if len(sent_otps) > 1000:
                sent_otps.clear()
                
        except Exception as e:
            print(f"Monitor Error: {e}")
        time.sleep(5)

# ==================== মেইন ====================
if __name__ == "__main__":
    print("=" * 60)
    print("🤖 X-MNIT OTP BOT (Facebook + Instagram Only)")
    print("=" * 60)
    print("✅ Service: Facebook + Instagram")
    print("✅ Countries: All 240+ countries supported")
    print("✅ Auto-detect country from range prefix")
    print("✅ 2 Numbers per request")
    print("✅ MAIL Generator - Random email every time")
    print("✅ SUBMIT ACCOUNT - User can submit accounts (Number + Email + Password)")
    print("✅ Admin can approve/reject accounts with their own password")
    print("✅ Daily limit system for account submission")
    print("=" * 60)
    
    settings = get_settings()
    print(f"💰 OTP Price: {settings['otp_price']} BDT")
    print(f"💳 Min Withdraw: {settings['min_withdraw']} BDT")
    print(f"🔢 Daily Limit: {settings['daily_limit']} accounts/user")
    print(f"🔐 Admin Password: {ADMIN_SET_PASSWORD}")
    
    print("\n🔍 Logging in...")
    if xmnit_login():
        print("✅ Login Successful!")
    else:
        print("⚠️ Login Failed - check credentials")
    
    print("\n🤖 Bot Starting...")
    threading.Thread(target=otp_monitor, daemon=True).start()
    
    print("✅ Bot Running!")
    print("=" * 60)
    
    bot.infinity_polling(timeout=60)
