import re
from datetime import datetime

from allauth.account.models import EmailAddress
from openai import OpenAI

from hn_jobs.utils import get_tjalerts_logger

client = OpenAI()

from .constants import GENERIC_KEYWORDS
from .models import Technology, Title

logger = get_tjalerts_logger(__name__)

list_of_expected_keys = [
    "company_name",
    "job_titles",
    "locations",
    "cities",
    "countries",
    "compensation_summary",
    "is_remote",
    "remote_timezones",
    "is_onsite",
    "capacity",
    "description",
    "technologies_used",
    "company_homepage_link",
    "emails",
    "company_job_application_link",
    "names_of_the_contact_person",
    "years_of_experience",
    "levels_of_experience",
]


def clean_job_json_object(original_comment: dict, nlp_data: dict) -> dict:
    nlp_data = make_sure_all_keys_exists(nlp_data, list_of_expected_keys)

    for key, value in nlp_data.items():
        nlp_data[key] = if_value_is_unknown_return_empty_string(value)

    nlp_data["years_of_experience"] = check_years_of_experience_value(
        nlp_data["years_of_experience"], original_comment["text"]
    )

    nlp_data["original_text"] = original_comment["text"]

    check_boolean_value(nlp_data["is_remote"])
    check_boolean_value(nlp_data["is_onsite"])

    if not has_number(nlp_data["compensation_summary"]):
        nlp_data["min_salary"] = 0
        nlp_data["max_salary"] = 0

    return nlp_data


def check_years_of_experience_value(years: int, text: str):
    """Python function to check that the estimated years of experience appears in the text."""
    if str(years) in text and isinstance(years, int):
        return years
    else:
        return ""


def if_value_is_unknown_return_empty_string(value: str) -> str:
    if value in ["Unknown", "unknown", "empty", "not specified", "N/A", "null", "None", None]:
        return ""
    else:
        return value


def sort_dates(dates):
    """
    Sorts a list of dates in ascending order.
    """
    date_format = "%B %Y"
    sorted_dates = sorted(dates, key=lambda x: datetime.strptime(x, date_format))
    return sorted_dates


def check_boolean_value(boolean_value: any) -> bool:
    if isinstance(boolean_value, bool) or boolean_value in [
        "True",
        "true",
        "Yes",
        "yes",
    ]:
        return boolean_value
    else:
        return False


def make_sure_all_keys_exists(data: dict, keys: list) -> dict:
    for key in keys:
        try:
            data[key]
        except KeyError:
            data[key] = ""

    return data


def fix_email(email):
    """
    Fixes common misspellings of email addresses and returns the corrected email.
    """
    email = email.lower()
    email = (
        re.sub(r"\s+at\s+", "@", email)
        .replace(" [at] ", "@")
        .replace("[at]", "@")
        .replace(" at ", "@")
        .replace("(at)", "@")
        .replace("(a)", "@")
        .replace("[@]", "@")
        .replace("{@}", "@")
        .replace("-at-", "@")
        .replace("<at>", "@")
        .replace(" at:", "@")
        .replace("'at'", "@")
        .replace("_at_", "@")
        .replace(" dot ", ".")
        .replace("<dot>", ".")
        .replace(" [dot] ", ".")
        .replace("(dot)", ".")
        .replace("[dot]", ".")
        .replace(" dot:", ".")
        .replace(" dot;", ".")
        .replace("-dot-", ".")
        .replace("_dot_", ".")
        .replace("'dot'", ".")
        .replace(";", ".")
        .replace(",", ".")
        .replace(" ", "")
        .replace(":", ".")
    )
    return email


def is_generic(email: str) -> bool:
    """
    Returns True if the email address is generic, False otherwise.
    A generic email is defined as an email that has a generic local part
    such as 'jobs', 'apply', etc.
    """

    return email.split("@")[0].lower() in GENERIC_KEYWORDS


def has_number(input_string):
    return any(char.isdigit() for char in input_string)


def get_embedding(text):
    text = text.replace("\n", " ")

    embedding = client.embeddings.create(input=[text], model="text-embedding-3-small")

    return embedding.data[0].embedding


def default_alert_name(alert, idx):
    if "technologies" in alert.filter and len(alert.filter) == 1 and alert.filter["technologies"][0]:
        return f"{Technology.objects.get(id=alert.filter['technologies'][0]).name} Alert"
    else:
        return alert.name if alert.name else f"Alert #{idx+1}"


def remove_params_for_filters(params):
    try:
        del params["o"]
    except KeyError:
        pass

    try:
        del params["page"]
    except KeyError:
        pass

    return params


def is_email_confirmed(user):
    try:
        email_address = EmailAddress.objects.get(user=user, email=user.email)
        return email_address.verified
    except EmailAddress.DoesNotExist:
        return False


def generate_job_search_title(query_params, first_item_datetime):
    date = first_item_datetime.strftime("%B %Y")
    if len(query_params) > 1 or len(query_params) == 0:
        return f"Available Jobs - {date}"

    query_param = list(query_params.keys())[0]

    if query_param == "technologies":
        technologies_list = query_params.getlist("technologies")
        if len(technologies_list) == 1:
            tech_name = Technology.objects.get(id=query_params.getlist("technologies")[0]).name
            return f"{tech_name} Jobs - {date}"

    if query_param == "titles":
        titles_list = query_params.getlist("titles")
        if len(titles_list) == 1:
            title_name = Title.objects.get(id=query_params.getlist("titles")[0]).name
            return f"{title_name} Jobs - {date}"

    if query_param == "locations":
        return f"Jobs in {query_params['locations']} - {date}"

    if query_param == "compensation_summary__isempty":
        compensation_summary = query_params["compensation_summary__isempty"]
        return f"Jobs with {'no' if compensation_summary == 'false' else ''} Comp Info - {date}"

    if query_param == "emails__isempty":
        emails = query_params["emails__isempty"]
        return f"Jobs with {'no' if emails == 'false' else ''} Contact Info - {date}"

    if query_param == "is_remote":
        is_remote = query_params["is_remote"]
        return f"{'Remote' if is_remote == 'true' else ''} Jobs - {date}"

    if query_param == "is_onsite":
        is_onsite = query_params["is_onsite"]
        return f"{'Onsite' if is_onsite == 'true' else ''} Jobs - {date}"

    return f"Available Jobs - {date}"


def generate_job_search_keywords(query_params):
    keywords = []

    for key in query_params.keys():
        if key == "technologies":
            technologies_list = query_params.getlist("technologies")
            for tech_id in technologies_list:
                keywords.append(Technology.objects.get(id=tech_id).name)

        if key == "titles":
            titles_list = query_params.getlist("titles")
            for title_id in titles_list:
                keywords.append(Title.objects.get(id=title_id).name)

        if key == "locations":
            keywords.append(query_params["locations"])

        if key == "compensation_summary__isempty" and query_params["compensation_summary__isempty"] == "true":
            keywords.append("Compensation Information")

        if key == "emails__isempty" and query_params["emails__isempty"] == "true":
            keywords.append("Contact Information")

        if key == "is_remote" and query_params["is_remote"] == "true":
            keywords.append("Remote")

        if key == "is_onsite" and query_params["is_onsite"] == "true":
            keywords.append("Onsite")

    return keywords
