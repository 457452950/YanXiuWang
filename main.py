import os

import StateMachine

def debug_info():
    print("running dir : ", os.getcwd())

# main
if __name__ == "__main__":
    debug_info()

    # 已验证
    # loop = State.StateMachine()
    # loop.run()

    # or
    ser = StateMachine.Service()
    ser.run()
