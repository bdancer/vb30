#
# V-Ray For Blender
#
# http://chaosgroup.com
#
# Author: Andrei Izrantcev
# E-Mail: andrei.izrantcev@chaosgroup.com
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# All Rights Reserved. V-Ray(R) is a registered trademark of Chaos Software.
#

import os
import re
import struct
import subprocess
import signal
import sys
import tempfile

from vb30.debug import Debug
from . import PathUtils


class VRayProcess:
    def __init__(self):
        self.filepath = ""
        self.waitExit = False
        self.autorun  = True

        # Process
        self.process  = None

        # Performance
        self.numThreads = 0

        # Input data
        self.sceneFile = ""
        self.include = ""

        # Animation
        self.frames = ""

        # Distributed Rendering
        self.distributed = 0
        self.renderhost = ""
        self.portNumber = 20207
        self.limitHosts = 0

        self.transferAssets = 0
        self.cachedAssetsLimitType = 0
        self.cachedAssetsLimitValue = 0.0
        self.overwriteLocalCacheSettings = 0

        # VFB Display Options
        self.useRegion = False
        self.useCrop   = False

        self.autoClose = 0
        self.setfocus = 1
        self.display = 1
        self.displayAspect = 0
        self.displayLUT = 0
        self.displaySRGB = 2
        self.region = ""

        # Output file
        self.imgFile = ""
        self.noFrameNumbers = 0

        # Realtime engine
        self.rtEngine = 0
        self.rtNoise = 0.001
        self.rtSampleLevel = 0
        self.rtTimeOut = 0.0

        # Progress output
        self.verboseLevel = '3'
        self.showProgress = '1'
        self.progressIncrement = 10
        self.progressUpdateFreq = 200
        self.progressUseColor = 1
        self.progressUseCR = 1

        # Unused params
        #
        # self.interactive = 0

        # These params will be setup via 'SettingsOutput'
        #
        # imgHeight
        # imgWidth
        # region
        # crop

    def setVRayStandalone(self, filepath):
        self.filepath = filepath

    def setAutorun(self, autorun):
        self.autorun = autorun

    def setSceneFile(self, sceneFile):
        self.sceneFile = sceneFile

    def setWaitExit(self, waitExit):
        self.waitExit = waitExit

    def setDisplaySRGB(self, useSRBG):
        self.displaySRGB = 1 if useSRBG else 2

    def setDisplayVFB(self, displayVFB):
        self.display = displayVFB

    def setAutoclose(self, autoclose):
        self.autoclose = autoclose

    def setOutputFile(self, imgFile):
        self.imgFile = imgFile

    def setVerboseLevel(self, verboseLevel):
        self.verboseLevel = verboseLevel

    def setShowProgress(self, progress):
        self.showProgress = progress

    def setThreads(self, threads):
        self.numThreads = threads

    def setRegion(self, x0, y0, x1, y1, useCrop=False):
        self.useRegion = True
        self.useCrop   = useCrop
        self.region = "%i;%i;%i;%i" % (x0, y0, x1, y1)

    def setFrames(self, frameStart, frameEnd, frameStep=1):
        self.frames = "%d-%d,%d" % (frameStart, frameEnd, frameStep)

    def getCommandLine(self):
        cmd = [self.filepath]
        cmd.append('-verboseLevel=%s' % self.verboseLevel)
        cmd.append('-showProgress=%s' % self.showProgress)
        cmd.append('-display=%s' % self.display)
        cmd.append('-displaySRGB=%s' % self.displaySRGB)

        if self.numThreads:
            cmd.append('-numThreads=%s' % self.numThreads)

        if self.useRegion:
            regionType = "crop" if self.useCrop else "region"
            cmd.append('-%s=%s' % (regionType, self.region))

        if self.imgFile:
            cmd.append('-imgFile=%s' % PathUtils.Quotes(self.imgFile))

        if self.frames:
            cmd.append('-frames=%s' % self.frames)

        cmd.append('-sceneFile=%s' % PathUtils.Quotes(self.sceneFile))

        return cmd


    def run(self):
        cmd     = self.getCommandLine()
        errCode = 0

        if self.autorun:
            self.process = subprocess.Popen(cmd)
            if self.waitExit:
                errCode = self.process.wait()
        else:
            print("V-Ray Command Line: %s" % " ".join(cmd))

        return errCode


    def kill(self):
        if self.is_running():
            self.process.terminate()
        self.process = None


    def is_running(self):
        if self.process is None:
            return False
        if self.process.poll() is None:
            return True
        return False
