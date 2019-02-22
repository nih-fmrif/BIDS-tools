#!/usr/bin/env python

from   optparse  import  OptionParser
import time, sys, os
from   fs.opener import fsopendir, fsopen


defaultDelimiter = "."      # Default delimiter for BIDS/nii
# defaultDelimiter = "+"      # Default delimiter for AFNI

defaultExt = ".nii"         # Default file extension for BIDS/nii
# defaultExt = "+orig"        # Default file extension for AFNI

class bidsToolsFS:
   """

   This class is designed to traverse a BIDS formatted data tree, and label
   the necessary data sets in each subject's folder needed for a particular
   analysis.

   """

   
   # def __init__(self):
      # print "Doing not much at all"


   def buildBIDSDict(self, bidsDir):

      bidsFS = fsopendir(bidsDir)

      # internalBIDSPath = bidsFS._decode_path(bidsDir)

      allRuns = bidsFS.walkfiles(wildcard="*sub*")
      # Store all unique dataset names
      runsList = []

      # Alternative to using the 'fs' module.  Needs to be tested and validated!
      #
      # allRuns = []
      #
      # for dirName, subdirList, fileList in os.walk(bidsDir, topdown=False):
      #    for fname in fileList:
      #       if ('sub' in fname):
      #          allRuns.append (unicode(os.path.join (dirName, fname), 'utf-8'))


      for eachRun in allRuns:
         if defaultDelimiter == "+": # AFNI data set
            runRootName = eachRun.split(defaultDelimiter)[0]
            if runRootName not in runsList:
	       runsList.append(runRootName)

         if defaultDelimiter == ".": # NIFTI data set
	    if eachRun not in runsList:
               runsList.append(eachRun)

      bidsMasterTreeDict = {}

      # Iterate over all datasets and build bidsMasterTreeDict
      for eachRun in runsList:

         runNameElements = eachRun.split("/")

         # If this is a properly formed BIDS tree, the format should be:
         # 
         #    sub-*/ses-*/scanType/*run*
         # 
         # or:
         # 
         #    sub-*/scanType/*run*

         thisRunName = runNameElements[-1]
         thisRunNameScanType = runNameElements[-2]

         if "ses-" in runNameElements[-3]:
            thisRunNameSession = runNameElements[-3]
            thisRunNameSub = runNameElements[-4]
         else:
            thisRunNameSession = "ses-NULL" # to indicate an artificially generated session, since none was explicity present in the original directory structure
            thisRunNameSub = runNameElements[-3]

         if thisRunNameSub not in bidsMasterTreeDict.keys():
            sessionDict = {}
            bidsMasterTreeDict[thisRunNameSub] = sessionDict

         if thisRunNameSession not in bidsMasterTreeDict[thisRunNameSub].keys():
            scanTypeDict = {}
            bidsMasterTreeDict[thisRunNameSub][thisRunNameSession] = scanTypeDict

         if thisRunNameScanType not in bidsMasterTreeDict[thisRunNameSub][thisRunNameSession].keys():
            scanTypeRunList = []
            bidsMasterTreeDict[thisRunNameSub][thisRunNameSession][thisRunNameScanType] = scanTypeRunList

         if thisRunName not in bidsMasterTreeDict[thisRunNameSub][thisRunNameSession][thisRunNameScanType]:
            bidsMasterTreeDict[thisRunNameSub][thisRunNameSession][thisRunNameScanType].append(thisRunName)

      return (bidsMasterTreeDict)



def main():

   """Will print the string equivalent of a dictionary
      representing a BIDS-formatted directory tree
      structure.
   """

   usage = "%prog [options]"
   description = ("Routine to build a dictionary from a BIDS tree:")

   usage =       ("  %prog -d bidsDataTree" )
   epilog =      ("For questions, suggestions, information, please contact Vinai Roopchansingh, Jerry French")

   parser = OptionParser(usage=usage, description=description, epilog=epilog)

   parser.add_option ("-d", "--dataDir",  action="store",
                                          help="Directory with BIDS-formatted subject data folders")

   options, args = parser.parse_args()

   bidsDict = bidsToolsFS().buildBIDSDict(options.dataDir)



if __name__ == '__main__':
   sys.exit(main())

