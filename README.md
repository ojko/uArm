# uArm
Programs for controlling a uArm 

Here are a few short programs written in python 3 for controlling the ufactory uArm. They are written and tested on linux so you would need to change the serial port to comX if using under windows.

<b>uarmControl.py</b><br> 
Takes the end effector position as a user argument to move the arm.
<pre>./uamControl.py 0 100 -40 0 1</pre>

<ul>
<li>Argument 1 is arm rotation</li>
<li>Argument 2 is arm length</li>
<li>Argument 3 is arm height</li>
<li>Argument 4 is wrist rotation</li>
<li>Argument 5 is gripper activation eg 0 off 1 on</li>
</ul>

The serial device can be changed with argument 6 if you have more serial devices connected
<pre>./uamControl.py 0 0 0 0 0 /dev/ttyUSB1</pre>

<b>uarmControlCSV.py</b><br> 
Reads the end effector position from a CSV file to run a sequence of moves.
<pre>./uarmControlCSV.py position.csv</pre>

The csv should be formated with the postions as armRotation,armLength,armHeight,wristRotation,gripper

The serial device can be changed with argument 2 if you have more serial devices connected
<pre>./uarmControlCSV.py position.csv /dev/ttyUSB1</pre>

<b>uarmController.py</b><br> 
Moves the end effector using a game pad controller. The program has been set up using a xbox controller so the get_axis() values may change if you using a different controller
<pre>./uarmController.py</pre>
