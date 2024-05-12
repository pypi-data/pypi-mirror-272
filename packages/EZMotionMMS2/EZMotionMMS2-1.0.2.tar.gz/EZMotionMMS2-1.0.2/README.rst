
EZMotionMMS2
========================

Python wrapper built around minimalmodbus for controlling EZMotion MMP/ MMS 740 and 760 series servo motors and driver modules via USB serial-to-RS485 converter.
<br>(Unless required by applicable law or agreed to in writing, software is distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.)



![Wiring Diagram](https://github.com/EZmotionTechnologies/Python_API_EZM2/tree/main/EZMotionMMS2/img/Wiring.JPG )

Example: Position Mode (Single motor)
--------------
::

    from EZMotionMMS2 import *
    Motor1= Ezm("COM24", 1, 115200)
    Motor1.Shutdown()                  # Shutdown and Enable the motor

    # Set modes of operation to Relative Position mode
    Motor1.Set_Op_Mode("POSITION REL")

    #print selected modes of operation
    print(Motor1.Read_Op_Mode())

    Motor1.Enable_Motor()

    #send new target position (10 turns + 180 degrees in CCW direction) to the motor and update
    Motor1.Set_Target_Position(10,180,"CCW")
    Motor1.Update()

    # wait for the motor to reach target position
    while (Motor1.Pos_Target_Check_Flag() == False):
        pass

    # Read and print motors current position
    turns,angle = Motor1.Read_Actual_Position()
    print("Turns = ", turns)
    print("Angle = ", angle)

    #send new target position to the motor and update
    Motor1.Set_Target_Position(5,180,"CW")
    Motor1.Update()

    # wait for the motor to reach target position
    while (Motor1.Pos_Target_Check_Flag() == False):
        pass

    Motor1.Disable_Motor()

Example: Speed Mode (Single motor)
--------------
::

    import time
    from EZMotionMMS2 import *
    #Create motor object with slave address 1 and port COM24
    Motor1= Ezm("COM24", 1, 115200)
    Motor1.Shutdown()

    # Set modes of operation to Speed mode
    Motor1.Set_Op_Mode("SPEED")
    Motor1.Shutdown()

    Motor1.Set_Acceleration(500)
    Motor1.Set_Deceleration(500)

    # Set target velocity to 1000rpm in CW direction
    Motor1.Set_Target_Velocity(-1000)

    Motor1.Enable_Motor()
    time.sleep(5)
    #read and print motor actual velocity
    print("Motor Speed = ", Motor1.Read_Actual_Velocity())

    #print selected modes of operation
    print(Motor1.Read_Op_Mode())

    # Set target velocity to 1000rpm in CCW direction
    Motor1.Set_Target_Velocity(1000)

    time.sleep(5)
    Motor1.Disable_Motor()


Example: Torque Mode (Single motor)
--------------
::

    from EZMotionMMS2 import *
    import time

    #Create motor object with slave address 1 and port COM24
    Motor1= Ezm("COM24", 1, 115200)

    Motor1.Shutdown()

    # Set modes of operation to Torque mode
    Motor1.Set_Op_Mode("TORQUE")

    #Set target motor torque
    Motor1.Set_Target_Torque(-80)

    Motor1.Enable_Motor()

    #read and print actual motor torque
    print(Motor1.Read_Actual_Torque())
    time.sleep(15)

    #read and print motor actual velocity
    print("Motor Speed = ", Motor1.Read_Actual_Velocity())

    #read and print actual motor torque
    print(Motor1.Read_Actual_Torque())

    #print selected modes of operation
    print(Motor1.Read_Op_Mode())

    Motor1.Disable_Motor()


Example: Homing Mode (Single motor)
--------------
::

    from EZMotionMMS2 import *
    import time
    Motor1= Ezm( "COM24", 1, 115200)
    Motor1.Shutdown()
    Motor1.Set_Op_Mode("HOMING")
    Motor1.Shutdown()
    Motor1.Homing_Method(-3)
    Motor1.Homing_Torque(200)
    Motor1.Update()


    Motor1.Enable_Motor()
    time.sleep(5)
    print("Motor Speed = ", Motor1.Read_Actual_Velocity())
    print(Motor1.Read_Op_Mode())
    # Motor1.Set_Target_Velocity(1000)
    time.sleep(5)

    Motor1.Disable_Motor()


Example: Speed Mode (Dual motor)
--------------
::

    import time
    from EZMotionMMS2 import *
    #Create motor object with slave address 1 and port COM?
    Motor1= Ezm("COM24", 1, 115200)
    #Create 2nd motor object with slave address 2 and port COM?
    Motor2= Ezm("COM2", 2, 115200)
    Motor1.Shutdown()
    Motor2.Shutdown()

    # Set modes of operation to Speed mode
    Motor1.Set_Op_Mode("SPEED")
    Motor1.Shutdown()
    Motor2.Set_Op_Mode("SPEED")
    Motor2.Shutdown()


    Motor1.Set_Acceleration(500)
    Motor1.Set_Deceleration(500)

    Motor2.Set_Acceleration(500)
    Motor2.Set_Deceleration(500)

    # Set target velocity to 1000rpm in CW direction
    Motor1.Set_Target_Velocity(-1000)

    # Set target velocity to 1000rpm in CCW direction for 2nd motor
    Motor2.Set_Target_Velocity(1000)

    Motor1.Enable_Motor()
    Motor2.Enable_Motor()
    time.sleep(5)
    #read and print motor actual velocity
    print("Motor Speed = ", Motor1.Read_Actual_Velocity())
    print("Motor Speed = ", Motor2.Read_Actual_Velocity())

    #print selected modes of operation
    print(Motor1.Read_Op_Mode())
    print(Motor2.Read_Op_Mode())

    # Set target velocity to 1000rpm in CCW direction
    Motor1.Set_Target_Velocity(1000)

    # Set target velocity to 1000rpm in CW direction for 2nd motor
    Motor2.Set_Target_Velocity(-1000)

    time.sleep(5)
    Motor1.Disable_Motor()
    Motor2.Disable_Motor()

