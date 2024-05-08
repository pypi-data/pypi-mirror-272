import numpy as np
import casadi as ca
import spatial_casadi as sc
from grasp_planning.constraints.constraint_template import Constraint

class GraspPosConstraint(Constraint):
    def __init__(self, robot, q_ca, waypoint_ID, n_dofs, tolerance=0.0) -> None:
        super().__init__() 
        # q = q_ca[:n_dof, waypoint_ID] -> joint space of the robot (decision variable)
        # manip_frame = q_ca[n_dof:, waypoint_ID] -> manipulation frame (decision variable)
        # manip frame_pos - T_W_Grasp_pos = 0
        self._robot = robot
        self.g = q_ca[n_dofs:(n_dofs+3), waypoint_ID]
        self.g_eval = ca.Function('g_grasp_pos', [q_ca], [self.g])
        self.tolerance = tolerance
        # self.update_limits(T_W_Grasp)
      
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
        R_W_Grasp_rpy = sc.Rotation.from_matrix(T_W_Grasp[:3,:3]).as_euler("xyz") #convert rotation part of FK into rpy 
        self._T_W_Grasp_rpy = np.vstack((T_W_Grasp[:3,3][:,None], R_W_Grasp_rpy))
        g_lb = (np.zeros((3,1)) + self._T_W_Grasp_rpy[:3]) - self.tolerance
        g_ub = (np.zeros((3,1)) + self._T_W_Grasp_rpy[:3]) + self.tolerance
        self.set_limits(g_lb, g_ub)