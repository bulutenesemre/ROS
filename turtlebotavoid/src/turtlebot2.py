#! /usr/bin/env python

import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist,Vector3


def callback(msg):

    shortrange = 0.5
    mediumrange = 1.0
    longrange = 2.0

    left = msg.ranges[:360] #0-90
    front = msg.ranges[360:481] #90-120
    right = msg.ranges[481:] #120-180
    #print msg.ranges[:360] #You can print

    if min(left) < mediumrange  and min(front)>=mediumrange:
        move = Twist(
            Vector3(0.3, 0, 0),
            Vector3(0, 0, 0.45)
        )
    elif min(right) <mediumrange and min(front)>=mediumrange:
        move = Twist(
            Vector3(0.3, 0, 0),
            Vector3(0, 0, -0.45)
        )
    elif min(left) <shortrange:
        move = Twist(
            Vector3(0, 0, 0),
            Vector3(0, 0, -0.25)
        )
    elif min(right) <shortrange:
        move = Twist(
            Vector3(0, 0, 0),
            Vector3(0, 0, 0.25)
        )
    elif min(left) < longrange and min(front) < longrange:
        # If it's closing to the wall getting slows the velocity and rotate value
        move = Twist(
            Vector3(0.25, 0, 0),
            Vector3(0, 0, 0.65)
        )

    elif min(right) < longrange and min(front) < longrange :
        move = Twist(
            Vector3(0.35, 0, 0),
            Vector3(0, 0, -0.65)
        )

    else:
        move = Twist(
            Vector3(0.3, 0, 0),
            Vector3(0, 0, 0.0)
        )


    pub.publish(move)

rospy.init_node('turtlebot2_node') #Determine name of node
sub = rospy.Subscriber('/kobuki/laser/scan', LaserScan, callback) #We subscribe to the laser's topic
pub = rospy.Publisher('/cmd_vel', Twist) #We publish velocity to master
rospy.spin() #All callbacks get called for subscribers.