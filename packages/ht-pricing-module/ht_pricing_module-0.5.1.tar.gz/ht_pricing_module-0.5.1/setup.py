from setuptools import setup, find_packages


VERSION = "0.5.1"


def filter_package():
    packages = []
    packages_all = find_packages()
    for i in packages_all:
        if i.split(".")[0] == 'ht_pricing_module':
            packages.append(i)
    return packages


setup(name="ht_pricing_module",
      version=VERSION,
      author="wangjun",
      readme="README.md",
      description="huatai option pricing module",
      author_email="wangjun@htgwfzb.com",
      url='http://10.17.75.129:9002/wangjun/ht_pricing_server/-/tree/main/ht_pricing_module',
      requires_python=">=3.6",

      packages=filter_package(),
      include_package_data=True,
      platforms="any",
      install_requires=['numpy', 'scipy', 'pandas', 'grpcio==1.38.0', 'grpcio-status==1.38.0',
                        'grpcio-tools==1.38.0', 'protobuf==3.17.3']
      )

# user, pypi2023
# py -m build
# py -m twine upload .\dist\* --repository-url=http://10.17.75.129:9001
# pip install ht-pricing-module --upgrade -i http://10.17.75.129:9001 --trusted-host 10.17.75.129
