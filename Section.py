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
        else:
            return 0.0
        
    def tangentModulus(self, strain):
        if strain<0.0:
            return 0.0
        elif strain<=self.ec2:
            return (self.n*self.fcd/self.ec2)*((1-strain/self.ec2)**(self.n-1))
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
            return -self.fyd + (strain-ey)*(self.fyd*(self.k-1)/(self.euk-ey))
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
        else:
            return 0.0





class section:
    def __init__(self, sectionCorners, rebarPositions, rebarDiameters):
        self.concreteCorners = sectionCorners
        self.rebarPositions = rebarPositions
        self.rebarDiameters = rebarDiameters

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
