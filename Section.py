import numpy as np



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
        if strain<0.0:
            return 0.0
        elif strain<=self.ec2:
            return self.fcd * (1-(1-strain/self.ec2)**self.n)
        elif strain<=self.ecu2:
            return self.fcd
        elif strain>self.ecu2 and strain<=self.ecu2*1.05:
            return self.fcd*((self.ecu2*1.05-strain)/(0.05*self.ecu2))
        else:
            return 0.0
        
    def tangentModulus(self, strain):
        if strain<0.0:
            return 0.0
        elif strain<=self.ec2:
            return (self.n*self.fcd/self.ec2)*((1-strain/self.ec2)**(self.n-1))
        elif strain>self.ecu2 and strain<=self.ecu2*1.05:
            return -self.fcd/(0.05*self.ecu2)
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

    def computeNMM(self,axialStrain,curvatureM3,curvatureM2):
        return np.array([0.0,0.0,0.0], dtype=float)

    

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
        return np.array([N,M3,M2],dtype=float)
            
