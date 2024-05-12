from enum import IntEnum


class Allow(IntEnum):
    """
    Describes whether to allow or deny an action.
    """

    ALLOW = 0
    """
    Allow an action.
    """

    ALLOW_WITH_WARNING = 1
    """
    Allow an action, but log a warning.
    """

    DENY = 2
    """
    Deny an action.
    """


ALLOWS = [
    Allow.ALLOW,
    Allow.ALLOW_WITH_WARNING,
]
"""
All the Allow enum values that indicate that an action is allowed.
"""
