import pyexr, math, os, glob, sys, xlsxwriter, re
from sys import stdout

def calcMSE(curimg, refimg):
    mse = 0;
    for curX, refX in zip(curimg, refimg):
        for (curPixel, refPixel) in zip(curX, refX):
            if (curPixel[0] == float('Inf') or curPixel[1] == float('Inf') or curPixel[2] == float('Inf') ):
                print ("Pixel with inf value, skipping this pixel ...");
            else:
                mse += pow(curPixel[0] - refPixel[0], 2);
                mse += pow(curPixel[1] - refPixel[1], 2);
                mse += pow(curPixel[2] - refPixel[2], 2);

    return math.sqrt(mse)


if (len(sys.argv) != 3):
    print ("Usage: <referenceFile.exr> <check File or Folder>")
    sys.exit(0)
refFilePath, tarFilePath = sys.argv[1], sys.argv[2]
refereceFile = pyexr.open(refFilePath)
if (os.path.isdir(tarFilePath)):
    tarFilePaths = [x[0] for x in os.walk(tarFilePath)]

for curFilePath in tarFilePaths:
    if not curFilePath.endswith('.exr'):
        curFilePath += '\\'
    curFilePaths = []

    if (os.path.isdir(curFilePath)):
        for filename in glob.iglob(curFilePath + '*.exr'):
            curFilePaths.append(filename)
    else:
        curFilePaths.append(curFilePath)

    if curFilePaths:
        workbook = xlsxwriter.Workbook(str(os.path.dirname(curFilePath) + '\\' + os.path.dirname(curFilePath) + '_mse_report.xlsx'))
        print(str('Writing report to: ' + os.path.dirname(curFilePath) + '\\' + os.path.dirname(curFilePath) + '_mse_report.xlsx'))
        worksheet = workbook.add_worksheet()
        worksheet.write(0, 0, refFilePath)
        worksheet.write(0, 1, curFilePath)

        startDataLine = 3
        worksheet.write(startDataLine, 0, "Filename")
        worksheet.write(startDataLine, 1, "MSE")
        worksheet.write(startDataLine, 2, "Seconds")
        worksheet.write(startDataLine, 2, "RMSE")
        worksheet.write(startDataLine, 4, "Seconds*MSE")

        for index, curFilePath in enumerate(curFilePaths, start=startDataLine+1):
            print("\rCalculating file %d/%d... [%s]" % (index - startDataLine, len(curFilePaths), curFilePath)),
            stdout.flush()
            worksheet.write(index, 0, curFilePath)
            mse = calcMSE(pyexr.open(curFilePath).get(), refereceFile.get())
            worksheet.write(index, 1, mse)
            worksheet.write(index, 3, math.sqrt(mse))
            time = re.search(r'_t(\d+)_', curFilePath, re.IGNORECASE)
            if time:
                seconds = int(time.group(1))
                worksheet.write(index, 2, seconds)
                worksheet.write(index, 4, seconds*mse)


        workbook.close()
