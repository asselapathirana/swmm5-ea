import sys
import swmm_ea_controller
from multiprocessing import  freeze_support


if __name__=="__main__":
    freeze_support()
    sc=swmm_ea_controller.swmmeacontroller()
    sc.show()