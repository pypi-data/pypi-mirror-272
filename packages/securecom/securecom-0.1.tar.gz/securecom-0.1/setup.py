from setuptools import setup, find_packages

setup(
    name='securecom',  # Nom de votre package
    version='0.1',  # Version initiale
    packages=find_packages(),  # Détecte automatiquement tous les paquets Python dans le dossier
    install_requires=[
        'cryptography',  # Dépendance nécessaire pour certificate_manager
    ],
    author='Votre Nom',
    author_email='votre.email@example.com',
    description='Un package pour une communication sécurisée'
)
