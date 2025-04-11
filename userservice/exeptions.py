class UserAlreadyHasEmailException(Exception):
    detail = "User already has an email address"


class UserEmailNotFoundException(Exception):
    detail = "User not found"


class UserNotCorrectPasswordException(Exception):
    detail = "User not correct password"


class UserAlreadyLoggedException(Exception):
    detail = "User is already logged in"


class UserAccountDeleted(Exception):
    detail = "Account is deleted"