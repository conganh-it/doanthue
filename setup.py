from setuptools import setup

setup(
    name='fxplc',  # Tên thư viện
    version='1.0.0',
    description='A library for interfacing with FXPLC devices',
    author='Your Name',
    author_email='your_email@example.com',
    packages=['fxplc_lib'],  # Tên package (thư mục)
    install_requires=['pyserial'],  # Các thư viện phụ thuộc
)
