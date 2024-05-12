class QFlowException(Exception):
    """
    This class is used to raise exceptions in the moovs/sports package.
    """

    def __init__(self, message: str):
        """
        Initialize the SportsException class.
        """
        super().__init__(message)


class VideoTooSmallException(QFlowException):
    """
    This class is used when the video is too small.
    """

    def __init__(self):
        """
        Initialize the VideoTooSmallException class.
        """

        super().__init__(message=f"Video has no content.")
