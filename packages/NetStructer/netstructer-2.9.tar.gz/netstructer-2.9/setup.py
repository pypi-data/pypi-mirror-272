import setuptools

setuptools.setup(
	name = 'NetStructer',
	version = '2.9',
	author='Haytam-Zakaria',
	description="",
	packages=['NetStructer'],
	long_description='',
	long_description_content_type='text/markdown',
    install_requires=[
        'cryptography',
        'psutil',
        'requests'],
	classifiers=[
	'Programming Language :: Python :: 3',
	'Operating System :: OS Independent',
	'License :: OSI Approved :: MIT License']
)


'''
python setup.py sdist bdist_wheel
twine upload dist/*

'''
__token__ = '__token__'
token = 'pypi-AgEIcHlwaS5vcmcCJDUwM2ZlOGE0LWY0OGEtNGI3OC1hZjYzLTg0ZWIzYTViMWM2ZAACKlszLCIxMTc1ZTVmYi0yNTlkLTRmMDAtOTA0Ni03NWQzMWZjODNiYzEiXQAABiDkBd_eGJcEpcheZJQmtH7njwWTdgIQmoaF2zFASvhLkg'