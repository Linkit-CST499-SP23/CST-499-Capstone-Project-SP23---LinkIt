import re

"""
The get_confidence_score() function takes in a csv column passed in as a list
and returns a confidence score for how likely the column is to made up of credit
card numbers.

input: string list
output: double

"""


def get_confidence_score(col):
    scores = []
    col = remove_whitespace(col)
    col = remove_null(col)

    for elem in col:
        scores.append(get_elem_score(elem))

    return sum(scores) / len(scores)


"""
The get_elem_score() function takes a number as a string
and returns a confidence score for how likely it is to be
a valid credit card number

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
    if is_valid_card_number:
        return 75.0
    if is_expected_length:
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
    # Card numbers in the U.S. aren't more than 16 digits long
    if len(elem) > 16:
        return False

    # American Express
    if (match := re.search("^3[47]", elem)) is not None:
        return len(elem) == 15
    # Diner Club Carte Blanche
    elif (match := re.search("(^30[0-5])| (^36) | (^38)", elem)) is not None:
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
    elif (match := re.search("(^2123) | (^1800)", elem)) is not None:
        return len(elem) == 15
    # JCB
    elif (match := re.search("^3", elem)) is not None:
        return len(elem) == 16
    else:
        return False


"""
The check_valid_card_number() function checks whether a credit card number is valid.
Since Luhn's algorith can be applied to the credit card numbers to check
whether it is a valid number all credit cards should be able to be
validated this way.

input: string
output: boolean
"""


def check_valid_card_number(number):
    sum = 0
    double = False

    for n in range(len(number), 0):
        if double:
            doubled = str(int(number[n]) * 2)
            for digit in doubled:
                sum += int(digit)
        else:
            sum += int(number[n])
        double = not double
    return (sum % 10) == 0


"""
The remove_whitespace() function removes any leading, trailing, and inner whitespace
that may be in the strings of the column list.

input: string list
output: string list

"""


def remove_whitespace(col):
    return [''.join(elem.split()) for elem in col]  # remove all white space from each element


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
