#include <franka_gazebo/model_kdl.h>

#include <Eigen/Dense>
#include <string>
#include <ros/ros.h>
#include <chrono>













/*



fk_1(FkFixture, fk_joint1_zero_pose) {
  std::array<double, 7> q = {0, 0, 0, 0, 0, 0, 0};
  std::array<double, 16> pose = model->pose(franka::Frame::kJoint1, q, identity, identity);

  Eigen::Matrix4d expected;
  // clang-format off
  expected <<
      1,    0,    0,       0,
      0,    1,    0,       0,
      0,    0,    1,   0.333,
      0,    0,    0,       1;
  // clang-format on

  Eigen::Affine3d actual(Eigen::Matrix4d(pose.data()));
  print_mat( expected, actual)
}

fk_2(FkFixture, fk_joint2_zero_pose) {
  std::array<double, 7> q = {0, 0, 0, 0, 0, 0, 0};
  std::array<double, 16> pose = model->pose(franka::Frame::kJoint2, q, identity, identity);

  Eigen::Matrix4d expected;
  // clang-format off
  expected <<
      1,    0,    0,       0,
      0,    0,    1,       0,
      0,   -1,    0,   0.333,
      0,    0,    0,       1;
  // clang-format on

  Eigen::Affine3d actual(Eigen::Matrix4d(pose.data()));
}

fk_3(FkFixture, fk_joint3_zero_pose) {
  std::array<double, 7> q = {0, 0, 0, 0, 0, 0, 0};
  std::array<double, 16> pose = model->pose(franka::Frame::kJoint3, q, identity, identity);

  Eigen::Matrix4d expected;
  // clang-format off
  expected <<
      1,    0,    0,       0,
      0,    1,    0,       0,
      0,    0,    1,   0.649,
      0,    0,    0,       1;
  // clang-format on

  Eigen::Affine3d actual(Eigen::Matrix4d(pose.data()));
}

fk_4(FkFixture, fk_joint4_zero_pose) {
  std::array<double, 7> q = {0, 0, 0, 0, 0, 0, 0};
  std::array<double, 16> pose = model->pose(franka::Frame::kJoint4, q, identity, identity);

  Eigen::Matrix4d expected;
  // clang-format off
  expected <<
      1,    0,    0,  0.0825,
      0,    0,   -1,       0,
      0,    1,    0,   0.649,
      0,    0,    0,       1;
  // clang-format on

  Eigen::Affine3d actual(Eigen::Matrix4d(pose.data()));
}

fk_5(FkFixture, fk_joint5_zero_pose) {
  std::array<double, 7> q = {0, 0, 0, 0, 0, 0, 0};
  std::array<double, 16> pose = model->pose(franka::Frame::kJoint5, q, identity, identity);

  Eigen::Matrix4d expected;
  // clang-format off
  expected <<
      1,    0,    0,       0,
      0,    1,    0,       0,
      0,    0,    1,   1.033,
      0,    0,    0,       1;
  // clang-format on

  Eigen::Affine3d actual(Eigen::Matrix4d(pose.data()));
}

fk_6(FkFixture, fk_joint6_zero_pose) {
  std::array<double, 7> q = {0, 0, 0, 0, 0, 0, 0};
  std::array<double, 16> pose = model->pose(franka::Frame::kJoint6, q, identity, identity);

  Eigen::Matrix4d expected;
  // clang-format off
  expected <<
      1,    0,    0,       0,
      0,    0,   -1,       0,
      0,    1,    0,   1.033,
      0,    0,    0,       1;
  // clang-format on

  Eigen::Affine3d actual(Eigen::Matrix4d(pose.data()));
}

fk_7(FkFixture, fk_joint7_zero_pose) {
  std::array<double, 7> q = {0, 0, 0, 0, 0, 0, 0};
  std::array<double, 16> pose = model->pose(franka::Frame::kJoint7, q, identity, identity);

  Eigen::Matrix4d expected;
  // clang-format off
  expected <<
      1,    0,    0,   0.088,
      0,   -1,    0,       0,
      0,    0,   -1,   1.033,
      0,    0,    0,       1;
  // clang-format on

  Eigen::Affine3d actual(Eigen::Matrix4d(pose.data()));
}

fk_flange(FkFixture, fk_flange_zero_pose) {
  std::array<double, 7> q = {0, 0, 0, 0, 0, 0, 0};
  std::array<double, 16> pose = model->pose(franka::Frame::kFlange, q, identity, identity);

  Eigen::Matrix4d expected;
  // clang-format off
  expected <<
      1,    0,    0,   0.088,
      0,   -1,    0,       0,
      0,    0,   -1,   0.926,
      0,    0,    0,       1;
  // clang-format on

  Eigen::Affine3d actual(Eigen::Matrix4d(pose.data()));
}

fk_flange_random(FkFixture, fk_flange_random_pose) {
  std::array<double, 7> q = {0.5157262388785411,  1.2140897359597562,  1.5346381355065786,
                             -3.0398301021734246, -1.2930720893855998, 1.332867311125138,
                             -1.5554459725458225};
  std::array<double, 16> pose = model->pose(franka::Frame::kFlange, q, identity, identity);

  Eigen::Matrix4d expected;
  // clang-format off
    expected <<
        0.281895,  -0.741623,   0.608712,  -0.144822,
       -0.927236,   -0.37359, -0.0257594,   0.114741,
        0.246513,  -0.557158,  -0.792973,    0.17244,
               0,          0,          0,          1;
  // clang-format on

  Eigen::Affine3d actual(Eigen::Matrix4d(pose.data()));
}



void run_tests(){
  fk_1(FkFixture, fk_joint1_zero_pose)
  fk_2(FkFixture, fk_joint2_zero_pose)
  fk_3(FkFixture, fk_joint3_zero_pose)
  fk_4(FkFixture, fk_joint4_zero_pose)
  fk_5(FkFixture, fk_joint5_zero_pose)
  fk_6(FkFixture, fk_joint6_zero_pose)
  fk_7(FkFixture, fk_joint7_zero_pose)
  fk_flange(FkFixture, fk_flange_zero_pose)
  fk_flange_random(FkFixture, fk_flange_random_pose)
}*/















int main(int argc, char** argv) {
  ros::init(argc, argv, "fk_test");
  ros::NodeHandle nh;
  
  std::array<double, 7> q = {0, -0.785398163397, 0, -2.3561944899, 0, 1.57079632679, 0.785398163397};
  std::array<double, 16> identity = {1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1};
  urdf::Model robot;
  robot.initParam("robot_description");
  //model = std::make_unique<franka_gazebo::ModelKDL>(robot, "panda_link0", "panda_link8");
  franka_gazebo::ModelKDL model = franka_gazebo::ModelKDL(robot, "panda_link0", "panda_link8");



  std::chrono::time_point<std::chrono::system_clock> t_start = std::chrono::system_clock::now();
  std::array<double, 16> pose_J4 = model.pose(franka::Frame::kJoint4, q, identity, identity);
  std::array<double, 16> pose_J6 = model.pose(franka::Frame::kJoint6, q, identity, identity);
  std::array<double, 16> pose_EE = model.pose(franka::Frame::kFlange, q, identity, identity);

  std::chrono::time_point<std::chrono::system_clock> t_end = std::chrono::system_clock::now();
  std::chrono::duration<double> t_elaps = t_end - t_start;
  std::cout << "Elapsed time for computation: " << t_elaps.count() << "s" << std::endl;

  
  Eigen::Matrix4d aframe(Eigen::Matrix4d(pose_EE.data()));

  std::cout << "Actual frame:" << std::endl;
  std::cout << aframe << std::endl << std::endl;
  
  
  
  
  
 


}
