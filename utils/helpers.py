import string
import random


def get_random_string(fmt: str = "LLLLLLNNN") -> str:
    result = []
    for f in fmt:
        match f:
            case "L":
                result.append(random.choice(string.ascii_uppercase))
            case "N":
                result.append(random.choice(string.digits))
    return "".join(result)
