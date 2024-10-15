from abc import ABC, abstractmethod

class IParams(ABC):
    """
    Interface for parameter classes used in modules.
    Module developers should inherit from this class when creating parameter classes for their modules.
    """

    def __init__(self, *args, **kwargs):
        """
        Common initialization logic for all parameter classes.
        """
        super().__init__(*args, **kwargs)
        # Any common setup can be done here
        # For example, initializing instance variables
        # self.some_common_variable = None

    @abstractmethod
    async def __ainit__(self, params: dict, validator, *args, **kwargs) -> None:
        """
        Asynchronous initializer for parameter classes.

        Args:
            params (dict): A dictionary of parameters.
            validator: An object responsible for validating parameters.
        """
        pass

    @abstractmethod
    def __repr__(self) -> str:
        """
        Return a string representation of the parameter object.

        Returns:
            str: String representation of the object.
        """
        pass

    @abstractmethod
    def get_chain(self):
        """
        Return the network or chain associated with these parameters.

        Returns:
            The network or chain object.
        """
        pass