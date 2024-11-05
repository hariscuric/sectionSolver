import numpy as np



def inputSection():


    return 0


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
