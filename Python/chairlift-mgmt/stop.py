stopcheck=1

import shared
import status


while shared.go==1:
    if shared.op=="e":
        status.mainstatus=3

    if shared.op=="nn e":
        status.mainstatus=2