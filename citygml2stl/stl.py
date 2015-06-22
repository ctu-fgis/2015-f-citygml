class StlFile(object):
    """
    Class representing an STL file

    Use within the with statement
    """

    facet = '''  facet normal 0 0 0
    outer loop
      vertex {} {} {}
      vertex {} {} {}
      vertex {} {} {}
    endloop
  endfacet
'''

    def __init__(self, filename):
        """
        Saves the filename
        """
        self.filename = filename

    def __enter__(self):
        """
        Opens an STL file for writing
        """
        self.file = open(self.filename, 'w')
        self.file.write('solid citygml2stl\n')
        return self

    def write_triangles(self, triangles):
        """
        Writes triangles to the openned file
        """
        for tri in triangles:
            self.file.write(StlFile.facet.format(*[coord for vertex in tri for coord in vertex]))

    def __exit__(self, type, value, traceback):
        """
        End the syntax and close the file
        """
        self.file.write('endsolid citygml2stl\n')
        self.file.close()
