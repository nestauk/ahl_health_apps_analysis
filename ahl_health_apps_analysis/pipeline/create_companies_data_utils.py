import re
from urllib import parse

urls_to_remove = [
    "facebook.com",
    "u3asites.org.uk",
    "sites.google.com",
    "",
    "N/A",
    " N/A",
    "no.website",
    "None",
    ".none",
    "n.a",
    "not.applicable",
]


def charity_url_clean(url):
    if "http" not in url:
        url = url.replace("www.", "https://")
    parsed_url = parse.urlparse(url)
    if parsed_url.netloc:
        new_url = parsed_url.netloc
        new_url = new_url.replace("www.", "")
    else:
        new_url = parsed_url.path

    if new_url in urls_to_remove:
        return None
    else:
        return new_url.lower()


company_stop_words = set(
    [
        "limited",
        "inc",
        "llc",
        "ltd",
        "apps",
        "co",
        "the",
        "services",
        "management",
        "company",
        "uk",
        "c",
        "llp",
        "lp",
        "international",
        "group",
        "cic",
        "plc",
    ]
)

clean_dict = {
    "nbcuniversal media": "nbcuniversal",
    "amazon mobile": "amazon",
    "garmin": "garmin europe",
    "uber technologies": "uber london",
}


def clean_function(name):
    name = str(name)
    name = re.sub(r"[^\w\s]", "", name)
    name = " ".join(name.split())  # sort out double spaces and trailing spaces
    name = name.lower()

    # Found using the most common words
    words = [word for word in name.split() if word not in company_stop_words]
    name = " ".join(words)

    # App specific cleaning
    if name in clean_dict:
        name = clean_dict[name]

    return name
