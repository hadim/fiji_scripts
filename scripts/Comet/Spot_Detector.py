# @ImagePlus imp
 
from fiji.plugin.trackmate.detection import DogDetector
from ij.gui import PointRoi
from ij.plugin.frame import RoiManager
from net.imglib2.img.display.imagej import ImageJFunctions
 
# Set the parameters for DogDetector
img = ImageJFunctions.wrap(imp)
interval = img
cal = imp.getCalibration()
calibration = [cal.pixelWidth, cal.pixelHeight, cal.pixelDepth]
radius = 0.2 # the radius is half the diameter
threshold = 100
doSubpixel = True
doMedian = False
 
# Setup spot detector
# (see http://javadoc.imagej.net/Fiji/fiji/plugin/trackmate/detection/DogDetector.html)
# 
# public DogDetector(RandomAccessible<T> img,
#            Interval interval,
#            double[] calibration,
#            double radius,
#            double threshold,
#            boolean doSubPixelLocalization,
#            boolean doMedianFilter)
detector = DogDetector(img, interval, calibration, radius, threshold, doSubpixel, doMedian)
 
# Start processing and display the results
if detector.process():
    # Get the list of peaks found
    peaks = detector.getResult()
    print str(len(peaks)), "peaks were found."
 
    # Add points to ROI manager
    rm = RoiManager.getInstance()
    if not rm:
        rm = RoiManager()
 
    # Loop through all the peak that were found
    for peak in peaks:
        # Print the current coordinates
        print peak.getDoublePosition(0), peak.getDoublePosition(1), peak.getDoublePosition(2)
        # Add the current peak to the Roi manager
        proi = PointRoi(peak.getDoublePosition(0) / cal.pixelWidth, peak.getDoublePosition(1) / cal.pixelHeight)
        proi.setPosition(int(peak.getDoublePosition(2) / cal.pixelDepth))
        rm.addRoi(proi)
 
    # Show all ROIs on the image
    rm.runCommand(imp, "Show All")
 
else:
    print "The detector could not process the data."