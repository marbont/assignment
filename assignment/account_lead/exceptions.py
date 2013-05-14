class TBDBException(Exception):
    """Exception raised for errors during TB Database synchronization.

    Attributes:
        msg  -- explanation of the error
    """
    
    def __init__(self, msg):
        self.msg = msg

