import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Quantitative-BackTest-Framework",  # 发布到PyPI的包名称
    version="0.0.1",  # 包的版本号
    author="TonnyTang",
    author_email="e1127294@u.nus.edu",
    description="A project for backtest quantitative trading strategy",  # 对包的简短描述
    long_description=long_description,  # 从README.md读取的详细描述
    long_description_content_type="text/markdown",
    url="https://github.com/TonnyTang09/Quantitative-BackTest-Framework",  # 包的主页
    packages=setuptools.find_packages(),  # 自动查找包内所有的python包
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],  # 元数据分类器
    python_requires='>=3.6',  # 指定Python版本
    install_requires=[  # 依赖包列表
        'numpy == 1.23.5',
        'openpyxl == 3.0.10',
        'pandas == 2.2.2',
        'plotly == 5.9.0',
        'setuptools == 67.8.0'
    ]
)
