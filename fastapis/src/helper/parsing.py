'''Validate Excel file'''
import secrets
import re
import string
import sys
import importlib.util
import openpyxl


class ValidationResult():
    '''Excel Validation result'''

    def __init__(self, status=False, message=''):
        self.status = status
        self.message = message
        self.err = {}


def gensym(length=32, prefix="gensym_"):
    """
    generates a fairly unique symbol, used to make a module name,
    used as a helper function for load_module

    :return: generated symbol
    """
    alphabet = string.ascii_uppercase + string.ascii_lowercase + string.digits
    symbol = "".join([secrets.choice(alphabet) for i in range(length)])

    return prefix + symbol


def load_module(source, module_name=None):
    """
    reads file source and loads it as a module

    :param source: file to load
    :param module_name: name of module to register in sys.modules
    :return: loaded module
    """

    if module_name is None:
        module_name = gensym()

    spec = importlib.util.spec_from_file_location(module_name, source)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)

    return module


def load_config(method):
    '''Load excel validation config'''
    config_filename = f"{method}_config"
    return load_module(f"/code/fastapis/config/{config_filename}.py")


def validate_file_struct(file_path, method, excel_data_df, headerlive):
    '''Validate the file structure'''
    config = load_config(method)

    if headerlive != config.HEADER:
        return False

    env_columns = [col for col in config.HEADER.split('|') if col]

    if excel_data_df.shape[1] != len(env_columns) or \
            not validate_excel_structure(file_path, config.SHEETNAME):
        return False

    return True


def validate_parsed(file_path, method, excel_data_df, headerlive):
    '''Validate the parsed excel file'''
    validation_results = ValidationResult()
    config = load_config(method)
    cached_structure_validation = True
    if headerlive != config.HEADER:
        validation_results.message = "invalid method or structure"
        return validation_results

    env_columns = [col for col in config.HEADER.split('|') if col]
    limit = len(excel_data_df[excel_data_df.columns[0]]) \
        - config.IGNORE_LAST_ROWS

    if not cached_structure_validation or \
            excel_data_df.shape[1] != (len(env_columns) + 1):
        if not validate_excel_structure(file_path, config.SHEETNAME):
            validation_results.message = "invalid method or structure"
            return validation_results
        cached_structure_validation = True

    for i, col in enumerate(env_columns):
        if i == config.COLS - config.IGNORE_LAST_COLS \
                or i == config.IGNORE_COL:
            continue
        if col in config.BIG_COLS:
            validation_results.err[col] = validate_data_big(
                excel_data_df, excel_data_df.columns[i],
                limit, config.get_max_len(col))
        elif col in config.REGEXES:
            regex = config.REGEXES[col]
            if regex:
                validation_results.err[col] = validate_data(
                    excel_data_df, excel_data_df.columns[i], regex,
                    limit, config.get_max_len(col))

    validation_results.status = not any(
        bool(val) is False for val in validation_results.err.values())

    return validation_results


def validate_data(df, col_name, pattern, limit, maxlen):
    '''Apply regex to all data y column'''
    # regex = regex[2:-1]
    # pattern = re.compile(regex)
    data = df[col_name][:limit]
    r = all(map(lambda x: bool(
        pattern.match(str(x)))
        and len(str(x)) <= maxlen, data))
    return r


def validate_data_big(df, col_name, limit, maxlen):
    '''Apply regex to all data y column'''
    # regex = regex[2:-1]
    # pattern = re.compile(regex)
    data = df[col_name][:limit]
    r = all(map(lambda x: bool(
        is_safe_string(str(x)))
        and len(str(x)) < maxlen, data))
    return r


def validate_excel_structure(file_path, sheetname):
    '''validate the excel general structure'''
    try:
        wb = openpyxl.load_workbook(file_path)
        if sheetname not in wb.sheetnames:
            return False
        return True
    except openpyxl.utils.exceptions.InvalidFileException:
        return False


# Define a regular expression pattern to validate against script tags
unsafe_patterns = {
    # pylint: disable=line-too-long
    "script": re.compile(r'<script[^>]*>([^<]*)</script>', re.IGNORECASE),
    # pylint: disable=line-too-long
    "xss": re.compile(r'''(<script[^>]*>([^<]*)</script>|javascript:[^ ]+)''', re.IGNORECASE),  # noqa: E501
    # pylint: disable=line-too-long
    "command": re.compile(r'(\bbash\b|\bsh\b|\bcmd\b|\bpowershell\b|\bperl\b|\bphp\b|\.\./|[|&;]|[`"])', re.IGNORECASE),  # noqa: E501
    "sql": re.compile(r"(?:\b(SELECT|INSERT|UPDATE|DELETE|EXECUTE|EXEC|DROP|ALTER|CREATE|SHOW TABLES|SHOW DATABASES)\b)", re.IGNORECASE),  # noqa: E501
}


def is_safe_string(input_str):
    """Check if the given input string is safe \
    based on the defined unsafe patterns."""

    # Iterate through each pattern and check if \
    # there is a match in the input string
    # pylint: disable=unused-variable
    for pattern, regex in unsafe_patterns.items():
        if regex.search(input_str):
            return False

    # If no unsafe patterns are found, the input string is considered safe
    return True
