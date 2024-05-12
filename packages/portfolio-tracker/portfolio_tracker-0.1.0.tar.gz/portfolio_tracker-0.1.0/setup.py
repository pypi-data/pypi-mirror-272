from setuptools import setup, find_packages

setup(
    name='portfolio_tracker',
    python_requires='>=3.10',
    packages=find_packages(include=['portfolio_tracker']),
    version='0.1.0',
    description='A portfolio tracker library, that allows to track a portfolio of stocks and their performance.',
    author='Poli Luca',
    install_requires=['pandas', 'yfinance', 'numpy', 'pandas_market_calendars'],
    package_data={'docs': ['manager.html', 'price_repo.html', 'utils.html', 'xlsx_example.xlsx', 'example.ipynb']},
)
