import os, sys
import setuptools
from pathlib import Path

about = {}
here = Path(__file__).absolute().parent
with open(here /"src" / "cjops" / "__version__.py", "r", encoding="utf-8") as f:
    # exec() 函数用于执行从文件中读取的 Python 代码。具体来说，exec() 函数可以接受字符串形式的Python代码并执行,或者从文件中读取代码并执行。
    # 在你的例子中，通过打开文件 __version__.py 并读取其中的内容，然后使用 exec() 函数执行这些代码，将执行结果存储在 about 字典中。这种做法通常用于从外部文件中加载配置、定义变量或执行一些特定的操作。
    exec(f.read(), about)

with open("README.md", "r") as fh:
    long_description = fh.read()

# 'setup.py publish' shortcut.
if sys.argv[-1] == "publish":
    os.system("rm -rf build cjops.egg-info dist")
    os.system("python setup.py sdist bdist_wheel")
    os.system("twine upload --skip-existing --repository-url https://upload.pypi.org/legacy/  dist/*")
    os.system("pip uninstall cjops -y && pip install -U cjops -i https://pypi.org/simple")
    sys.exit()

requires = [
        'aliyun-log-python-sdk>=0.8.15',
        'requests>=2.31.0',
        'loguru>=0.6.0',
        'dnspython',
        'pandas',
        'pendulum',
        'pymysql',
        'openpyxl',
        'cryptography',
        'yagmail',
        'tqdm',
        'pyperclip',
        'emoji'
]

setuptools.setup(
    # 包的分发名称，使用字母、数字、_、-
    name=about['__title__'],
     # 版本号, 版本号规范：https://www.python.org/dev/peps/pep-0440/
    version=about['__version__'],
    # 作者名
    author=about['__author__'],
     # 作者邮箱
    author_email=about['__author_email__'],
    # 包的简介描述
    description=about['__description__'],
    # 包的详细介绍(一般通过加载README.md)
    long_description=long_description,
    # 和上条命令配合使用，声明加载的是markdown文件
    long_description_content_type="text/markdown",
    # 如果项目由多个文件组成，我们可以使用find_packages()自动发现所有包和子包，而不是手动列出每个包，在这种情况下，包列表将是example_pkg
    # packages=setuptools.find_packages(),
    packages=["cjops"],  # 指定包名，确保只包含你需要的包
    package_dir={"": "src"},  # 指定包的根目录为src
    # 关于包的其他元数据(metadata)
    zip_safe=False,# 设置为False,提高安装效率和性能
    classifiers=[
         # 该软件包仅与Python3兼容
        "Programming Language :: Python :: 3",
        # 根据MIT许可证开源
        "License :: OSI Approved :: MIT License",
        # 与操作系统无关
        "Operating System :: OS Independent",
    ],
    # 依赖模块
    install_requires= requires,
    python_requires='>=3',
)