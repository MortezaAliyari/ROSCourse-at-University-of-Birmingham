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
void PointToPoint(double xr0,double xt, double yr0, double yt,double yawr0,double yawpath);
void posecallback(const turtlesim::Pose::ConstPtr & pose_message);
//************************
int main(int argc, char **argv){


    double errortheta=0.0, theta0=0,vx=0,wz=0,yawr0=0,yawpath=0,xr0=0,yr0=0,l=0,xr=0,yr=0;

    geometry_msgs::Twist vel_msgs;
    string sl;
    ros::init(argc,argv,"lab1_2");
    ros::NodeHandle n;
    ros::NodeHandle nh("~");
    ros::Rate r(Ts);
    //ros::param::get("vx",vx);
    //ros::param::get("wz",wz);// unit is degree

    vel_publisher=n.advertise<geometry_msgs::Twist>("/turtle1/cmd_vel",1000);
    pose_subscriber=n.subscribe("/turtle1/pose",1,posecallback);

    cout<<"please length of square:"<<endl;
    cin>>sl;
    l=stoi(sl);
    ros::Duration(2).sleep();
    ros::spinOnce();
    ros::Duration(2).sleep();
    theta0=turtlesim_pose.theta;
    xr0=turtlesim_pose.x;
    yr0=turtlesim_pose.y;
    double xt[5]={xr0,xr0+l,xr0+l,xr0  ,xr0};
    double yt[5]={yr0,yr0  ,yr0+l,yr0+l,yr0};
    vel_msgs.linear.x=vx;
    vel_msgs.linear.y=0;
    vel_msgs.linear.z=0;
    vel_msgs.angular.z=wz*D2R;
    vel_msgs.angular.y=0;
    vel_msgs.angular.x=0;
    cout<<"turtle will move in square with side length : "<<l<<endl;
    while (l<=0){cout<<"are you kidding?! the lengt is zero or negative!!"<<endl;};
    do {

        xr=turtlesim_pose.x;
        yr=turtlesim_pose.y;
        yawpath=atan2((yt[c+1]-yr),(xt[c+1]-xr));
        yawr0=turtlesim_pose.theta;
        PointToPoint(xr,xt[c+1],yr,yt[c+1],yawr0,yawpath);

        cout<<"c: "<<c<<endl;
        c++;
        cout<<"Direct Path Yaw Angle "<<yawpath*R2D<<" Robot Yaw Angle "<<turtlesim_pose.theta*R2D<<" yr0"<<" : "<<yr0<<"\n";

        ros::spinOnce();
        r.sleep();
        if (c>3)
            c=0;
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

void PointToPoint(double xr0,double xt, double yr0, double yt,double yawr0,double yawpath){
        ros::Rate r(Ts);
        geometry_msgs::Twist vel_msgs;
        double vx=0,xr=0,yr=0,DisErr=0,AngErr=0;
        double wz=10;

        vel_msgs.linear.x=vx;
        vel_msgs.linear.y=0;
        vel_msgs.linear.z=0;
        vel_msgs.angular.z=wz*D2R;
        vel_msgs.angular.y=0;
        vel_msgs.angular.x=0;


        do{

                AngErr=yawpath-turtlesim_pose.theta;
                vel_msgs.angular.z=AngErr;
                vel_publisher.publish(vel_msgs);
                cout<<"Direct Path Yaw Angle "<<yawpath*R2D<<" Robot Yaw Angle "<<turtlesim_pose.theta*R2D<<" Error"<<" : "<<AngErr*R2D<<"\n";
                ros::spinOnce();
                r.sleep();

                }while((abs(AngErr*R2D)>0.02));

                vel_msgs.linear.x=2;
                vel_msgs.linear.y=0;
                vel_msgs.linear.z=0;
                vel_msgs.angular.z=0*D2R;
                vel_msgs.angular.y=0;
                vel_msgs.angular.x=0;


        do{

                xr=turtlesim_pose.x;
                yr=turtlesim_pose.y;
                DisErr=sqrt(pow((xr-xt),2) + pow((yr-yt),2));

                vel_msgs.linear.x=DisErr;

                vel_publisher.publish(vel_msgs);
                cout<<"Robot Distance from Target Point   :"<<DisErr<<"\n";
                ros::spinOnce();
                r.sleep();

                }while(DisErr>0.01);
                cout<<"ROBOT X & Y positions axis is   :"<<turtlesim_pose.x<<" , "<<turtlesim_pose.y <<" , "<<turtlesim_pose.theta*R2D<<" , "<<"\n";
                cout<<"Reached to desire target number... "<<c+1<<endl;
                vel_msgs.angular.z=0;
                vel_msgs.linear.x=0;
                vel_publisher.publish(vel_msgs);
                }

