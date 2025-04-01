echo Loading bricks...

rosservice call gazebo/delete_model '{model_name: base1}'
rosservice call gazebo/delete_model '{model_name: base2}'
rosservice call gazebo/delete_model '{model_name: brick1}'
rosservice call gazebo/delete_model '{model_name: brick2}'
rosrun gazebo_ros spawn_model -file /home/lozer/franka_emika_ws/src/path_planning/data/models/base/model.urdf -urdf -model base1 -x 0.5 -y 0.1 -z 0.1
rosrun gazebo_ros spawn_model -file /home/lozer/franka_emika_ws/src/path_planning/data/models/base/model.urdf -urdf -model base2 -x 0.5 -y 0.4 -z 0.08
rosrun gazebo_ros spawn_model -file /home/lozer/franka_emika_ws/src/path_planning/data/models/brick/model.urdf -urdf -model brick1 -x 0.45 -y 0.05 -z 0.22
rosrun gazebo_ros spawn_model -file /home/lozer/franka_emika_ws/src/path_planning/data/models/brick/model.urdf -urdf -model brick2 -x 0.58 -y 0.05 -z 0.22