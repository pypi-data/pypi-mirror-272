from recompose.enums import Allow


class Options:
    """
    Recomposition options.

    `missing_data` describes whether missing data should be accepted or raise
    `PathNotFound`.
    """

    def __init__(
        self,
        missing_data: Allow = Allow.DENY,
    ) -> None:
        self.missing_data = missing_data
