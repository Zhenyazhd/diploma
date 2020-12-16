from z3 import *
import random as rand

I = IntSort()
R = RealSort()
Adr = DeclareSort('Address')

zero, sm_c, wallet, a0, a1, a2, a3, a4, a5 = Consts('zero sm_c wallet a0 a1 a2 a3 a4 a5', Adr)
_rate, _totalSupply, = Reals('_rate _totalSupply')

time = Array('time', I, I)
weiRaised = Array('weiRaised', I, R)
_min = Array('_min', I, R)
owner = Array('owner', I, Adr)

balance_a0 = Array('balance_a0', I, R)
balance_a1 = Array('balance_a1', I, R)
balance_a2 = Array('balance_a2', I, R)
balance_a3 = Array('balance_a3', I, R)
balance_a4 = Array('balance_a4', I, R)
balance_a5 = Array('balance_a5', I, R)
Tbalances_a0 = Array('Tbalance_a0', I, R)
Tbalances_a1 = Array('Tbalance_a1', I, R)
Tbalances_a2 = Array('Tbalance_a2', I, R)
Tbalances_a3 = Array('Tbalance_a3', I, R)
Tbalances_a4 = Array('Tbalance_a4', I, R)
Tbalances_a5 = Array('Tbalance_a5', I, R)

#args for functions
m_s_trOwn = Array('m_s_trOwn', I, Adr)
m_v_trOwn = Array('m_v_trOwn', I, R)
m_s_buyT = Array('m_s_buyT', I, Adr)
m_v_buyT = Array('m_v_buyT', I, R)
m_s_setMin = Array('m_s_setMin', I, Adr)
m_v_setMin = Array('m_v_setMin', I, R)
m_s_trFr = Array('m_s_trFr', I, Adr)
m_v_trFr = Array('m_v_trFr', I, R)

newOwner = Array('newOwner', I, Adr) #transferOwnership
beneficiary = Array('beneficiary', I, Adr) #buyTokens
sender = Array('sender', I, Adr) #transferFrom
recipient = Array('recipient', I, Adr) #transferFrom

amount = Array('amount', I, R) #transferFrom
value = Array('value', I, R) #setMin

# events 
#Ev = DeclareSort('Event')
#Transfer, SetMin, OwnershipTransferred, TokensPurchased = \
#                    Consts('Transfer SetMin OwnershipTransferred TokensPurchased', Ev)
#E = [Transfer, SetMin, OwnershipTransferred, TokensPurchased]

def init(k): 
    P_t = True
    P_ms = True
    P_Tbalance = True
    I = Solver()

    for i in range(k+1):
        P_t = And(P_t, time[i] < time[i+1])
        
        P_ms = And(P_ms, Not(Or(m_s_trOwn[time[i]] == sm_c, m_s_buyT[time[i]] == sm_c, 
                                m_s_setMin[time[i]] == sm_c, m_s_trFr[time[i]] == sm_c,
                                m_s_trOwn[time[i]] == a0, m_s_buyT[time[i]] == a0, 
                                m_s_setMin[time[i]] == a0, m_s_trFr[time[i]] == a0)))
        
        P_Tbalance = And(P_Tbalance, Tbalances_a0[time[i]] + Tbalances_a1[time[i]] + Tbalances_a2[time[i]] + \
            Tbalances_a3[time[i]] + Tbalances_a4[time[i]] + Tbalances_a5[time[i]] == _totalSupply)

      
    I.add(And(sm_c == a1, wallet == a2, owner[time[0]] == a3, _rate > 0, weiRaised[time[0]] == 0,
            _min[time[0]] == 0, _totalSupply > 0, balance_a0[time[0]] == 0, 
            balance_a1[time[0]] == 0, balance_a2[time[0]] >= 0, balance_a3[time[0]] > 0, 
            balance_a4[time[0]] > 0, balance_a5[time[0]] > 0, Tbalances_a3[time[0]] == _totalSupply, 
            newOwner[time[0]] == a0, beneficiary[time[0]] == a0, sender[time[0]] == a0, 
            recipient[time[0]] == a0, amount[time[0]] == 0, value[time[0]] == 0, 
            m_v_trOwn[time[0]] == 0, m_s_trOwn[time[0]] == zero, m_s_buyT[time[0]] == zero, 
            m_v_buyT[time[0]] == 0, m_s_setMin[time[0]] == zero, m_v_setMin[time[0]] == 0, 
            m_s_trFr[time[0]] == zero, m_v_trFr[time[0]] == 0))
    
    return I, P_Tbalance, P_ms, P_t  

def path(k, I, P1, P2, P3): #P1 - P balance
    for i in range(k):
        I.add(Or(And(value[time[i+1]] > 0, m_s_setMin[time[i+1]] == owner[time[i]],   #setMin
                                    m_v_setMin[time[i+1]] == 0, 
                                    weiRaised[time[i+1]] == weiRaised[time[i]],
                                    _min[time[i+1]] == value[time[i]],  
                                    owner[time[i+1]] == owner[time[i]],
                                    balance_a0[time[i+1]] == balance_a0[time[i]], 
                                    balance_a1[time[i+1]] == balance_a1[time[i]],
                                    balance_a2[time[i+1]] == balance_a2[time[i]], 
                                    balance_a3[time[i+1]] == balance_a3[time[i]] , 
                                    balance_a4[time[i+1]] ==  balance_a5[time[i]], 
                                    balance_a5[time[i+1]] == balance_a5[time[i]],
                                    Tbalances_a0[time[i+1]] == Tbalances_a0[time[i]], 
                                    Tbalances_a1[time[i+1]] == Tbalances_a1[time[i]], 
                                    Tbalances_a2[time[i+1]] == Tbalances_a2[time[i]],  
                                    Tbalances_a3[time[i+1]] == Tbalances_a3[time[i]], 
                                    Tbalances_a4[time[i+1]] == Tbalances_a4[time[i]],
                                    Tbalances_a5[time[i+1]] == Tbalances_a5[time[i]]),

                                    And(Or(Not(Or(newOwner[time[i+1]] == owner[time[i]],    #transferOwnership
                                    newOwner[time[i+1]] == a0)), newOwner[time[i+1]] == a3, 
                                    newOwner[time[i+1]] == a4, newOwner[time[i+1]] == a5 ), 
                                    m_s_trOwn[time[i+1]] == owner[time[i]], m_v_trOwn[time[i+1]] == 0,
                                    owner[time[i+1]] == newOwner[time[i+1]], 
                                    weiRaised[time[i+1]] == weiRaised[time[i]],
                                    balance_a0[time[i+1]] == balance_a0[time[i]], 
                                    balance_a1[time[i+1]] == balance_a1[time[i]],
                                    balance_a2[time[i+1]] == balance_a2[time[i]], 
                                    balance_a3[time[i+1]] == balance_a3[time[i]] , 
                                    balance_a4[time[i+1]] ==  balance_a5[time[i]], 
                                    balance_a5[time[i+1]] == balance_a5[time[i]],
                                    Tbalances_a0[time[i+1]] == Tbalances_a0[time[i]], 
                                    Tbalances_a1[time[i+1]] == Tbalances_a1[time[i]], 
                                    Tbalances_a2[time[i+1]] == Tbalances_a2[time[i]],  
                                    Tbalances_a3[time[i+1]] == Tbalances_a3[time[i]], 
                                    Tbalances_a4[time[i+1]] == Tbalances_a4[time[i]],
                                    Tbalances_a5[time[i+1]] == Tbalances_a5[time[i]]), 

                                    And(Or(And(sender[time[i+1]] == a3,    #transferFrom
                                    Tbalances_a3[time[i+1]] == Tbalances_a3[time[i]] - amount[time[i+1]],
                                    Tbalances_a0[time[i+1]] == Tbalances_a0[time[i]], 
                                    Tbalances_a1[time[i+1]] == Tbalances_a1[time[i]], 
                                    Tbalances_a2[time[i+1]] == Tbalances_a2[time[i]],  
                                    Tbalances_a4[time[i+1]] == Tbalances_a4[time[i]],
                                    Tbalances_a5[time[i+1]] == Tbalances_a5[time[i]]),

                                    And(sender[time[i+1]] == a4, 
                                    Tbalances_a4[time[i+1]] == Tbalances_a4[time[i]] - amount[time[i+1]],
                                    Tbalances_a0[time[i+1]] == Tbalances_a0[time[i]], 
                                    Tbalances_a1[time[i+1]] == Tbalances_a1[time[i]], 
                                    Tbalances_a2[time[i+1]] == Tbalances_a2[time[i]],  
                                    Tbalances_a3[time[i+1]] == Tbalances_a3[time[i]],
                                    Tbalances_a5[time[i+1]] == Tbalances_a5[time[i]]), 

                                    And(sender[time[i+1]] == a5, 
                                    Tbalances_a5[time[i+1]] == Tbalances_a5[time[i]] - amount[time[i+1]],
                                    Tbalances_a0[time[i+1]] == Tbalances_a0[time[i]], 
                                    Tbalances_a1[time[i+1]] == Tbalances_a1[time[i]], 
                                    Tbalances_a2[time[i+1]] == Tbalances_a2[time[i]],  
                                    Tbalances_a3[time[i+1]] == Tbalances_a3[time[i]], 
                                    Tbalances_a4[time[i+1]] == Tbalances_a4[time[i]]),

                                    And(recipient[time[i+1]] == a3,
                                    Tbalances_a3[time[i+1]] == Tbalances_a3[time[i]] + amount[time[i+1]],
                                    Tbalances_a0[time[i+1]] == Tbalances_a0[time[i]], 
                                    Tbalances_a1[time[i+1]] == Tbalances_a1[time[i]], 
                                    Tbalances_a2[time[i+1]] == Tbalances_a2[time[i]],  
                                    Tbalances_a4[time[i+1]] == Tbalances_a4[time[i]],
                                    Tbalances_a5[time[i+1]] == Tbalances_a5[time[i]]),

                                    And(recipient[time[i+1]] == a4,
                                    Tbalances_a4[time[i+1]] == Tbalances_a4[time[i]] + amount[time[i+1]],
                                    Tbalances_a0[time[i+1]] == Tbalances_a0[time[i]], 
                                    Tbalances_a1[time[i+1]] == Tbalances_a1[time[i]], 
                                    Tbalances_a2[time[i+1]] == Tbalances_a2[time[i]],  
                                    Tbalances_a3[time[i+1]] == Tbalances_a3[time[i]], 
                                    Tbalances_a5[time[i+1]] == Tbalances_a5[time[i]]),

                                    And(recipient[time[i+1]] == a5, 
                                    Tbalances_a5[time[i+1]] == Tbalances_a5[time[i]] + amount[time[i+1]]),
                                    Tbalances_a0[time[i+1]] == Tbalances_a0[time[i]], 
                                    Tbalances_a1[time[i+1]] == Tbalances_a1[time[i]], 
                                    Tbalances_a2[time[i+1]] == Tbalances_a2[time[i]],  
                                    Tbalances_a3[time[i+1]] == Tbalances_a3[time[i]], 
                                    Tbalances_a4[time[i+1]] == Tbalances_a4[time[i]]),

                                    amount[time[i+1]] > 0, m_s_trFr[time[i+1]] == sender[time[i+1]],     
                                    m_v_trFr[time[i+1]] == 0, owner[time[i+1]] == owner[time[i]], 
                                    weiRaised[time[i+1]] == weiRaised[time[i]],
                                    owner[time[i+1]] == owner[time[i]],
                                    balance_a0[time[i+1]] == balance_a0[time[i]], 
                                    balance_a1[time[i+1]] == balance_a1[time[i]],
                                    balance_a2[time[i+1]] == balance_a2[time[i]], 
                                    balance_a3[time[i+1]] == balance_a3[time[i]], 
                                    balance_a4[time[i+1]] == balance_a5[time[i]], 
                                    balance_a5[time[i+1]] == balance_a5[time[i]],),

                                    And(m_s_buyT[time[i+1]] == owner[time[i]],   #buyTokens
                                    m_v_buyT[time[i+1]] > 0, Or(
                                    And(beneficiary[time[i+1]] == a2,
                                    Tbalances_a2[time[i+1]] == Tbalances_a2[time[i]] + _rate*m_v_buyT[time[i+1]],
                                    Tbalances_a0[time[i+1]] == Tbalances_a0[time[i]], 
                                    Tbalances_a1[time[i+1]] == Tbalances_a1[time[i]], 
                                    Tbalances_a3[time[i+1]] == Tbalances_a3[time[i]], 
                                    Tbalances_a4[time[i+1]] == Tbalances_a4[time[i]],
                                    Tbalances_a5[time[i+1]] == Tbalances_a5[time[i]]),

                                    And(beneficiary[time[i+1]] == a3,
                                    Tbalances_a3[time[i+1]] == Tbalances_a3[time[i]] + _rate*m_v_buyT[time[i+1]],
                                    Tbalances_a0[time[i+1]] == Tbalances_a0[time[i]], 
                                    Tbalances_a1[time[i+1]] == Tbalances_a1[time[i]], 
                                    Tbalances_a2[time[i+1]] == Tbalances_a2[time[i]], 
                                    Tbalances_a4[time[i+1]] == Tbalances_a4[time[i]],
                                    Tbalances_a5[time[i+1]] == Tbalances_a5[time[i]]), 

                                    And(beneficiary[time[i+1]] == a4,
                                    Tbalances_a4[time[i+1]] == Tbalances_a4[time[i]] + _rate*m_v_buyT[time[i+1]],
                                    Tbalances_a0[time[i+1]] == Tbalances_a0[time[i]], 
                                    Tbalances_a1[time[i+1]] == Tbalances_a1[time[i]], 
                                    Tbalances_a2[time[i+1]] == Tbalances_a2[time[i]],  
                                    Tbalances_a3[time[i+1]] == Tbalances_a3[time[i]], 
                                    Tbalances_a5[time[i+1]] == Tbalances_a5[time[i]]),

                                    And(beneficiary[time[i+1]] == a5,
                                    Tbalances_a5[time[i+1]] == Tbalances_a5[time[i]] + _rate*m_v_buyT[time[i+1]]),
                                    Tbalances_a0[time[i+1]] == Tbalances_a0[time[i]], 
                                    Tbalances_a1[time[i+1]] == Tbalances_a1[time[i]], 
                                    Tbalances_a2[time[i+1]] == Tbalances_a2[time[i]],  
                                    Tbalances_a3[time[i+1]] == Tbalances_a3[time[i]], 
                                    Tbalances_a4[time[i+1]] == Tbalances_a4[time[i]]),

                                    weiRaised[time[i+1]] == weiRaised[time[i]] + m_v_buyT[time[i+1]],
                                    If(owner[time[i+1]] == a3, 
                                    And(balance_a3[time[i+1]] == balance_a3[time[i]] - m_v_buyT[time[i+1]],
                                    balance_a0[time[i+1]] == balance_a0[time[i]], 
                                    balance_a1[time[i+1]] == balance_a1[time[i]],
                                    balance_a2[time[i+1]] == balance_a2[time[i]],  
                                    balance_a4[time[i+1]] == balance_a5[time[i]], 
                                    balance_a5[time[i+1]] == balance_a5[time[i]]), True),
                                    If(owner[time[i+1]] == a4, 
                                    And(balance_a4[time[i+1]] == balance_a4[time[i]] - m_v_buyT[time[i+1]],
                                    balance_a0[time[i+1]] == balance_a0[time[i]], 
                                    balance_a1[time[i+1]] == balance_a1[time[i]],
                                    balance_a2[time[i+1]] == balance_a2[time[i]], 
                                    balance_a3[time[i+1]] == balance_a3[time[i]], 
                                    balance_a5[time[i+1]] == balance_a5[time[i]]), True),
                                    If(owner[time[i+1]] == a5, 
                                    And(balance_a5[time[i+1]] == balance_a5[time[i]] - m_v_buyT[time[i+1]],
                                    balance_a0[time[i+1]] == balance_a0[time[i]], 
                                    balance_a1[time[i+1]] == balance_a1[time[i]],
                                    balance_a2[time[i+1]] == balance_a2[time[i]], 
                                    balance_a3[time[i+1]] == balance_a3[time[i]], 
                                    balance_a4[time[i+1]] == balance_a5[time[i]]), True))))             
    print(I.check(), I.statistics())
    return I
    





def main():
    ar = init(3)
    I = ar[0]
    P_Tbalance = ar[1]
    P_ms = ar[2] 
    P_t = ar[2]
    i = path(3 , I, P_Tbalance, P_ms, P_t)
    
    
    


if __name__ == '__main__':
    main()


