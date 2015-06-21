class CityGMLError(Exception):
    """
    Base exception indicating something went wrong with CityGML parsing
    """


class CityGMLInputError(CityGMLError):
    """
    Exception indicating the input file is not existing, cannot be read or similar
    """


class PlaneError(Exception):
    """
    Base exception indicating something went wrong with Plane class
    """


class PlaneConstructionError(PlaneError):
    """
    Exception indicating Plane class could not be constructed
    """
