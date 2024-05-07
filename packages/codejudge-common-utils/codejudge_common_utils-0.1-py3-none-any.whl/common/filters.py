import json
from enum import Enum

import jinja2
from rest_framework import status
from dateutil import parser

from restapi.common.date_time_util import DateTimeUtil
from restapi.common.enums import RunStatus, CodeSubmissionStatus, QuestionSubTypes, SubjectiveCustomFieldTypes
from restapi.common.html_util import HtmlUtil
from restapi.common.json_util import JsonUtil
from restapi.common.list_util import ListUtil
from restapi.common.map_util import MapUtil
from restapi.common.string_util import StringUtil
from restapi.exception.exception import RecruitException


class TemplateFilter(object):

    def register_templates(self):
        jinja2.filters.FILTERS['divide'] = divide
        jinja2.filters.FILTERS['convert_seconds'] = convert_seconds
        jinja2.filters.FILTERS['integer'] = integer
        jinja2.filters.FILTERS['percent'] = percent
        jinja2.filters.FILTERS['sum'] = sum
        jinja2.filters.FILTERS['to_pretty_json'] = to_pretty_json
        jinja2.filters.FILTERS['timestamp'] = timestamp
        jinja2.filters.FILTERS['transform_pre_text'] = transform_pre_text
        jinja2.filters.FILTERS['list_valid'] = list_valid
        jinja2.filters.FILTERS['float_integer'] = float_integer
        jinja2.filters.FILTERS['str_not_empty'] = str_not_empty
        jinja2.filters.FILTERS['arr_not_empty'] = arr_not_empty
        jinja2.filters.FILTERS['project_submission_status'] = project_submission_status
        jinja2.filters.FILTERS['programming_submission_status'] = programming_submission_status
        jinja2.filters.FILTERS['time_spent'] = time_spent
        jinja2.filters.FILTERS['best_score'] = best_score
        jinja2.filters.FILTERS['quality_score'] = best_score
        jinja2.filters.FILTERS['plagiarism_status'] = plagiarism_status
        jinja2.filters.FILTERS['language_validity_check'] = language_validity_check
        jinja2.filters.FILTERS['score_class'] = score_class
        jinja2.filters.FILTERS['compliance_score_key'] = compliance_score_key
        jinja2.filters.FILTERS['convert_code_to_json'] = convert_code_to_json
        jinja2.filters.FILTERS['get_submission_detail_keys'] = get_submission_detail_keys
        jinja2.filters.FILTERS['get_subjective_custom_field_types'] = SubjectiveCustomFieldTypes.get_subjective_custom_field_types
        jinja2.filters.FILTERS['check_for_none_for_subjective'] = check_for_none_for_subjective
        jinja2.filters.FILTERS['get_fields_from_submission_details'] = get_fields_from_submission_details
        jinja2.filters.FILTERS['get_true_options_for_checkbox'] = get_true_options_for_checkbox
        jinja2.filters.FILTERS['get_link_for_diagram_and_whiteboard'] = get_link_for_diagram_and_whiteboard
        jinja2.filters.FILTERS['get_text_for_subj'] = get_text_for_subj
        jinja2.filters.FILTERS['get_link_for_proctor_tab'] = get_link_for_proctor_tab


def divide(value, arg):
    try:
        if int(arg) != 0:
            return int(value) / int(arg)

        raise RecruitException('Denominator can\'t be zero!', status=status.HTTP_400_BAD_REQUEST)
    except (ValueError, ZeroDivisionError):
        return None


def percent(value, arg):
    ans = divide(value, arg)
    return ans * 100


def sum(value, arg):
    return value + arg


def convert_seconds(value):
    return DateTimeUtil.convert_seconds_test_pdf(value)


def time_spent(value):
    if value is not None:
        return convert_seconds(value)
    return "-"


def best_score(value):
    if MapUtil.check_if_map_has_key(value, 'best_score') and value['best_score'] != 'NA':
        return "{}/{}".format(value['best_score'], integer(value['points']))
    return "-"


def quality_score(value):
    if MapUtil.check_if_map_has_key(value, 'is_quality_present') and value['is_quality_present'] \
            and MapUtil.check_if_map_has_key(value, 'best_quality_score') and (value['best_quality_score'] is not None or value['best_quality_score'] != 'NA') \
            and MapUtil.check_if_map_has_key(value, 'total_quality_score') and (value['total_quality_score'] is not None or value['total_quality_score'] != 'NA'):
        return "{}/{}".format(value['best_quality_score'], value['total_quality_score'])
    return "-"


def integer(value):
    return int(value)


def to_pretty_json(value):
    return json.dumps(value, sort_keys=True,
                      indent=4, separators=(',', ': '))


def timestamp(value):
    return parser.parse(value).strftime('%d %b %Y, %I: %M %p %Z')


def transform_pre_text(text):
    text = '\n' + text
    text = HtmlUtil.html_escape(text)
    return text.replace('\n', '\n&emsp;&emsp;')


def list_valid(value):
    return ListUtil.is_valid(value)


def string(value):
    return str(value)


def float_integer(value):
    return int(float(value))


def str_not_empty(value):
    value = StringUtil.trim(value)
    response = int(value is not None and len(value) > 0)
    return response


def arr_not_empty(value):
    return ListUtil.is_valid(value)


def project_submission_status(value):
    return RunStatus.get_display_value_from_value(int(value))


def programming_submission_status(value):
    return CodeSubmissionStatus.get_display_value_from_value(int(value))


def language_validity_check(value):
    return int(value is not None and len(value) > 0 and value != "-")


def plagiarism_status(value):
    return None


def score_class(value):
    if value is not None:
        value = int(value)
        if 80 < value <= 100:
            return "high-score"
        elif 60 < value <= 80:
            return "high-mid-score"
        elif 40 < value <= 60:
            return "mid-score"
        elif 20 < value <= 40:
            return "mid-low-score"
        elif 0 < value <= 20:
            return "low-score"
        else:
            return "not-attempted"
    else:
        return "not-attempted"


def compliance_score_key(functionality_per):
    if functionality_per is not None:
        value = functionality_per
        if 68.75 < value <= 100:
            return "extremely unlikely"
        elif 31.25 < value <= 68.75:
            return "uncertain"
        elif 0 < value <= 31.25:
            return "extremely likely"
        else:
            return None
    else:
        return None


def convert_code_to_json(code):
    if JsonUtil.is_valid(code):
        code = JsonUtil.convert_json_to_dict(code)
    return code


def get_submission_detail_keys(submission_details):
    try:
        return submission_details.keys()
    except (KeyError, TypeError):
        return None


def check_for_none_for_subjective(data):
    try:
        if data is None or (isinstance(data, str) and str_not_empty(data) == 0):
            return "-"
        return data
    except (KeyError, TypeError):
        return None


def get_fields_from_submission_details(question):
    metadata = question['metadata']
    fields = []
    if MapUtil.check_if_map_has_key(metadata, 'form') and metadata['form']:
        forms = metadata['form']
        for form in forms:
            if MapUtil.check_if_map_has_key(form, 'fields') and form['fields']:
                fields = form['fields']
                break
    else:
        fields.extend(QuestionSubTypes.get_ques_sub_types_info(question['fileUploadType']))
    return fields


def get_true_options_for_checkbox(candidate_options, recruiter_options):
    num_of_true_options = 0
    true_options_str = ""
    true_options_list = []
    for index, option in enumerate(candidate_options):
        if option is True:
            true_options_str += recruiter_options[index]
            true_options_list.append(recruiter_options[index])
            num_of_true_options += 1
    if num_of_true_options > 1:
        true_options_str = ', '.join(true_options_list)
    return true_options_str


def get_link_for_diagram_and_whiteboard(report_path_url, question_id):
    report_path_url += "/?tab=1&ques_id={}".format(question_id)
    return report_path_url


def get_link_for_proctor_tab(report_path_url):
    report_path_url += "/?tab=3"
    return report_path_url


def get_text_for_subj(field_type):
    if field_type in SubjectiveCustomFieldTypes.FILE.value:
        return "Download File"
    if field_type in SubjectiveCustomFieldTypes.VOICE.value:
        return "Download Audio Recording"
    if field_type in SubjectiveCustomFieldTypes.VIDEO.value:
        return "Download Video Recording"
