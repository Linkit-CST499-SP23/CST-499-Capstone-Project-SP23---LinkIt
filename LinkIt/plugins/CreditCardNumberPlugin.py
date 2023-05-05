import re

"""
The get_confidence_score() function takes in a csv column passed in as a list
and returns a confidence score for how likely the column is to made up of credit
card numbers.

input: string list
output: double

"""


def get_confidence_score(col_name, col):
    scores = []
    col = remove_null(col)
    col = remove_delimiters(col)

    if len(col) == 0:
        return 0.0

    col_name = col_name.lower()
    if "ccn" in col_name or "credit" in col_name or "card" in col_name:
        col_name_score_multiplier = 1.15
    else:
        col_name_score_multiplier = 1.0

    for elem in col:
        scores.append(get_elem_score(elem))

    confidence_score = min((sum(scores) / len(scores) * col_name_score_multiplier), 100.0)

    return confidence_score


"""
The get_elem_score() function takes a number as a string
and returns a confidence score for how likely it is to be
a valid credit card number.

input: string
output: double

"""


def get_elem_score(elem):
    # A card number should only be made up of digits
    if not elem.isdigit():
        return 0.0

    is_expected_length = matches_expected_length(elem)
    is_valid_card_number = check_valid_card_number(elem)

    if is_expected_length and is_valid_card_number:
        return 100.0
    elif is_valid_card_number:
        return 75.0
    elif is_expected_length:
        return 25.0
    else:
        return 0.0


"""
The is_expected_length() function takes one element from the column list and
returns whether the number is the expected length based on the fact that the
length of a credit card number varies depending on what brand of credit card it is.

Source for expected lengths of different credit card brands:
https://www.ibm.com/docs/en/order-management-sw/9.3.0?topic=cpms-handling-credit-cards

input: string
output: boolean

"""


def matches_expected_length(elem):
    # American Express
    if (match := re.search("^3[47]", elem)) is not None:
        return len(elem) == 15
    # Diner Club Carte Blanche
    elif (match := re.search("^30[0-5]|^36|^38", elem)) is not None:
        return len(elem) == 14
    # MasterCard
    elif (match := re.search("^5[1-5]", elem)) is not None:
        return len(elem) == 16
    # Visa
    elif (match := re.search("^4", elem)) is not None:
        return len(elem) == 13 or len(elem) == 16
    # Discover
    elif (match := re.search("^6011", elem)) is not None:
        return len(elem) == 16
    # JCB
    elif (match := re.search("^2123|^1800", elem)) is not None:
        return len(elem) == 15
    # JCB
    elif (match := re.search("^3", elem)) is not None:
        return len(elem) == 16
    else:
        return False


"""
The check_valid_card_number() function checks whether a credit card number is
valid. Since Luhn's algorith can be applied to the credit card numbers to check
whether it is a valid number all credit cards should be able to be
validated this way.

input: string
output: boolean
"""


def check_valid_card_number(number):
    # Card numbers in the U.S. aren't more than 16 digits
    # long or shorter than 13 digits
    if len(number) > 16 or len(number) < 13:
        return False

    number_sum = 0
    double = False

    for n in range(len(number) - 1, -1, -1):
        if double:
            doubled = str(int(number[n]) * 2)
            for digit in doubled:
                number_sum += int(digit)
        else:
            number_sum += int(number[n])
        double = not double

    return (number_sum % 10) == 0


"""
The remove_delimiters() function removes any delimiters that would typically
found as part of a credit card number as well as leading and trailing
whitespace for all elements of the column.

input: string list
output: string list

"""


def remove_delimiters(col):
    delimiters = [" ", "-", "."]
    new_col = []

    for string in col:
        new_str = string.strip()
        for i in delimiters:  # replace each delimiter in turn with a space
            new_str = new_str.replace(i, '')
        new_col.append(new_str)

    return new_col


"""
The remove_null() function removes any null elements that may be in the column list.

input: string list
output: string list

"""


def remove_null(col):
    null_strings = ['NA', 'N/A', 'na', 'n/a', 'Na', 'N/a']
    col = [elem for elem in col if elem is not None]  # remove None values
    col = [elem for elem in col if elem not in null_strings]  # remove any strings denoting null values
    return col
