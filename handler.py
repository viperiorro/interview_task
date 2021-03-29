"""
Requirements:
    Input event must contain FirstName and LastName parameters, if it does not contain them raise exception.
    FirstName and LastName parameters can't contain any numbers. If any of them contains raise exception.
    Response contains FullName parameter matching following pattern: "<FirstName> <LastName>".
    Regardless of the input FirstName and LastName, FullName must be capitalized (ivan IVANOV -> Ivan Ivanov)

    Input event can contain Age parameter.
    Age parameter must be integer. Age cannot be less than 0
    Response contains AgeGroup parameter generated according to age:
        ..-10 - Child
        11-20 - Teenager
        20-.. - Adult

Event structure:
{
    'FirstName': 'str',
    'LastName': 'str',
    'Age': 'int'
}

Response structure:
{
    'FullName': 'str',
    'AgeGroup': 'str'
}

Event example:
{
    "FirstName": "Ivan",
    "LastName": "Ivanov",
    "Age": 18
}

Response example:
{
    'FullName': 'Ivan Ivanov',
    'AgeGroup': 'Teenager'
}
"""
import re

from exceptions import FirstNameNotFound, LastNameNotFound, InvalidParameterPattern, InvalidParameterType, \
    InvalidParameterValue


def execute(event):
    # Get parameters
    first_name = event.get('FirstName')
    last_name = event.get('LastName')
    age = event.get('Age')

    # Validate parameters
    if not first_name:
        raise FirstNameNotFound
    if not last_name:
        raise LastNameNotFound

    if not isinstance(first_name, str):
        raise InvalidParameterType('FirstName', 'str')
    if not isinstance(last_name, str):
        raise InvalidParameterType('LastName', 'str')

    if re.search(r'\d', first_name):
        raise InvalidParameterType('FirstName', 'str')
    if re.search(r'\d', last_name):
        raise InvalidParameterPattern('LastName')

    # Make first name and last name capitalized
    first_name = first_name.capitalize()
    last_name = last_name.capitalize()

    # Generate response
    full_name = f'{first_name} {last_name}'

    if age:
        age_group = get_age_group(age)
    else:
        age_group = 'Unknown'

    # return response
    return {'FullName': full_name, 'AgeGroup': age_group}


def get_age_group(age):
    if age < 1:
        raise InvalidParameterValue('Age', 'Age cannot be less than 0')
    elif age < 10:
        return 'Child'
    elif 10 < age < 20:
        return 'Teenager'
    elif age >= 20:
        return 'Adult'

