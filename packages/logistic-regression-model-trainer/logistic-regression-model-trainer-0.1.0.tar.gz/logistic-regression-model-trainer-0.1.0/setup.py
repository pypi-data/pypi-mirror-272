from setuptools import setup, find_packages

setup(
       name="logistic-regression-model-trainer",
       version="0.1.0",
       author="Zh",
       author_email="1119009608@qq.com",
       description="A brief description of your package",
       long_description=open("README.md",encoding='utf-8').read(),
       long_description_content_type="text/markdown",
       packages=find_packages(),  # 找到所有子目录下的包
       install_requires=["numpy", "scikit-learn", "sklearn2pmml"],  # 添加你的依赖
   )