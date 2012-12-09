# -*- coding: utf-8 -*-
#
# Copyright © 2011 Pierre Raybaut
# Licensed under the terms of the MIT License
# (see spyderlib/__init__.py for details)

"""Create a stand-alone executable"""
import os
os.chdir("src")
try:
    from guidata.disthelpers import Distribution
except ImportError:
    raise ImportError, "This script requires guidata 1.4+"

import os.path as osp
#import spyderlib


def create_executable():
    """Build executable using ``guidata.disthelpers``"""
    dist = Distribution()
    dist.setup(name="SWMM5 EC", version="0.5", #spyderlib.__version__,
               description=u"Running Evolutionary Algorithm with SWMM 5.0",
               script="swmm5ec.pyw",
               target_name="swmm5ec.exe")#, icon="spyder.ico")
 #   spyderlib.add_to_distribution(dist)

    import guiqwt
    import guidata
    import h5py
    import email
    dist.add_modules('guiqwt', 'h5py', 'guidata')

    #dist.includes+=["email"]
    
    ##try:
    #import guiqwt  # analysis:ignore
    #dist.add_modules('guiqwt')
    #except ImportError:
        #pass
    #dist.includes += ['spyderlib.widgets.externalshell.startup',
                      #'spyderlib.widgets.externalshell.sitecustomize',
                      #'IPython']
    #dist.excludes += ['sphinx']  #XXX: ...until we are able to distribute it
    #if osp.isfile("Spyderdoc.chm"):
        #dist.add_data_file("Spyderdoc.chm")
    #dist.add_data_file(osp.join("rope", "base", "default_config.py"))
    # Building executable
    dist.build('cx_Freeze')


if __name__ == '__main__':
    create_executable()