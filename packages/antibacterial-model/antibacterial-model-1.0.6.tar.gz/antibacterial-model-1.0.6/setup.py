from setuptools import setup, find_packages

setup(
    name='antibacterial-model',
    version='1.0.6',
    description='A model for predicting antibacterial activity from SMILES strings',
    author='Chonthicha Arbsuwan',
    author_email='chon7599@gmail.com',
    packages=find_packages(),
    install_requires=[
        'numpy==1.24.1',
        'rdkit==2023.3.3',
        'scikit-learn==1.2.1',
        'joblib==1.2.0',
        'pandas==1.5.3',
    ],
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    package_data={'antibacterial_model': ['data/anti-bact-data.csv', 'data/anti-bact-model.pkl']},
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
