import Section as sec
import numpy as np
import matplotlib.pyplot as plt


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
    b = sec.ordinaryRectangularSection(400,250,40,1,1,0,0,14,14)
    b.assignSectionMaterial(con)
    b.assignRebarMaterial(steel)
    b.assignDiscretisation(100)
    

    d, lamb = b.computeM_muDiagram(0.000001,160,0)

    print("d:")
    print(d)
    print("lamb:")
    print(lamb)

    print("Nmm:")

    
    print("curvature at max 68kNm")
    print(d[6])

    Nmm = b.computeNMM(d[-1])
    print("Nmm at curvature of 0.0002/mm")
    print(Nmm)

    plt.plot(d[:,1]*1000, lamb*0.000001)
    plt.title("M3 moment - curvature graph; Normal force = 0")
    plt.xlabel("Curvature (1/m)")
    plt.ylabel("M3 moment (kNm)")
    plt.grid()
    plt.show()





main()