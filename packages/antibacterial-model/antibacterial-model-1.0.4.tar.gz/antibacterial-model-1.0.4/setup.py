from setuptools import setup, find_packages

setup(
    name='antibacterial-model',
    version='1.0.4',
    description='A model for predicting antibacterial activity from SMILES strings',
    author='Chonthicha Arbsuwan',
    author_email='chon7599@gmail.com',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'rdkit',
        'scikit-learn',
        'joblib',
        'pandas',
    ],
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    package_data={'antibacterial_model': ['data/anti-bact-data.csv', 'anti-bact-model.pkl']},
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
