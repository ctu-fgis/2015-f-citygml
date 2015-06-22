CityGML to STL
==============

Python library to convert `CityGML <http://www.citygml.org/>`_ data to
STL 3D models printable on FDM 3D printers, such as various
`RepRap <http://reprap.org/>`_ printers.

CityGML versions 2.0.0, 1.0.0 and 0.4.0 are supported. Other versions might work as well.

This is a coursework for `Free software GIS
<http://geo.fsv.cvut.cz/gwiki/155YFSG_Free_software_GIS>`_ class on
`Faculty of Civil Engineering <http://www.fsv.cvut.cz/index.php.en>`_,
`Czech Technical University in Prague <http://www.cvut.cz/>`_ (academic
year 2014/2015, group F). Licensed as MIT (see LICENSE).

.. figure:: https://raw.githubusercontent.com/ctu-yfsg/2015-f-citygml/master/berlin.png
   :alt: Image of generated STL

   CityGML of Alexanderplatz, Berlin, Germany.

   Data © `Research Center Karlsruhe, Institute for Applied Computer Science <http://www.iai.fzk.de/www-extern/index.php?id=222&L=1>`_

Usage
-----

.. highlight:: python

To use cityglm2stl from Python proceed as follows::

    # import stuff
    from citygml2stl import citygml
    from citygml2stl import polygons
    from citygml2stl import stl
    
    # parse the CityGML file
    c = citygml.CityGML('Berlin_Alexanderplatz_v0.4.0.xml')
    
    # export to file berlin.stl
    with stl.StlFile('berlin.stl') as berlin:
        # Specify as many types as you want,
        # or leave without arguments to get all city objects
        for obj in c.get_objects_of_types('Building'):
            berlin.write_triangles(polygons.object2triangles(obj))

Or, if you would prefer to have multiple STL files instead::

    # initialize a counter for filenames
    counter = 0
    
    for obj in c.get_objects_of_types('Building'):
        with stl.StlFile('berlin{}.stl'.format(counter)) as berlin:
            berlin.write_triangles(polygons.object2triangles(obj))
        counter += 1

Note that given the quality of most CityGML data found, the STLs will probably not be valid as the
facets will intersect each other. Also given the way the algorithm works, the order of the vertices
of a facet is random and will not always follow the right hand rule.

That said, consider that output needs repairing. Use public cloud services such as
`netfabb Cloud <http://cloud.netfabb.com/>`_ or even open source tools such as
`ADMesh <http://admesh.org/>`_ to repair the output.

You can even use Python's `admesh <https://pypi.python.org/pypi/admesh>`_ module to repair the STLs::

    import admesh
    ...
    
    filename = 'berlin{}.stl'.format(counter)
    with stl.StlFile(filename) as berlin:
        berlin.write_triangles(polygons.object2triangles(obj))
    
    s = admesh.Stl(filename)
    s.repair()
    
    # the results are often located on unthinkable coordinates
    s.translate(0, 0, 0)
    s.write_binary(filename)

Note that due to limitations of the admesh module it is currently not possible to redirect output
of citygml2stl to admesh without writing it to a file first.

Authors
-------

-  `Miro Hrončok <https://github.com/hroncok>`_
-  Inspired a bit by `CityGML2OBJs <https://github.com/tudelft3d/CityGML2OBJs>`_ by `Filip Biljecki <https://github.com/fbiljecki>`_ 
