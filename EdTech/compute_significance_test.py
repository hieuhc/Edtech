'''
Created on Oct 9, 2015

@author: HCH
'''
import math
def t_Welch_comp(x1_mean, s1, n1, x2_mean, s2, n2):
    t = (x1_mean - x2_mean) / math.sqrt(s1*s1/n1 + s2*s2/n2)
    return t
def t_comp(x1_mean, s1, n1, x2_mean, s2, n2):
    t = (x1_mean - x2_mean) / math.sqrt((1/n1 + 1/n2)*((n1-1)*s1*s1 + (n2-1)*s2*s2)/(n1+n2-2))
    return t
if __name__ == '__main__':    
    print(t_Welch_comp(28.66 , 3.87, 20, 29.65, 4.97, 20))