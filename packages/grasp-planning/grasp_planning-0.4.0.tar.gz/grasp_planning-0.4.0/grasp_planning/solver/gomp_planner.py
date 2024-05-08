import numpy as np
import casadi as ca
import spatial_casadi as sc
from scipy.spatial.transform import Rotation as R
from grasp_planning.solver.robot_model import RobotKinematicModel
from grasp_planning.cost.costs import SquaredAccCost
from grasp_planning.constraints.constraints import GraspPosConstraint, GraspRotConstraint, ManipulationConstraint

class GOMP():
    def __init__(self, n_waypoints, urdf, theta=np.pi/4, root_link='world', end_link='tool_frame') -> None:
        # Init variables
        self.T_W_Grasp = None
        self.T_W_Obj = None
        self.T_Obj_Grasp = np.eye(4, dtype=float)
        
        # Kinematics
        self._robot_model = RobotKinematicModel(urdf, root_link, end_link)
        self.n_dofs = self._robot_model.n_dofs
        self.manipulation_frame_dim = 6
        self.x_dim = self.n_dofs + self.manipulation_frame_dim
        self.n_waypoints = n_waypoints
        self.theta = theta
        
        # Optimization
        self.x = ca.SX.sym("x", self.x_dim, self.n_waypoints)
        self.x_init = None
        
        self._objective = None
        self.l_joint_limits, self.u_joint_limits = None, None
        self.g_list = []




    def update_grasp_DOF(self, theta: float, degrees=True) -> None:
        """
        Object has to have z-axis aligned with the world frame
        """
        if degrees:
            R_Obj_Grasp = R.from_euler('xyz', [180, 0, theta], degrees=True).as_matrix()
            self.theta = np.deg2rad(theta)
        else:
            R_Obj_Grasp = R.from_euler('xyz', [np.pi, 0, theta], degrees=False).as_matrix()
            self.theta = theta
        self.T_Obj_Grasp[:3,:3] = R_Obj_Grasp
        self.T_W_Grasp = self.T_W_Obj @ self.T_Obj_Grasp

    def update_object_pose(self, T_W_Obj: np.array) -> None:
        """
        Update object and grasp poses
        """
        self.T_W_Obj = T_W_Obj

    def _grasp2rpy(self):
        """
        Convert T_W_Grasp into [x,y,z,r,p,y]
        """
        R_W_Grasp_rpy = sc.Rotation.from_matrix(self.T_W_Grasp[:3,:3]).as_euler("xyz") #convert rotation part of FK into rpy 
        self.T_W_Grasp_rpy = np.vstack((self.T_W_Grasp[:3,3][:,None], R_W_Grasp_rpy))
        return self.T_W_Grasp_rpy


    def set_init_guess(self, q):
        self.x_init = np.tile(q, self.n_waypoints)

    def set_boundary_conditions(self, q_start, q_end=None):
        if self.l_joint_limits is None or self.u_joint_limits is None:
            # Reset joint limits
            self.l_joint_limits = np.full((self.x_dim, self.n_waypoints), -100.0)
            self.u_joint_limits = np.full((self.x_dim, self.n_waypoints), 100.0)

            # get joint limits
            joint_limits = self._robot_model.get_joint_pos_limits()
            for t in range(self.n_waypoints):
                self.l_joint_limits[:self.n_dofs, t] = joint_limits[:,0]
                self.u_joint_limits[:self.n_dofs, t] = joint_limits[:,1]
                self.l_joint_limits[-3:, t] = -2*np.pi
                self.u_joint_limits[-3:, t] = 2*np.pi

        
        # init boundary
        self.l_joint_limits[:,0] = q_start
        self.u_joint_limits[:,0] = q_start

        if q_end != None:
            print("Final boundary condition is not implemented.")
      

    def setup_problem(self):
        # assert self.T_Obj_Grasp != None, "Grasp DOF is not set. Set additional degree of freedom around object."
        # assert self.T_W_Obj != None, "Object pose is not set."
        # 1. create decision variable
        x_ca_flatten = self.x.reshape((-1,1))
        
        # assert self.x_init != None, "Initial guess is missing. Set up one using `set_init_guess(q)`."

        # Define objective function
        cost = SquaredAccCost(self.n_waypoints, self.x_dim, manip_frame=True)
        objective = cost.eval_cost(x_ca_flatten)

        # Define constraints
        g = ca.vertcat()
        for g_term in self.g_list:
            gt = g_term.get_constraint()
            g = ca.vertcat(g, gt)

        options = {}
        options["ipopt.acceptable_tol"] = 1e-3
        self.solver = ca.nlpsol('solver', 'ipopt', {'x': x_ca_flatten, 'f': objective, 'g': g}, options)
  
        
    def solve(self):
        result = self.solver(x0=self.x_init,
                             lbg=self.g_lb,
                             ubg=self.g_ub,
                             lbx=self.l_joint_limits.reshape((-1,1), order='F'),
                             ubx=self.u_joint_limits.reshape((-1,1), order='F'))
        return result['x']

    def _add_grasp_pos_constraint(self, waypoint_ID, tolerance=0.0):
        self.g_list.append(ManipulationConstraint(self._robot_model, self.x, waypoint_ID, self.n_dofs))
        self.g_list.append(GraspPosConstraint(self._robot_model, self.x, waypoint_ID, self.n_dofs, tolerance))

    def _add_grasp_rot_constraint(self, waypoint_ID, tolerance=0.1):
        self.g_list.append(GraspRotConstraint(self._robot_model, self.x, waypoint_ID, self.n_dofs, self.theta, tolerance))


    def add_grasp_constraint(self, waypoint_ID, tolerance=0.0):
        self._add_grasp_pos_constraint(waypoint_ID, tolerance)
        self._add_grasp_rot_constraint(waypoint_ID)

    def add_collision_constraint(self, waypoint_ID):
        pass

    def update_constraints_boundaries(self, T_W_Obj):
        self.update_object_pose(T_W_Obj)
        self.update_grasp_DOF(theta=self.theta, degrees=False)
   
        self.g_lb, self.g_ub = ca.vertcat(), ca.vertcat()

        for g_term in self.g_list:
            g_term.update_limits(self.T_W_Grasp)
            g_lb, g_ub = g_term.get_limits()
            self.g_lb = ca.vertcat(self.g_lb, g_lb)
            self.g_ub = ca.vertcat(self.g_ub, g_ub)
        

