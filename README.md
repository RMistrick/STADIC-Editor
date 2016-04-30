##STADIC Editor

The STADIC Editor tool (Stadic) is a cross-platform data-visualization software that is meant to edit or enter data into the JSON control file provided by STADIC. The Stadic Editor tool was written in Python with the help of third-party open-source plugins. 
The following are the primary dependencies for the Stadic Editor:

1.	[Python 2.7.11, 32-bit ](https://www.python.org/ftp/python/2.7.11/python-2.7.11.msi)

2.	[PyQT 4, Python 2.7, 32 bit ](http://sourceforge.net/projects/pyqt/files/PyQt4/PyQt-4.11.4/PyQt4-4.11.4-gpl-Py2.7-Qt4.8.7-x32.exe)   

Provided that the modules mentioned above are installed on the client system, the Stadic Editor can by compiled into executable files by using [PyInstaller ](https://codeload.github.com/pyinstaller/pyinstaller/legacy.zip/develop)or [Py2exe](https://sourceforge.net/projects/py2exe/files/py2exe/0.6.9/py2exe-0.6.9.win32-py2.7.exe/download). 

The syntax for compiling the Stadic Editor on a windows system using Py2exe on a win-32 system is:   

`python setup.py py2exe`. 

The details for creating the setup.py file can be found at: http://py2exe.org/index.cgi/Tutorial#Step2 . The setup.py file should refer to stadic.py, the main script for launching the program.
