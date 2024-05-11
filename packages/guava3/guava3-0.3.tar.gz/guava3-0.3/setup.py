from setuptools import setup, find_packages

setup(
    name="guava3",
    version="0.3",
    packages=find_packages(),
    install_requires=[
        'PyYAML==6.0.1',
        'anthropic==0.23.1',
        'openai==1.13.3',
        'tiktoken==0.5.2',
        'Markdown==3.6',
        'pyarmor==8.5.0',
        'ipywidgets',
        'scikit-learn',
        'matplotlib',
        'pandas'
    ],
    author='Guava3',
    author_email='adm@guava3.com',
    description='multi-agent conversations for data analysis',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/guava-3/unified_framework',
)
