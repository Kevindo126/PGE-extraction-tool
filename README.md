# PGE-extraction-tool
This tool uses Tesseract OCR to extract specific text from PGE bill statements and constructs a csv file with specific fields.

# Original Process
The finance department recieves PGE bills and the manually enters the specific details into Unity. Once the information is verified and correct, it is entered into FMS and the batch is given back to finance department, where they cut the check.

# Improved Process
The tool will boost productivity and take out the labor of manually entering data into unity, as well as reducing human errors. Once PGE bill is recieved, it will be scanned into a PDF format. Once that is done, the tool will take the PDF and convert it into a tiff file. Then the program uses Tesseract to extract text and creates a text file. After that, the program will create a csv file with the specific fields and all the data from PGE in it.

# Requirements
1. Linux OS preferably Ubuntu 18.04 LTS
2. Python 3
3. pip ($sudo apt-get install python3-pip)
3. Pip 3 for tqdm (progress bar)($pip3 install tqdm)
4. PyPDF2 for reading pdfs ($sudo apt-get install python3-pypdf2)
5. pdftk for splitting pdfs 
   ($sudo add-apt-repository ppa:malteworld/ppa;
    $sudo apt update;
    $sudo apt install pdftk)
6. modify ImageMagick policy to read/write pdf ($cd /etc/ImageMagick-6; $sudo nano policy.xml)
   a. Go to <policymap>
   b. Find the line <policy domain="coder" rights="none" pattern="PDF" />
   c. change: rights="none" to rights="read|write"
   d. Press ctrl + x and then enter to save
7. Tesseract for optical character recognition ($sudo apt-get install tesseract-ocr)
   

# Todo or comments
1. Establish a folder location for program to automatically fetch all the PDFs. 
2. Automate converting process to reduce the need of user input.
