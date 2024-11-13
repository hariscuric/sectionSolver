import numpy as np
import math as m



def inputSection():


    return 0


class material:
    def __init__(self):
        pass

    def stress(self, strain):
        return 0.0
    
    def tangentModulus(self, strain):
        return 0.0
    

class concrete(material):
    def __init__(self,fck,gamaM):
        super().__init__()
        if fck <= 50.0:
            self.ec2 = 0.002
            self.ecu2 = 0.0035
            self.n = 2.0
        else:
            self.ec2 = (2.0+0.085*(fck-50)**0.53)/1000
            self.ecu2 = (2.6+35*((90-fck)/100)**4)/1000
            self.n = 1.4+23.4*((90-fck)/100)**4
        self.fck = fck
        self.fcd = fck/gamaM

    def stress(self, strain):
        strain = -strain
        if strain<0.0:
            return 0.0
        elif strain<=self.ec2:
            return -self.fcd * (1-(1-strain/self.ec2)**self.n)
        elif strain<=self.ecu2:
            return -self.fcd
        # elif strain>self.ecu2 and strain<=self.ecu2*1.5:
        #     return -0.05*self.fcd-0.95*self.fcd*((self.ecu2*1.5-strain)/(0.5*self.ecu2))
        # elif strain>self.ecu2*1.5:
        #     return -0.05*self.fcd
        else:
            return -self.fcd
        
    def tangentModulus(self, strain):
        strain = -strain
        if strain<0.0:
            return 0.0
        elif strain<=self.ec2:
            return (self.n*self.fcd/self.ec2)*((1-strain/self.ec2)**(self.n-1))
        # elif strain>self.ecu2 and strain<=self.ecu2*1.5:
        #     return -0.95*self.fcd/(0.5*self.ecu2)
        else:
            return 0.0




class steel(material):
    def __init__(self,fyk,gamaM,Class="B"):
        super().__init__()
        self.fyk = fyk
        self.fyd = fyk/gamaM
        if Class == "A":
            self.k = 1.05
            self.euk = 0.025
        elif Class == "B":
            self.k = 1.08
            self.euk = 0.05
        elif Class == "C":
            self.k = 1.15
            self.euk = 0.075
        else:
            self.k = 1.08
            self.euk = 0.05

        self.eud = self.euk*0.9

    def stress(self, strain):
        Es = 200000
        ey = self.fyd/Es
        if strain<=ey and strain>=-ey:
            return Es*strain
        elif strain>ey and strain<=self.eud:
            return self.fyd + (strain-ey)*(self.fyd*(self.k-1)/(self.euk-ey))
        elif strain<-ey and strain>=-self.eud:
            return -self.fyd + (strain+ey)*(self.fyd*(self.k-1)/(self.euk-ey))
        elif strain>self.eud and strain<=self.euk:
            return (self.fyd + (self.eud-ey)*(self.fyd*(self.k-1)/(self.euk-ey)))*(self.euk-strain)/(self.euk-self.eud)
        elif strain<-self.eud and strain>=-self.euk:
            return (-self.fyd + (-self.eud+ey)*(self.fyd*(self.k-1)/(self.euk-ey)))*(-self.euk-strain)/(-self.euk+self.eud)
        else:
            return 0.0
        
    def tangentModulus(self, strain):
        Es = 200000
        ey = self.fyd/Es
        if strain<=ey and strain>=-ey:
            return Es
        elif strain>ey and strain<=self.eud:
            return (self.fyd*(self.k-1)/(self.euk-ey))
        elif strain<-ey and strain>=-self.eud:
            return (self.fyd*(self.k-1)/(self.euk-ey))
        elif strain>self.eud and strain<=self.euk:
            return -(self.fyd + (self.eud-ey)*(self.fyd*(self.k-1)/(self.euk-ey)))/(self.euk-self.eud)
        elif strain<-self.eud and strain>=-self.euk:
            return -(self.fyd + (self.eud-ey)*(self.fyd*(self.k-1)/(self.euk-ey)))/(self.euk-self.eud)
        else:
            return 0.0
        





class section:
    def __init__(self, sectionCorners, rebarPositions, rebarDiameters):
        self.concreteCorners = sectionCorners
        self.rebarPositions = rebarPositions
        self.rebarDiameters = rebarDiameters
        self.sectionMaterial = material()
        self.rebarMaterial = material()
        self.sectionDiscretisation = 10


    def assignSectionMaterial(self, Mat:material):
        self.sectionMaterial = Mat

    def assignRebarMaterial(self, Mat:material):
        self.rebarMaterial = Mat

    def assignDiscretisation(self, n:int):
        self.sectionDiscretisation = n

    def computeNMM(self,Strains):
        return np.array([0.0,0.0,0.0], dtype=float)

    def computeK(self,Strains):
        return np.zeros((3,3),dtype=float)

    

    def __str__(self):
        a = "Concrete Corners:\n"
        b = str(self.concreteCorners)
        c = "\nRebar Positions:\n"
        d = str(self.rebarPositions)
        e = "\nRebar Diameters:\n"
        f = str(self.rebarDiameters)
        return a+b+c+d+e+f



class ordinaryRectangularSection(section):
    def __init__(self, height, width, concreteCover, topBarNum, bottomBarNum, rightBarNum, leftBarNum, cornerBarDiameter, otherBarDiameter):

        sectionCorners = np.array([[width/2,height/2], [width/2,-height/2], [-width/2,-height/2], [-width/2,height/2]],dtype=float)
        numOfBars = 4 + topBarNum + bottomBarNum + leftBarNum + rightBarNum
        rebarPositions = np.zeros([numOfBars,2])
        rebarDiameters = np.zeros([numOfBars], dtype=float)

        
        rebarDiameters[0:4] = cornerBarDiameter
        Wr = width/2 - concreteCover - cornerBarDiameter/2
        Hr = height/2 - concreteCover - cornerBarDiameter/2
        rebarPositions[0:4,:] = np.array([[Wr,Hr], [Wr,-Hr], [-Wr,-Hr], [-Wr,Hr]])

        rebarDiameters[4:] = otherBarDiameter
        Wr = width/2 - concreteCover - otherBarDiameter/2
        Hr = height/2 - concreteCover - otherBarDiameter/2
        for n, i in enumerate(range(4,4+topBarNum)):
            rebarPositions[i,:] = np.array([-Wr+(Wr*2/(topBarNum+1))*(n+1),Hr],dtype=float)
        for n, i in enumerate(range(4+topBarNum,4+topBarNum+bottomBarNum)):
            rebarPositions[i,:] = np.array([-Wr+(Wr*2/(bottomBarNum+1))*(n+1),-Hr],dtype=float)
        for n, i in enumerate(range(4+topBarNum+bottomBarNum,4+topBarNum+bottomBarNum+rightBarNum)):
            rebarPositions[i,:] = np.array([Wr,-Hr+(Hr*2/(rightBarNum+1))*(n+1)],dtype=float)
        for n, i in enumerate(range(4+topBarNum+bottomBarNum+rightBarNum,4+topBarNum+bottomBarNum+rightBarNum+leftBarNum)):
            rebarPositions[i,:] = np.array([-Wr,-Hr+(Hr*2/(leftBarNum+1))*(n+1)],dtype=float)


        super().__init__(sectionCorners, rebarPositions, rebarDiameters)
        self.width = width; self.height = height

    def computeNMM(self,Strains):
        a = Strains[0]
        c3 = Strains[1]
        c2 = Strains[2]
        N = 0.0; M3 = 0.0; M2 = 0.0
        incrementWidth = self.width/self.sectionDiscretisation
        incrementHeight = self.height/self.sectionDiscretisation
        for i in range(self.sectionDiscretisation):
            for ii in range(self.sectionDiscretisation):
                X = -self.width/2+incrementWidth/2+incrementWidth*ii
                Y = -self.height/2+incrementHeight/2+incrementHeight*i
                n = self.sectionMaterial.stress(a+c3*Y-c2*X)*incrementWidth*incrementHeight
                m3 = n*Y; m2 = -n*X
                N+=n; M3+=m3; M2+=m2

        for i in range(len(self.rebarDiameters)):
            X = self.rebarPositions[i,0]
            Y = self.rebarPositions[i,1]
            As = (self.rebarDiameters[i])**2*m.pi/4
            n = self.rebarMaterial.stress(a+c3*Y-c2*X)*As
            m3 = n*Y; m2 = -n*X
            N+=n; M3+=m3; M2+=m2

            nc = self.sectionMaterial.stress(a+c3*Y-c2*X)*As
            m3c = nc*Y; m2c = -nc*X
            N-=nc; M3-=m3c; M2-=m2c

        return np.array([N,M3,M2],dtype=float)

    def computeK(self, Strains):
        a = Strains[0]
        c3 = Strains[1]
        c2 = Strains[2]
        K = np.zeros((3,3),dtype=float)
        incrementWidth = self.width/self.sectionDiscretisation
        incrementHeight = self.height/self.sectionDiscretisation
        for i in range(self.sectionDiscretisation):
            for ii in range(self.sectionDiscretisation):
                X = -self.width/2+incrementWidth/2+incrementWidth*ii
                Y = -self.height/2+incrementHeight/2+incrementHeight*i
                K[0,0] += self.sectionMaterial.tangentModulus(a+c3*Y-c2*X)*incrementWidth*incrementHeight
                K[0,1] += self.sectionMaterial.tangentModulus(a+c3*Y-c2*X)*Y*incrementWidth*incrementHeight
                K[0,2] += self.sectionMaterial.tangentModulus(a+c3*Y-c2*X)*(-X)*incrementWidth*incrementHeight

                K[1,0] += self.sectionMaterial.tangentModulus(a+c3*Y-c2*X)*Y*incrementWidth*incrementHeight
                K[1,1] += self.sectionMaterial.tangentModulus(a+c3*Y-c2*X)*(Y**2)*incrementWidth*incrementHeight
                K[1,2] += self.sectionMaterial.tangentModulus(a+c3*Y-c2*X)*(-X*Y)*incrementWidth*incrementHeight

                K[2,0] += self.sectionMaterial.tangentModulus(a+c3*Y-c2*X)*(-X)*incrementWidth*incrementHeight
                K[2,1] += self.sectionMaterial.tangentModulus(a+c3*Y-c2*X)*(-X*Y)*incrementWidth*incrementHeight
                K[2,2] += self.sectionMaterial.tangentModulus(a+c3*Y-c2*X)*(X**2)*incrementWidth*incrementHeight

        for i in range(len(self.rebarDiameters)):
            X = self.rebarPositions[i,0]
            Y = self.rebarPositions[i,1]
            As = (self.rebarDiameters[i])**2*m.pi/4
            K[0,0] += self.rebarMaterial.tangentModulus(a+c3*Y-c2*X)*As
            K[0,1] += self.rebarMaterial.tangentModulus(a+c3*Y-c2*X)*Y*As
            K[0,2] += self.rebarMaterial.tangentModulus(a+c3*Y-c2*X)*(-X)*As

            K[1,0] += self.rebarMaterial.tangentModulus(a+c3*Y-c2*X)*Y*As
            K[1,1] += self.rebarMaterial.tangentModulus(a+c3*Y-c2*X)*(Y**2)*As
            K[1,2] += self.rebarMaterial.tangentModulus(a+c3*Y-c2*X)*(-X*Y)*As

            K[2,0] += self.rebarMaterial.tangentModulus(a+c3*Y-c2*X)*(-X)*As
            K[2,1] += self.rebarMaterial.tangentModulus(a+c3*Y-c2*X)*(-X*Y)*As
            K[2,2] += self.rebarMaterial.tangentModulus(a+c3*Y-c2*X)*(X**2)*As


            K[0,0] -= self.sectionMaterial.tangentModulus(a+c3*Y-c2*X)*As
            K[0,1] -= self.sectionMaterial.tangentModulus(a+c3*Y-c2*X)*Y*As
            K[0,2] -= self.sectionMaterial.tangentModulus(a+c3*Y-c2*X)*(-X)*As

            K[1,0] -= self.sectionMaterial.tangentModulus(a+c3*Y-c2*X)*Y*As
            K[1,1] -= self.sectionMaterial.tangentModulus(a+c3*Y-c2*X)*(Y**2)*As
            K[1,2] -= self.sectionMaterial.tangentModulus(a+c3*Y-c2*X)*(-X*Y)*As

            K[2,0] -= self.sectionMaterial.tangentModulus(a+c3*Y-c2*X)*(-X)*As
            K[2,1] -= self.sectionMaterial.tangentModulus(a+c3*Y-c2*X)*(-X*Y)*As
            K[2,2] -= self.sectionMaterial.tangentModulus(a+c3*Y-c2*X)*(X**2)*As

        return K
    
    def computeM_muDiagram(self,mu_increment,increment_num):
        K = self.computeK(np.zeros((3),dtype=float))
        fint = self.computeNMM(np.zeros((3),dtype=float))
        fext = np.zeros((3),dtype=float)
        d_all = np.zeros((increment_num+1, 3),dtype=float)
        d = np.zeros((3),dtype=float)
        lamb_all = np.zeros((increment_num+1),dtype=float)
        lamb = 0.0

        Ktt = K[[True,False,True],][:,[True,False,True]]
        Ktc = K[[True,False,True],][:,[False,True,False]]
        Kct = K[[False,True,False],][:,[True,False,True]]
        Kcc = K[[False,True,False],][:,[False,True,False]]

        fp = np.array([0,1,0],dtype=float)
        fpt = fp[[True,False,True]]
        fpc = fp[[False,True,False]]

        for i in range(increment_num):
            print(i)
            deltad = np.array([0,mu_increment,0],dtype=float)
            d += deltad

            F1 = -np.matmul(Ktc,deltad[[1]]) + fext[[True,False,True]] - fint[[True,False,True]]
            F2 = -np.matmul(Kcc,deltad[[1]]) + fext[[False,True,False]] - fint[[False,True,False]]
            F = np.zeros((3),dtype=float)
            F[0:2] = F1 ; F[2] = F2[0]
            F_norm = np.linalg.norm(F)
            while F_norm>10:
                K1 = np.zeros((3,3),dtype=float)
                K1[0:2,0:2] = Ktt
                K1[2,0:2] = Kct
                K1[0:2,2] = -fpt
                K1[2,2] = -fpc[0]

                sol = np.linalg.solve(K1,F)
                d[0] += sol[0]
                d[2] += sol[1]
                lamb += sol[2]
                deltad[1] = 0.0

                K = self.computeK(d)
                fint = self.computeNMM(d)
                fext += sol[2] * fp
                Ktt = K[[True,False,True],][:,[True,False,True]]
                Ktc = K[[True,False,True],][:,[False,True,False]]
                Kct = K[[False,True,False],][:,[True,False,True]]
                Kcc = K[[False,True,False],][:,[False,True,False]]
                F1 = fext[[True,False,True]] - fint[[True,False,True]]
                F2 = fext[[False,True,False]] - fint[[False,True,False]]
                F = np.zeros((3),dtype=float)
                F[0:2] = F1 ; F[2] = F2[0]
                F_norm = np.linalg.norm(F)
            d_all[i+1,:] = d
            lamb_all[i+1] = lamb

        return (d_all,lamb_all)

            

                


            
