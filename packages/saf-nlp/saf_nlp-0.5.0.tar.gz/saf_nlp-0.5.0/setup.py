from distutils.core import setup

setup(
    name='saf-nlp',
    version='0.5',
    packages=['saf', 'saf.test', 'saf.constants', 'saf.importers', 'saf.importers.tokenizers', 'saf.annotators',
              'saf.data_model', 'saf.formatters'],
    url='',
    license='',
    author='Danilo S. Carvalho',
    author_email='danilo.carvalho@manchester.ac.uk',
    description='Simple Annotation Framework',
    install_requires=[
        'nltk',
        'regex'
    ]
)
