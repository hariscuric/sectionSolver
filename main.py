import Section as sec
import numpy as np
import matplotlib.pyplot as plt


def main():

    con = sec.concrete(30,1.5)

    
    steel = sec.steel(420,1.15)
    b = sec.ordinaryRectangularSection(800,400,40,3,3,6,6,16,16)
    b.assignSectionMaterial(con)
    b.assignRebarMaterial(steel)
    b.assignDiscretisation(100)
    

    d, lamb = b.computeM_muDiagram(0.000001,34,-2000000)


    plt.plot(d[:,1]*1000, lamb*0.000001)
    plt.title("M3 moment - curvature graph; Normal force = -2000kN")
    plt.xlabel("Curvature (1/m)")
    plt.ylabel("M3 moment (kNm)")
    plt.grid()
    plt.show()





main()