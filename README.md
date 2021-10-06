# bank-statement-utility
This is a new repo for automating bank statement processing. 
One of the previous repos which was started with a friend of mine
is available [here on GitHub.](https://github.com/mattandersoninf/convert-bank-statement-to-expense-report)

Credits to Matt for starting the work with Google Drive, but to breathe new life 
into this effort (and help quickly get my finances together) I want to start 
fresh with as little tasks needed as possible. From there, I will expand to
include the work we were doing, and more.

# Known Issues
During installation, it is known that installing pdftotext can cause some issues. There are known solutions at the following links:
[Stackoverflow](https://stackoverflow.com/a/58139729)
[Coder.Haus's Personal Blog](https://coder.haus/2019/09/27/installing-pdftotext-through-pip-on-windows-10/)
[Conda Install](https://anaconda.org/conda-

Just in case the above instructions get taken down, the steps are:

1) Install Anaconda Python. 

2) pip install pdftotext gives error saying Microsoft Visual C++ is required

3) In browser: http://visualstudio.microsoft.com/downloads. 
Tools for Visual Studio 2019 tab > download the Build Tools for Visual Studio 2019. 
   Install the tools by checking the C++ build tools option box and clicking Install.

4) pip install gives new error “Cannot open include file: ‘poppler/cpp/poppler-document.h’. 
   This is because you’re missing the poppler libraries.

5) Need poppler for windows from http://blog.alivate.com.au/poppler-windows. 
   Uncompress the latest library. pip is looking for 
   {Anaconda3 directory}\include\poppler\cpp\poppler-document.h. 
   In the uncompressed folder "include" folder, copy the whole poppler directory (which should
   have the poppler-document.h file in its lowest subdirectory). 
   

6) Paste into the Anaconda3\include folder.

7) pip install gives new error for a missing linked library, poppler-cpp.lib. 
   run conda install -c conda-forge poppler

8) This installs poppler-cpp.lib file into {Anaconda3 directory}\Library\lib\poppler-cpp.lib 
   Now copy and paste it to {Anaconda3 directory}\libs.

9) pip install pdftotext should work
