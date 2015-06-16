class CityGMLError(Exception):
    """
    Base exception indicating something went wrong with CityGML parsing
    """


class CityGMLInputError(CityGMLError):
    """
    Exception indicating the input file is not existing, cannot be read or similar
    """
