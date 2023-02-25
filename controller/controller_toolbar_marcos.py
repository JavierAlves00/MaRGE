"""
session_controller.py
@author:    José Miguel Algarín
@email:     josalggui@i3m.upv.es
@affiliation:MRILab, i3M, CSIC, Valencia, Spain
"""
from widgets.widget_toolbar_marcos import MarcosToolBar
import os
import subprocess
import platform
import experiment as ex
import numpy as np
import shutil


class MarcosController(MarcosToolBar):
    def __init__(self, *args, **kwargs):
        super(MarcosController, self).__init__(*args, **kwargs)

        # Copy relevant files from marcos_extras
        shutil.copy("../marcos_extras/copy_bitstream.sh", "../PhysioMRI_GUI")
        shutil.copy("../marcos_extras/marcos_fpga_rp-122.bit", "../PhysioMRI_GUI")
        shutil.copy("../marcos_extras/marcos_fpga_rp-122.bit.bin", "../PhysioMRI_GUI")
        shutil.copy("../marcos_extras/marcos_fpga_rp-122.dtbo", "../PhysioMRI_GUI")
        shutil.copy("../marcos_extras/readme.org", "../PhysioMRI_GUI")

        self.action_server.setCheckable(True)
        self.action_start.triggered.connect(self.startMaRCoS)
        self.action_server.triggered.connect(self.controlMarcosServer)
        self.action_copybitstream.triggered.connect(self.copyBitStream)
        self.action_gpa_init.triggered.connect(self.initgpa)

    def startMaRCoS(self):
        """
        @author: J.M. Algarín, MRILab, i3M, CSIC, Valencia
        @email: josalggui@i3m.upv.es
        @Summary: execute startRP.sh: copy_bitstream.sh & marcos_server
        """

        # Set the path to the Git Bash executable
        bash_path = r"D:\Archivos de Programa\Git\git-bash.exe"

        # Set the path to the shell script
        script_path = "..\PhysioMRI_GUI\startRP.sh"

        if not self.demo:
            os.system('ssh root@192.168.1.101 "killall marcos_server"')
            if platform.system() == 'Windows':
                result = subprocess.run([bash_path, script_path])
                self.action_server.toggle()
                self.initgpa()
                # os.system('start ./startRP.sh')
            elif platform.system() == 'Linux':
                os.system('./startRP.sh &')
                self.action_server.toggle()
                self.initgpa()
            print("\nMaRCoS updated, server connected, gpa initialized.")

        else:
            print("\nThis is a demo.")

    def controlMarcosServer(self):
        """
        @author: J.M. Algarín, MRILab, i3M, CSIC, Valencia
        @email: josalggui@i3m.upv.es
        @Summary: connect to marcos_server
        """

        if not self.action_server.isChecked():
            self.action_server.setStatusTip('Connect to marcos server')
            self.action_server.setToolTip('Connect to marcos server')
            if not self.demo:
                os.system('ssh root@192.168.1.101 "killall marcos_server"')
            print("\nServer disconnected.")
        else:
            self.action_server.setStatusTip('Kill marcos server')
            self.action_server.setToolTip('Kill marcos server')
            if platform.system() == 'Windows' and not self.demo:
                os.system('ssh root@192.168.1.101 "killall marcos_server"')
                os.system('start ssh root@192.168.1.101 "~/marcos_server"')
            elif platform.system() == 'Linux' and not self.demo:
                os.system('ssh root@192.168.1.101 "killall marcos_server"')
                os.system('ssh root@192.168.1.101 "~/marcos_server" &')
            print("\nServer connected.")

    def copyBitStream(self):
        """
        @author: J.M. Algarín, MRILab, i3M, CSIC, Valencia
        @email: josalggui@i3m.upv.es
        @Summary: execute copy_bitstream.sh
        """
        if not self.demo:
            os.system('ssh root@192.168.1.101 "killall marcos_server"')
            if platform.system() == 'Windows':
                os.system("start ./copy_bitstream.sh 192.168.1.101 rp-122")
            elif platform.system() == 'Linux':
                os.system('./copy_bitstream.sh 192.168.1.101 rp-122')
            print("\nMaRCoS updated")
        else:
            print("\nThis is a demo.")

    def initgpa(self):
        """
        @author: J.M. Algarín, MRILab, i3M, CSIC, Valencia
        @email: josalggui@i3m.upv.es
        @Summary: initialize the gpa board
        """
        if self.action_server.isChecked():
            if not self.demo:
                expt = ex.Experiment(init_gpa=True)
                expt.add_flodict({
                    'grad_vx': (np.array([100]), np.array([0])),
                })
                expt.run()
                expt.__del__()
            print("\nGPA init done!")
        else:
            print("\nNo connection to the server")
            print("Please, connect to MaRCoS server first")