#include "ros/ros.h"
#include "geometry_msgs/Twist.h"
#include <turtlesim/Pose.h>

#include <math.h>
#include <string.h>
using namespace std;

ros::Publisher vel_publisher;
ros::Subscriber pose_subscriber;
turtlesim::Pose turtlesim_pose;
//**************
#define Ts 50
float PI=3.14159265359;
int j=0,k=0,c=0;
float R2D=180/PI,D2R=PI/180;
//**************
//void PointToPoint(double xr0,double xt, double yr0, double yt,double yawt,double yawr0,double yawpath);
void posecallback(const turtlesim::Pose::ConstPtr & pose_message);
//************************
int main(int argc, char **argv){
    double errortheta=0.0, theta0=0,vx=0,wz=0;
    geometry_msgs::Twist vel_msgs;
    string svx,swz;

    ros::init(argc,argv,"lab1_1");


    ros::NodeHandle n;
    ros::NodeHandle nh("~");
    ros::Rate r(Ts);
    //ros::param::get("vx",vx);
    //ros::param::get("wz",wz);// unit is degree

    vel_publisher=n.advertise<geometry_msgs::Twist>("/turtle1/cmd_vel",1000);
    pose_subscriber=n.subscribe("/turtle1/pose",1,posecallback);

    cout<<"please enter vx (m/s):"<<endl;
    cin>>svx;
    cout<<"please enter wz (degree) :"<<endl;
    cin>>swz;
    vx=stoi(svx);
    wz=stoi(swz);
    cout<<"Launch parameters are --> User Linear Vel: "<<vx<<" User Angular Vel: "<<wz<<endl;
    ros::Duration(2).sleep();
    ros::spinOnce();
    ros::Duration(2).sleep();
    theta0=turtlesim_pose.theta;
    vel_msgs.linear.x=vx;
    vel_msgs.linear.y=0;
    vel_msgs.linear.z=0;
    vel_msgs.angular.z=wz*D2R;
    vel_msgs.angular.y=0;
    vel_msgs.angular.x=0;
    cout<<"8 shape movement will start \n";

    do {
    errortheta=turtlesim_pose.theta*R2D-theta0;
    vel_publisher.publish(vel_msgs);

    if (abs(errortheta)<1.1 && c>50){
        k++;
        c=0;
        wz=-wz;}
    c++;
    vel_msgs.angular.z=-wz*D2R;
    errortheta=turtlesim_pose.theta-theta0;
    vel_publisher.publish(vel_msgs);
    ros::spinOnce();
    r.sleep();
    //cout<<c<<endl;
        }while(1);
        cout<<"K : "<<k<<"count: "<<c<<endl;
        return 0;
}
//**********************************************************************

void posecallback(const turtlesim::Pose::ConstPtr & pose_message){

        turtlesim_pose.x=pose_message->x;
        turtlesim_pose.y=pose_message->y;
        turtlesim_pose.theta=pose_message->theta;
        cout<<"turtla1 x pos : "<< turtlesim_pose.x<<" turtla1 y pos : "<< turtlesim_pose.y<<" turtla1 theta orientation : "<< turtlesim_pose.theta*R2D<<endl;

}

//void PointToPoint(double xr0,double xt, double yr0, double yt,double yawt,double yawr0,double yawpath){

//                }

