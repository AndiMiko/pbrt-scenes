import pyexr, math, os, glob, sys, xlsxwriter

def calcMSE(curimg, refimg):
    mse = 0;
    for curX, refX in zip(curimg, refimg):
        for (curPixel, refPixel) in zip(curX, refX):
            mse += pow(curPixel[0] - refPixel[0], 2);
            mse += pow(curPixel[1] - refPixel[1], 2);
            mse += pow(curPixel[2] - refPixel[2], 2);
    return math.sqrt(mse)


if (len(sys.argv) != 3):
    print ("Usage: <referenceFile.exr> <check File or Folder>")
    sys.exit(0)
refFilePath, curFilePath = sys.argv[1], sys.argv[2]
refereceFile = pyexr.open(refFilePath)
curFilePaths = []
workbook = xlsxwriter.Workbook('mse_report.xlsx')
worksheet = workbook.add_worksheet()
worksheet.write(0, 0, refFilePath)
worksheet.write(0, 1, curFilePath)

if (os.path.isdir(curFilePath)):
    for filename in glob.iglob(curFilePath + '*.exr'):
        curFilePaths.append(filename)
else:
    curFilePaths.append(curFilePath)


for index, curFilePath in enumerate(curFilePaths, start=2):
    worksheet.write(index, 0, curFilePath)
    curimg = pyexr.open(curFilePath).get()
    #mse = calcMSE(curimg, refereceFile.get())

workbook.close()
