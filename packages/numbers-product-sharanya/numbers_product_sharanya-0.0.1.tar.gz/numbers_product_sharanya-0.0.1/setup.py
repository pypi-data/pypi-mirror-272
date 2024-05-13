from setuptools import setup, find_packages


setup(
    name="numbers_product-sharanya",
    version = "0.0.1",
    packages= find_packages(),
    author= "Sharanya Ganesh Prasad",
    description= "product of digits in a number",
    long_description= open("README.md").read(),
    long_description_content_type="text/markdown"
)