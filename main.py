import Section as sec
import numpy as np


def main():

    con = sec.concrete(30,1.5)
    steel = sec.steel(420,1.15)
    b = sec.ordinaryRectangularSection(500,300,50,1,1,0,0,14,14)
    b.assignSectionMaterial(con)
    b.assignRebarMaterial(steel)
    b.assignDiscretisation(10)
    Nmm = b.computeNMM(np.array([0.000746943,0.000005,0]))
    print(Nmm)

    d, lamb = b.computeM_muDiagram(0.000001,100)

    print("d:")
    print(d)
    print("lamb:")
    print(lamb)




main()