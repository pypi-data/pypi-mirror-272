from setuptools import setup, find_packages

setup(

   name='Lib_charPk',
   version='1.0.1',
   author= 'Missael Angel Cardenas ',
   author_email='milton_ac@tesch.edu.mx',
   description='Es una libreria la cual permitira generar un pokemon  aleatorio',
   packages= ['Lib_charPk'],
   package_data={'Lib_charPk': ['pokemon.csv']},
   install_requires=['pandas',
                     'twine',
                     'wheel' ,
                     'setuptools'
                     ],
)
