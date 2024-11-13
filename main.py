import Section as sec
import numpy as np


def main():

    con = sec.concrete(30,1.5)

    # strain = np.arange(-0.006,0.001,0.0001)

    # stress = np.zeros((len(strain)),dtype=float)
    # stiffness = np.zeros((len(strain)),dtype=float)
    # for n,i in enumerate(strain):
    #     stress[n] = con.stress(i)
    #     stiffness[n] = con.tangentModulus(i)

    # print("strain:")
    # print(strain)
    # print("stress:")
    # print(stress)
    # print("tangent modulus:")
    # print(stiffness)

    
    steel = sec.steel(420,1.15)
    b = sec.ordinaryRectangularSection(500,300,50,1,1,0,0,14,14)
    b.assignSectionMaterial(con)
    b.assignRebarMaterial(steel)
    b.assignDiscretisation(100)
    

    d, lamb = b.computeM_muDiagram(0.000001,200)

    print("d:")
    print(d)
    print("lamb:")
    print(lamb)

    print("Nmm:")

    Nmm = b.computeNMM(np.array([0.0069,0.00005,0]))
    print(d[115])





main()