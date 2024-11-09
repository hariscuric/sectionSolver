import Section as sec


def main():

    a = sec.concrete(30,1)
    b = [a.tangentModulus(i/10000) for i in range(-10,50)]
    print(b)




main()