from setuptools import setup

setup(name='yt-dlp-api',
      version='0.1',
      description='The yt_dlp API Server',
      url='https://github.com/peter279k/yt-dlp-api',
      author='peter279k',
      author_email='peter279k@gmail.com',
      packages=['modules', 'routers'],
      license='MIT',
      python_requires=">=3.9",
      zip_safe=False)
