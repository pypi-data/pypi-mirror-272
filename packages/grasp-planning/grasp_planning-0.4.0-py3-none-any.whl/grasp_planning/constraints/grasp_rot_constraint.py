import numpy as np
import casadi as ca
import spatial_casadi as sc
from grasp_planning.constraints.constraint_template import Constraint

class GraspRotConstraint(Constraint):
    def __init__(self, robot, q_ca, waypoint_ID, n_dofs, theta=0.0, tolerance=0.1) -> None:
        super().__init__() 
        # q = q_ca[:n_dof, waypoint_ID] -> joint space of the robot (decision variable)
        # manip_frame = q_ca[n_dof:, waypoint_ID] -> manipulation frame (decision variable)
        # manip frame_pos - T_W_Grasp_pos = 0
        self._robot = robot
        self.theta = theta
        self.tolerance = tolerance

        self.q_ca = q_ca
        fk_ca_T_rpy = self._robot.compute_fk_rpy_ca(q_ca[:n_dofs, waypoint_ID])
        R_W_EEF_rpy = fk_ca_T_rpy[3:]



        # self._g_x_rot = R_W_EEF_rpy[0]
        # self._g_y_rot = R_W_EEF_rpy[1]
        # self._g_z_rot = R_W_EEF_rpy[2]
        fk_ca_T = self._robot.compute_fk_ca(q_ca[:n_dofs, waypoint_ID])

        # R_G_EEF = R_W_G.T @ fk_ca_T[:3,:3]
        R_W_EEF = fk_ca_T[:3,:3]


    
        self.g = sc.Rotation.from_matrix(R_W_EEF).as_euler("xyz")


        # rpy = sc.Rotation.from_matrix(R_G_EEF).as_euler("xyz")
        # self._g_x_rot = rpy[0]
        # self._g_y_rot = rpy[1]
        # self._g_z_rot = rpy[2]
        # g_y_l = -theta
        # g_y_u = theta
        # g_x_l = -0.1
        # g_x_u = 0.1
        # g_z_l = -0.1
        # g_z_u = 0.1
        # # self.update_limits(T_W_Grasp)
        # self.g_lb = ca.vertcat(g_x_l, g_y_l, g_z_l)
        # self.g_ub = ca.vertcat(g_x_u, g_y_u, g_z_u)
        # self.g = ca.vertcat(self._g_x_rot, self._g_y_rot, self._g_z_rot)
        
        self.g_eval = ca.Function('g_grasp_rot', [self.q_ca], [self.g])
    
    def get_constraint(self):
        return self.g

    def do_eval(self, q):
        return self.g_eval(q)

    def set_limits(self, lb, ub):
        self.g_lb = lb
        self.g_ub = ub

    def get_limits(self):
        return self.g_lb, self.g_ub
    
    def update_limits(self, T_W_Grasp):
        # R_W_G_rpy = sc.Rotation.from_matrix(T_W_Grasp[:3,:3]).as_euler("xyz")
        # # x-axis
        # self._g_x_l = R_W_G_rpy[0] - self.tolerance 
        # self._g_x_u = R_W_G_rpy[0] + self.tolerance
        # # y-axis
        # self._g_y_l = R_W_G_rpy[1] - self.theta 
        # self._g_y_u = R_W_G_rpy[1] + self.theta 
        # # z-axis
        # self._g_z_l = R_W_G_rpy[2] - self.tolerance 
        # self._g_z_u = R_W_G_rpy[2] + self.tolerance 

        # g_lb = ca.vertcat(self._g_x_l, self._g_y_l, self._g_z_l)
        # g_ub = ca.vertcat(self._g_x_u, self._g_y_u, self._g_z_u)
        # self.set_limits(g_lb, g_ub)
        
        R_W_G = T_W_Grasp[:3,:3]
        R_lb = sc.Rotation.from_euler("xyz", [-self.tolerance, -self.theta, -self.tolerance], degrees=False).as_matrix()
        R_ub = sc.Rotation.from_euler("xyz", [self.tolerance, self.theta, self.tolerance], degrees=False).as_matrix()

        R_lb = np.linalg.inv(R_W_G.T) @ R_lb
        R_ub = np.linalg.inv(R_W_G.T) @ R_ub

        self.g_lb = sc.Rotation.from_matrix(R_ub).as_euler("xyz")
        self.g_ub = sc.Rotation.from_matrix(R_lb).as_euler("xyz")
