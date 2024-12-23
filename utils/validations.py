import re
from typing import List


def validate_password(
    password: str,
    confirm_password: str = '',
    check_confirm_password: bool = True,
) -> bool:
    if check_confirm_password:
        if password != confirm_password:
            return False

    if len(password.strip()) < 8:
        return False

    if not re.search(r'[a-z]', password):
        return False

    if not re.search(r'[A-Z]', password):
        return False

    if not re.search(r'[0-9]', password):
        return False

    if not re.search(r'[!,@,&,*,%,$,#]', password):
        return False

    return True


def validated_fields_schemas(*args: List[str], values: dict):
    for field in args:
        if values.get(field) is None:
            continue
        if not values.get(field):
            raise ValueError(f'{field} cannot be empty')

    return values