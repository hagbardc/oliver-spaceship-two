from systemstate import SystemState

cs = [ ('button01', 'button'), ('mc', 'missile_controller'), ('switch01', 'button')]
ss = SystemState(cs)

ss.printState()
