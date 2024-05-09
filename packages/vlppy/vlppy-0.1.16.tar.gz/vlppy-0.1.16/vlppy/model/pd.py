import numpy as np
from numbers import Number
from typing import Union,Sequence
from .led import LED
from .room import Room
from ..error import VLPSequenceLenError,VLPValueRangeError
from scipy.spatial.transform import Rotation 
 
class PD:
    """光电探测器(PD)
    """
    def __init__(self,
                n:Number=1.5,
                fov:Number=60,
                Ar:Number=1e-4,
                Ts:Number=1,
                pos:tuple=(0,0,0),
                Nv:tuple=(0,0,1),
                origin:tuple= (0,0,0),
                *args,
                **kwargs) -> None:
        """ 
        n: 透镜的折射率
        fov: 接收视场角 (单位: 度) [0,90]
        Ar: PD检测器的有效接收面积(单位:平方米)
        Ts: 光学滤波器的增益
        pos: PD参考位置
        Nv: PD接收面的法向量
        origin: 原点位置
        """
        self.n   = n
        self.fov = fov
        self.Ar  = Ar
        self.Ts  = Ts

        self.origin = origin
        self.pos    = pos
        self.Nv     = Nv

    @staticmethod
    def recv_frame_model(l, alpha, beta, center_tp_pos:tuple):
        """接收机模型:PD支架模型(倾斜PD和中心参考点位置关系)
        Params
            l: 倾斜PD到中心水平PD(参考点)的长度(单位:米)
            alpha: PD摆放角(单位:度)
            beta: PD倾斜面倾斜角(单位:度)
            center_tp_pos: 水平中心测试点位置
        Return
            pos: 倾斜PD位置
            Nv: 倾斜PD的法向量
        """
        if len(center_tp_pos) == 3:
            x0, y0, z0 = center_tp_pos
        else:
            x0, y0, z0 = np.split(center_tp_pos, indices_or_sections=3, axis=-1)
        x0, y0, z0 = np.squeeze([x0, y0, z0]) # 除维数为1的维度  
        
        # 角度制转弧度制
        alpha_rad, beta_rad = np.radians([alpha, beta])

        # 倾斜PD和中心参考点位置关系
        xr = x0 + l * np.cos(alpha_rad) * np.cos(beta_rad) 
        yr = y0 + l * np.sin(alpha_rad) * np.cos(beta_rad)
        zr = z0 + l * np.sin(beta_rad)
        
        # alpha_rad+np.pi: PD的方位角和PD倾斜面的摆放角反向
        # beta_rad: PD的法向量与z轴的夹角和PD倾斜面的倾斜角相等
        Nx = np.cos(alpha_rad+np.pi) * np.sin(beta_rad)
        Ny = np.sin(alpha_rad+np.pi) * np.sin(beta_rad)
        Nz = np.cos(beta_rad)

        if len(center_tp_pos) == 3:
            pos = np.asarray([xr,yr,zr])
            Nv = np.asarray([Nx,Ny,Nz]) 
        else:
            pos = np.stack([xr,yr,zr], axis=-1) # 在最后一维度上堆叠
            Nv = np.stack([Nx,Ny,Nz], axis=-1)
        
        return pos, Nv

    @staticmethod
    def recv_surface_model(r:Union[Number,tuple], alpha, beta, center_tp_pos:tuple):
        """接收机模型:安全帽椭球面(倾斜PD和中心参考点位置关系)
        Params
            r: 曲球面半径(单位:米)
            alpha: PD摆放角(单位:度)
            beta: 椭球球心与PD连线与z轴夹角(单位:度)
            center_tp_pos: 椭球面顶部中心测试点位置
        Return
            pos: 倾斜PD位置
            Nv: 倾斜PD的法向量
        """
        r = np.asarray(r)
        assert r.size in (1,3)
        a, b, c = np.full(shape=(3), fill_value=r) if r.size == 1 else r

        # 角度制转弧度制
        alpha_rad, beta_rad = np.radians([alpha, beta]) 

        if not 0 <= beta_rad <= 90: # 限定
            raise VLPValueRangeError(beta, 0, 90)
        
        if len(center_tp_pos) == 3:
            x0, y0, z0 = center_tp_pos
        else:
            x0, y0, z0 = np.split(center_tp_pos, indices_or_sections=3, axis=-1)
        x0, y0, z0 = np.squeeze([x0, y0, z0]) # 除维数为1的维度  
        
        # 倾斜PD位置
        xr = x0 + a * np.cos(alpha_rad) * np.sin(beta_rad)
        yr = y0 + b * np.sin(alpha_rad) * np.sin(beta_rad)
        zr = z0 - c * (1 - np.cos(beta_rad))

        # alpha_rad: PD的方位角和PD倾斜面的摆放角相等
        # beta_rad: 椭球球心与PD连线与z轴夹角
        Nx = 1/a * np.cos(alpha_rad) * np.sin(beta_rad)
        Ny = 1/b * np.sin(alpha_rad) * np.sin(beta_rad)
        Nz = 1/c * np.cos(beta_rad)

        # PD位置与法向量
        if len(center_tp_pos) == 3:
            pos = np.asarray([xr,yr,zr])
            Nv = np.asarray([Nx,Ny,Nz]) 
        else:
            pos = np.stack([xr,yr,zr], axis=-1)
            Nv = np.stack([Nx,Ny,Nz], axis=-1)

        return pos, Nv

    @staticmethod
    def recv_hemisphere_model(r, l, alpha, center_tp_pos:tuple):
        """接收机模型:半球面模型(倾斜PD和中心参考点位置关系)
        Params
            r: 曲球面半径(单位:米)
            l: 倾斜PD到顶部中心(参考点)的弧长(单位:米)   
            alpha:倾斜PD方位角(单位:度) 
            center_tp_pos: 测试点位置 
        Return
            pos: 倾斜PD位置
            Nv: 倾斜PD的法向量
        """
        # 倾斜PD的方位角和倾斜角
        beta_rad = l/r              # 椭球球心与PD连线与z轴夹角(PD倾斜角)
        beta = np.degrees(beta_rad) # 弧度制转角度制
        pos, Nv = PD.recv_surface_model(r, alpha, beta, center_tp_pos)

        return pos, Nv

    def recv_led_radiation_intensity(self, led:LED):
        """计算LED辐射强度(LOS链路)
        Params
            led: LED实例化
        Return 
            LOS链路LED辐射强度
        """
        Vt_r = self.pos - led.pos                                           # LED到接收点的方向向量 (l*w*h,3)                                      # LED到PD的方向向量 (l*w*h,3)
        d = np.linalg.norm(Vt_r, axis=-1)                                   # LED到接收点的方向向量的模 (l*w*h)
        cos_led_t_angle_rad_rad = np.sum(Vt_r*led.Nv, axis=-1) / d          # LED发射角的余弦值 (l*w*h)
        led_t_angle_rad = np.arccos(cos_led_t_angle_rad)                    # LED发射角 (l1*w1)   
        led_t_angle = np.degrees(led_t_angle_rad)                           # 弧度制转为角度制 (l1*w1)

        cos_led_t_angle_rad = np.abs(cos_led_t_angle_rad)                   # 在LED辐射角内,解决辐射角大于90°,角余弦值为负值情况
        cos_led_t_angle_rad = np.where((led_t_angle>=0) & (led_t_angle<=led.fov), cos_led_t_angle_rad, 0) # 满足LED灯照射条件

        R0 = ((led.m + 1)  / (2 * np.pi)) * cos_led_t_angle_rad_rad**led.m  # 辐射强度模型 (l*w*h)

        """ y(t) = x(t) * h(t)
        H0 = H0.flatten() #打平 (l,w) -> (l*w)
        return np.array([np.convolve(h,led.send_signal) for h in H0])  #卷积 (l*w,npt)
              <=> np.array([h * led.send_signal for h in H0])          #相乘 (l*w,npt) 
        """
        # 以下是为了兼容交直流信号
        R0 = np.expand_dims(R0, -1)              # 在最后一维扩充一个维度 (l*w*h) -> (l*w*h,1)  <=> H0.reshape(l*w*h,1) <=> H0[...,np.newaxis]
        radiation_intensity = R0 * led.signal    # LED辐射强度[广播机制 (l*w*h,1) * (npt) -> (l*w*h,npt) * (l*w*h,npt) = (l*w*h,npt)]

        return np.squeeze(radiation_intensity)   # (l*w*h,npt).如果npt==1,则返回形状为(l*w*h)

    def recv_los_led_signal(self, led:LED, fov_condition=True, *args, **kwargs):
        """计算PD接收LED信号(LOS链路):
        Params
            led: LED实例化
            fov_condition: 是否添加视场条件(考虑旋转需设为False)
        Return 
            LOS链路中PD探测器接收LED信号
        """
        #⭐ LED -> PD
        # LED发射端
        Vt_r = self.pos - led.pos                                   # LED到PD的方向向量 (l*w*h,3)
        d = np.linalg.norm(Vt_r, axis=-1)                           # 求模:LED到PD的方向向量的模 (l*w*h)
        cos_led_t_angle_rad = np.sum(Vt_r*led.Nv, axis=-1) / d      # LED发射角的余弦值 (l*w*h)
        led_t_angle_rad = np.arccos(cos_led_t_angle_rad)            # LED发射角 (l1*w1)   
        led_t_angle = np.degrees(led_t_angle_rad)                   # 弧度制转为角度制 (l1*w1)

        cos_led_t_angle_rad = np.abs(cos_led_t_angle_rad)           # 在LED辐射角内,解决辐射角大于90°,角余弦值为负值情况
        cos_led_t_angle_rad = np.where((led_t_angle>=0) & (led_t_angle<=led.fov), cos_led_t_angle_rad, 0) # 满足LED灯照射条件

        # PD接收端
        Vr_t = -Vt_r # PD到LED的方向向量 (l*w*h,3)
        cos_pd_r_angle_rad = np.sum(Vr_t*self.Nv, axis=-1) / d      # PD接收角的余弦值 (l*w*h) 
        pd_r_angle_rad = np.arccos(cos_pd_r_angle_rad)              # PD接收器入射角的大小(弧度制) (l*w*h)
        pd_r_angle = np.degrees(pd_r_angle_rad)                     # 弧度制转为角度制 (l*w*h)

        cos_pd_r_angle_rad = np.abs(cos_pd_r_angle_rad)             # 解决PD入射角大于90°,入射角余弦值为负值情况
        if fov_condition:
            cos_pd_r_angle_rad = np.where((pd_r_angle>=0) & (pd_r_angle<=self.fov), cos_pd_r_angle_rad, 0)  # 满足PD入射条件

        # 计算信道增益
        H0 = (((led.m + 1) * self.Ar) / (2 * np.pi * d**2)) * cos_led_t_angle_rad**led.m * cos_pd_r_angle_rad * self.Ts * self.G_Con # (l*w*h)

        """ y(t) = x(t) * h(t)
        H0 = H0.flatten() # 打平 (l,w) -> (l*w,)
        return np.array([np.convolve(h,led.send_signal) for h in H0])  # 卷积 (l*w,npt)
              <=> np.array([h * led.send_signal for h in H0])          # 相乘 (l*w,npt) 
        """
        # 以下是为了兼容交直流信号
        H0 = np.expand_dims(H0, axis=-1)  # 在最后一维扩充一个维度 (l*w*h) -> (l*w*h,1)  <=> H0.reshape(l*w*h,1) <=> H0[...,np.newaxis]
        recv_signal = H0 * led.signal     # PD接收信号 [广播机制 (l*w*h,1) * (npt) -> (l*w*h,npt) * (l*w*h,npt) = (l*w*h,npt)]

        return np.squeeze(recv_signal)    # (l,w,h,npt).如果npt==1,则返回形状为(l,w,h)
      
    def recv_nlos_led_signal(self, led:LED, room:Room, fov_condition=True, *args, **kwargs):
        """计算PD接收LED一次反射信号(NLOS链路):
        Params
            led: LED实例化
            room: Room实例化
            fov_condition: 是否添加视场条件(考虑旋转需设为False)
        Return 
            NLOS链路中PD探测器接收LED一次反射信号
        """
        # 对PD坐标张量扩充维度,以便使用广播
        pd_pos = np.expand_dims(self.pos, axis=-2)  # (l*w*h,3) -> (l*w*h,1,3) 
        pd_Nv = np.expand_dims(self.Nv, axis=-2)   # PD法向量 (n,3) -> (n,1,3) or  (3) -> (1,3)

        H0 = 0  #反射(LOS)链路信道增益
        # 遍历每一面反射墙壁参数:(l1*w1,3),(l1*w1,2)
        for i, (w_pos, angle) in enumerate(room.get_reflect_wall_args()):
            w_alpha, w_beta = np.split(angle, indices_or_sections=2, axis=-1)   # (l1*w1,2) -> (l1*w1,1) + (l1*w1,1)
            w_alpha, w_beta = np.squeeze([w_alpha, w_beta])                     # (l1*w1,1) -> (l1*w1)

            # 墙壁反射面元法向量与x轴和z轴的夹角,角度制转弧度制
            w_alpha_rad, w_beta_rad = np.radians([w_alpha, w_beta]) # (l1*w1)
            
            # 墙壁反射面元法向量
            Nx = np.cos(w_alpha_rad) * np.sin(w_beta_rad)
            Ny = np.sin(w_alpha_rad) * np.sin(w_beta_rad)
            Nz = np.cos(w_beta_rad)

            Nw = np.stack([Nx,Ny,Nz], axis=-1)             # 墙壁反射面元法向量 (l1*w1,3)
            Nw_norm = np.linalg.norm(Nw, axis=-1)          # 墙壁反射面元法向量模 (l1*w1)
            if Nw.ndim > 1:
                Nw_norm = np.expand_dims(Nw_norm, axis=-1) # (l1*w1,1)
            Nw = Nw/Nw_norm                                # 墙壁反射面元单位法向量 (l1*w1,3)

            #⭐ LED -> 墙壁反射面元
            # LED发射端
            Vt_w = w_pos - led.pos              # LED灯到墙壁反射面元的方向向量 (l1*w1,3)
            d1 = np.linalg.norm(Vt_w, axis=-1)  # 求模:LED灯到墙壁反射面元的距离 (l1*w1)
            mark1 = np.all(Vt_w==0, axis=-1)    # 异常点处理:判断墙壁反射面元和LED是否重合(方向向量是否为零向量) (l1*w1)
            d1 = np.where(mark1, 1, d1)         # 异常点处理:为使cos_led_t_angle_rad分母不为0,让墙壁反射面元和LED重合时的距离不为0 (l1*w1)
            
            cos_led_t_angle_rad = np.sum(Vt_w*led.Nv, axis=-1) / d1    # LED发射角的余弦值 (l1*w1)  
            led_t_angle_rad = np.arccos(cos_led_t_angle_rad)           # LED发射角 (l1*w1)   
            led_t_angle = np.degrees(led_t_angle_rad)                  # 弧度制转为角度制 (l1*w1)  

            cos_led_t_angle_rad = np.abs(cos_led_t_angle_rad)          # 解决LED发射角大于90°,发射角余弦值为负值情况
            cos_led_t_angle_rad = np.where((led_t_angle>=0) & (led_t_angle<=led.fov), cos_led_t_angle_rad, 0) # 满足LED灯照射条件

            # 墙壁反射面元接收端
            Vw_t = -Vt_w     # 墙壁反射面元到LED灯的方向向量 (l1,w1,3)
            cos_wall_r_angle_rad = np.sum(Vw_t*Nw, axis=-1) / d1                             # 墙壁反射面元入射角 (l1*w1)
            cos_wall_r_angle_rad = np.where(cos_wall_r_angle_rad>0, cos_wall_r_angle_rad, 0) # 满足墙壁反射条件 (入射角小于90)

            #⭐墙壁反射面元 -> PD
            # 墙壁反射面元发射端
            Vw_r = pd_pos - w_pos              # 墙壁反射面元到PD的方向向量  (l*w*h,1,3)-(l1*w1,3) -> (l*w*h,l1*w1,3)
            d2 = np.linalg.norm(Vw_r, axis=-1) # 求模:墙壁反射面元到PD之间的距离 (l*w*h,l1*w1)
            mark2 = np.all(Vw_r==0, axis=-1)   # 异常点处理:判断墙壁反射面元和参考点是否重合(方向向量是否为零向量) (l*w*h,l1*w1)
            d2 = np.where(mark2, 1, d2)        # 异常点处理:为使cos_wall_t_angle_rad分母不为0,让墙壁反射面元和参考点重合时的距离不为0

            cos_wall_t_angle_rad = np.sum(Vw_r*Nw, axis=-1) / d2                             # 墙壁反射面元发射角 (l*w*h,l1*w1)
            cos_wall_t_angle_rad = np.where(cos_wall_t_angle_rad>0, cos_wall_t_angle_rad, 0) # 满足墙壁反射条件 (发射角小于90)
    
            # PD接收端
            Vr_w = -Vw_r                                             # PD到墙壁反射面元的方向向量 (l*w*h,l1*w1,3)
            cos_pd_r_angle_rad = np.sum(Vr_w*pd_Nv, axis=-1) / d2    # PD接收角的余弦值 (l*w*h,l1*w1)
            pd_r_angle_rad = np.arccos(cos_pd_r_angle_rad)           # PD接收器入射角(弧度制) (l*w*h,l1*w1)
            pd_r_angle = np.degrees(pd_r_angle_rad)                  # 弧度制转为角度制 (l*w*h,l1*w1)
            
            cos_pd_r_angle_rad = np.abs(cos_pd_r_angle_rad)          # 解决PD入射角大于90°,入射角余弦值为负值情况
            if fov_condition:
                cos_pd_r_angle_rad = np.where((pd_r_angle>=0) & (pd_r_angle<=self.fov), cos_pd_r_angle_rad, 0)  # 满足PD入射条件

            rho = room.rho[i]   # 墙壁反射率
            Aw  = room.Aw[i]    # 墙壁反射面元面积

            # 反射(NLOS)子链路信道增益  
            Hw = (((led.m + 1) * self.Ar) / (2 * np.pi * d1**2 * d2**2)) * rho * Aw * cos_led_t_angle_rad**led.m * cos_wall_r_angle_rad * cos_wall_t_angle_rad *  cos_pd_r_angle_rad * self.Ts * self.G_Con  # (l*w*h,l1*w1)
            Hw = np.sum(Hw, axis=-1)   # 反射(NLOS)链路信道增益求和 (l*w*h,l1*w1) -> (l*w*h)

            # 对所有反射墙壁(NLOS)链路信道增益求和  
            H0 += Hw                   # (l*w*h)

        # 墙壁一次反射(NLOS)链路信道增益
        H0 = np.expand_dims(H0,-1)     # 在最后一维扩充一个维度 (l*w*h) -> (l*w*h,1)  <=> H0.reshape(l*w*h,1) <=> H0[...,np.newaxis]
        recv_signal = H0 * led.signal  # PD接收信号[广播机制 (l*w*h,1) * (npt) -> (l*w*h,npt) * (l*w*h,npt) = (l*w*h,npt)]
        return np.squeeze(recv_signal) # 去除维度为1的维数

    def recv_led_signal(self, led:LED, room:Room,  *args, **kwargs):
        """计算PD接收LED信号(LOS+NLOS链路):
        Params
            led: LED实例化
            room: Room实例化
        Return 
            LOS+NLOS链路中PD探测器接收LED信号
        """
        recv_los_signal  = self.recv_los_led_signal (led=led)            # PD接收直射链路信号
        recv_nlos_signal = self.recv_nlos_led_signal(led=led, room=room) # PD接收一次反射链路信号
        return recv_los_signal + recv_nlos_signal

    def shot_noise(self, P, R=0.62, Ibg=2e-9, I2=0.562, B=100e6, *argv, **kwargv):
        """获取PD散粒噪声功率
        Params
            P: PD接收功率(W)
            R: PD响应度(A/W)
            Ibg: 暗电流(A)
            I2: 噪声带宽系数
            B: 噪声带宽(Hz)
        Return 
            PD散粒噪声功率
        """
        q = 1.6e-19  # 电子电荷量(C)
        return 2*q*R*P*B + 2*q*Ibg*I2*B
    
    def thermal_noise(self, Tk=300, G=10, eta=112, B=100e6, I2=0.562, I3=0.0868, gamma=1.5, gm=30, *argv, **kwargv):
        """获取PD热噪声功率
        Params
            Tk: 热力学温度:Tk = T + 273.15°C(K)
            G: 开环电压增益
            eta: PD每单位面积上固定电容(pF/cm2)
            B: 噪声带宽(Hz)
            I2: 噪声带宽系数 
            I3: 噪声带宽系数 
            gamma: 信道噪声系数
            gm: 跨导(mS)
        Return
            PD热噪声功率
        """
        k = 1.38e-23  # 玻尔兹曼常数
        eta *= 1e-8   # 单位换算(1pF/cm2 = 1e-8F/m2)
        gm *= 1e-3    # 单位换算(1mS = 1e-3S)

        return 8*np.pi*k*Tk/G*eta*self.Ar*I2*B**2 + \
            16*np.pi**2*k*Tk*gamma/gm*eta**2*self.Ar**2*I3*B**3

    def recv_noise_signal(self, P, *argv, **kwargv):
        """接收噪声信号功率
        """
        return self.shot_noise(P=P, *argv, **kwargv) + self.thermal_noise(*argv, **kwargv)


    def SNR(self, P, R, dB=True, *argv, **kwargv):
        """信噪比
        Params
            P: PD接收LOS+NLOS链路的光功率
            R: PD的响应度
            dB: 信噪比dB表示
        Return
            信噪比
        """
        P_noise = self.shot_noise(P=P, R=R, *argv, **kwargv) + self.thermal_noise(*argv, **kwargv)
        snr = (R*P)**2 / P_noise
        return 10*np.log10(snr) if dB else snr

    @property
    def origin(self) -> tuple:
        """设置原点位置
        """
        return self._origin

    @origin.setter
    def origin(self, o):
        """获取原点位置
        """
        if not len(o) == 3:
            raise VLPSequenceLenError(o,3)
        
        self._origin = tuple(o) 

    @property
    def pos(self):
        """获取PD的相对位置 (偏移位置)
        """
        return self._pos + self.origin
    
    @pos.setter
    def pos(self, pos:tuple):
        """设置PD的参考位置
        """
        pos = np.asarray(pos)
        assert len(pos) == 3 or pos.shape[-1] == 3

        if len(pos) == 3:
            xr,yr,zr = pos
            pos = np.stack([xr,yr,zr], axis=-1)

        self._pos = pos # (L*w*h,3)

    @property
    def Nv(self):  
        """获取PD单位法向量  
        """  
        norm = np.linalg.norm(self._Nv, axis=-1) # 求模 (n)
        if self._Nv.ndim > 1:
            norm = np.expand_dims(norm, axis=-1) # (n,1)

        return self._Nv / norm # 单位化 (n,3)
    
    @Nv.setter
    def Nv(self, n):
        """设置PD法向量  
        """  
        N = np.asarray(n)
        assert len(n) == 3 or n.shape[-1] == 3

        if len(n) == 3:
            Nx,Ny,Nz = N
            N = np.stack([Nx,Ny,Nz], axis=-1)

        self._Nv = N # (n,3)

    @property
    def fov(self):
        """获取接收视场角 (单位: 度)
        """    
        return self._fov

    @fov.setter
    def fov(self, fov): 
        """设置接收视场角 (单位: 度)
        """
        # if not 0 <= fov <= 90:
        #     raise VLPValueRangeError(fov,0,90)
        self._fov = fov

    @property
    def Ar(self):   
        """获取PD检测器的接收面积(单位:平方米)
        """ 
        return self._Ar

    @Ar.setter
    def Ar(self, a): 
        """设置PD检测器的接收面积(单位:平方米)
        """
        self._Ar = a

    @property
    def Ts(self):   
        """获取光学滤波器的增益 
        """ 
        return self._Ts

    @Ts.setter
    def Ts(self, ts): 
        """设置光学滤波器的增益 
        """
        self._Ts = ts

    @property
    def n(self): 
        """获取透镜的折射率
        """   
        return self._n

    @n.setter
    def n(self, n): 
        """设置透镜的折射率
        """
        self._n = n

    @property
    def G_Con(self):
        """获取聚光器增益
        """
        # 角度制转弧度制
        fov_rad = np.radians(self.fov)

        return self.n**2 / np.sin(fov_rad)**2  
    
    @staticmethod
    def expand_dims_to_broacast(arr,shape=None,repeat:int=None,axis:int=0):
        """ arr 维度扩充并广播到指定形状 shape
        Params:
            arr: 要扩维的array
            shape: 添加n个维度需要广播到对应的形状
            repeat: 重复添加n个维度(并广播到对应的形状)
            axis: 指定轴
        """
        assert repeat or np.all(shape)
        if isinstance(shape, Number): shape = [shape]
        if axis >= 0: shape = np.flip(shape)
        if not repeat: repeat = 1
        
        for _ in range(repeat):
            for i in range(np.size(shape)):
                arr = np.expand_dims(arr, axis=axis) # 扩维
                if np.all(shape):
                    arr = np.repeat(arr, shape[i], axis=axis) # 在axis轴上复制操作【广播】
        return arr
    
    @staticmethod
    def tp_raw_args(center_tp_pos:tuple, angles:Sequence):
        """获取PD特征【位置、角度】
        等效 x, y, z, alpha, beta, gamma = np.meshgrid(x, y, z, alpha, beta, gamma)
        """
        pos = np.asarray(center_tp_pos)
        angles = np.asarray(angles)

        assert len(pos) == 3 or pos.shape[-1] == 3
        assert len(angles) == 3 or angles.shape[-1] == 3

        if pos.ndim == 1:         # (3) -> (1,3)
            pos = np.expand_dims(pos, axis=0)
        else:
            if len(pos) == 3:     # (3,n) -> (n,3)
                pos = np.stack(pos, axis=-1)

        if angles.ndim == 1:      # (3) -> (1,3)
            angles = np.expand_dims(angles, axis=0)
        else:
            if len(angles) == 3:  # (3,n) -> (n,3)
                angles = np.stack(angles, axis=-1)
        pos_shape, angles_shape = pos.shape[0], angles.shape[0]         # (l*w*h), (a*b*g)

        if angles.ndim > 1: # 动态时PD将会存在角度偏转
            # 扩维后广播
            pos = PD.expand_dims_to_broacast(pos, shape=angles_shape, axis=-2)    # (l*w*h, a*b*g, 3) 
            pos = np.reshape(pos,newshape=(-1,3))                                 # (l*w*h*a*b*g,3) = (n,3)

        if pos.ndim > 1: 
            # 扩维后广播 
            angles = PD.expand_dims_to_broacast(angles, shape=pos_shape, axis=0)  # (l*w*h,a*b*g,3) 
            angles = np.reshape(angles,newshape=(-1,3))                 # (l*w*h*a*b*g,3) = (n,3)

        # 分离轴
        xr, yr, zr = np.split(pos, indices_or_sections=3, axis=-1)            # (n,1)*3
        alpha, beta, gamma = np.split(angles, indices_or_sections=3, axis=-1) # (n,1)*3

        # 去除维数为1的维度
        xr, yr, zr = np.squeeze([xr, yr, zr])                                 # (n)*3 
        alpha, beta, gamma = alpha.flatten(), beta.flatten(), gamma.flatten() # (n)*3

        return np.array([xr,yr,zr]), np.array([alpha,beta,gamma])
    
    @staticmethod
    def rotation_pd_recv_los_led_signal(P, led:LED, tp_pos, pd_pos, pd_Nv, fov=90, angles=(0,0,0), seq="zxy", *args, **kwargs):
        """LOS链路,获取旋转后的PD接收功率
           旋转前后功率的比值: 
                R_P/P = (d/R_d)**(m+3) * (R_Vtr @ R_Nt/ Vtr @ Nt)**m * (R_Vrt @ R_Nr/ Vrt @ Nr)
        Params
            P: 未旋转时PD接收功率(正常定位时的接收功率)
            led: LED实例化
            tp_pos: 待测点位置
            pd_pos: PD位置
            fov: PD视场角
            angles: 旋转角度 (单位:度)
            seq: 旋转顺序
        Return
            旋转后的PD接收功率
        """
        if not len(P) == len(tp_pos) == len(pd_pos):
            raise Exception("These arrays have different shapes.")

        # PD法向量单位化
        pd_Nv_norm = np.linalg.norm(pd_Nv, axis=-1)            # PD法向量模 (l1*w1)
        if pd_Nv.ndim > 1:
            pd_Nv_norm = np.expand_dims(pd_Nv_norm, axis=-1)   # (l1*w1,1)
        pd_Nv = pd_Nv/pd_Nv_norm                               # PD的单位法向量 (l1*w1,3)

        # 旋转角度
        assert len(angles) == 3 or angles.shape[-1] == 3
        if len(angles) == 3:
            alpha, beta, gamma = angles
            angles = np.stack([alpha, beta, gamma], axis=-1) # 旋转了m次 (m,3)   

        Rmat = Rotation.from_euler(
            seq, angles, degrees=True).as_matrix()           # 旋转矩阵 (m,3,3) 
        
        o_pd_pos = pd_pos - tp_pos                           # PD的相对于旋转中心O的位置 (n,3)
        R_pd_pos, R_Nv = [], []                              # 旋转后PD的位置和法向量
        for Vo_pd, o_pos in zip(o_pd_pos, tp_pos):
            R_pd_pos.append(Rmat @ Vo_pd + o_pos)            # n个待测点,每点旋转m次,旋转后PD位置 (m,3,3) @ n*(3) =(n,m,3)
        R_Nv = Rmat @ pd_Nv                                  # 旋转后PD的法向量 (n,m,3) or (m,3)

        #⭐未旋转前
        ## LED 发射端
        Vtr = pd_pos - led.pos                               # LED到PD方向向量 (n,3)
        Vtr_dot = np.sum(Vtr * led.Nv, axis=-1)              # 向量内积 (n)

        ## PD 接收端             
        Vrt = -Vtr                                           # PD到LED方向向量 (n,3)
        d = np.linalg.norm(Vrt, axis=-1)                     # PD到LED的距离 (n)
        Vrt_dot = np.sum(Vrt * pd_Nv, axis=-1)               # 向量内积 (n)

        #⭐旋转后
        ## LED 发射端
        R_Vtr = R_pd_pos - led.pos                           # 旋转后,LED到PD的方向向量 (n,m,3)
        R_Vtr_dot = np.sum(R_Vtr * led.Nv, axis=-1)          # 旋转后,向量内积 (n,m)

        ## PD 接收端
        R_Vrt = -R_Vtr                                       # 旋转后,PD到LED的方向向量 (n,m,3) 
        R_d = np.linalg.norm(R_Vrt, axis=-1)                 # 旋转后,PD到LED的距离 (n,m)
        R_Vrt_dot = np.sum(R_Vrt * R_Nv, axis=-1)            # 旋转后,向量内积 (n,m)

        # 预处理,便于矩阵运算
        d = np.expand_dims(d, axis=-1)                       # (n) -> (n,1)
        Vrt_dot = np.expand_dims(Vrt_dot, axis=-1)           # (n) -> (n,1)
        Vtr_dot = np.expand_dims(Vtr_dot, axis=-1)           # (n) -> (n,1)
        P = np.expand_dims(P, axis=-1)                       # (n) -> (n,1)

        # 代入计算
        R_P = P * (d/R_d)**(led.m+3) * np.abs(R_Vtr_dot/Vtr_dot)**led.m * np.abs(R_Vrt_dot/Vrt_dot) # (n,m)

        # 满足视场角内接收
        cos_pd_r_angle_rad = R_Vrt_dot/R_d                   # PD接收入射角余弦值
        pd_r_angle_rad = np.arccos(cos_pd_r_angle_rad)       # PD接收器入射角(弧度制) (n,l1*w1)
        pd_r_angle = np.degrees(pd_r_angle_rad)              # 弧度制转为角度制 (n,l1*w1)
        R_P = np.where((pd_r_angle>=0) & (pd_r_angle<=fov), R_P, 0) # 视场角内接收功率
        R_P = np.reshape(R_P,-1)                             # (n,m) -> (n*m)
        
        return R_P
    
    @staticmethod
    def rotation_pd_recv_nlos_led_signal( P, room:Room, tp_pos, pd_pos, pd_Nv, fov=90, angles=(0,0,0), seq="zxy", *args, **kwargs):
        """NLOS链路,获取旋转后的PD接收功率
           旋转前后功率的比值: 
                R_P/P = Σ( (d2/d2_r)**4 * (R_Vwr@R_Nw/Vwr@Nw) * (R_Vrw@R_Nr/Vrw@Nr) )
        Params 
            P: 未旋转时PD接收功率(正常定位时的接收功率)
            room: Room实例化
            tp_pos: 待测点位置
            pd_pos: PD位置
            fov: PD视场角
            angles: 旋转角度 (单位:度)
            seq: 旋转顺序
        Return 
            旋转后的PD接收功率 
        """
        raise Exception("This function is not implemented, please pay attention to the subsequent version.")
        # if not len(P) == len(tp_pos) == len(pd_pos) :          # (n)
        #     raise Exception("These two arrays have different shapes.")

        # # PD法向量单位化
        # pd_Nv_norm = np.linalg.norm(pd_Nv, axis=-1)            # PD法向量模 (n)
        # if pd_Nv.ndim > 1:
        #     pd_Nv_norm = np.expand_dims(pd_Nv_norm, axis=-1)   
        # pd_Nv = pd_Nv/pd_Nv_norm                               # PD的单位法向量 (n,3) or (3)
        # pd_Nv = np.broadcast_to(pd_Nv, np.shape(pd_pos))       # (n,3)

        # # 旋转角度
        # assert len(angles) == 3 or angles.shape[-1] == 3 
        # if len(angles) == 3:
        #     alpha, beta, gamma = angles
        #     angles = np.stack([alpha, beta, gamma], axis=-1)   # (m,3)   

        # Rmat = Rotation.from_euler(
        #     seq, angles, degrees=True).as_matrix()             # 旋转矩阵 (m,3,3) 
        
        # o_pd_pos = pd_pos - tp_pos                             # PD相对于旋转中心O的位置 (n,3)

        # R_pd_pos, R_Nv = [], []                                # 旋转后PD的位置和法向量
        # for Vo_pd, o_pos, Nv in zip(o_pd_pos, tp_pos, pd_Nv):
        #     R_pd_pos.append(Rmat @ Vo_pd + o_pos)              # n个待测点,每点旋转m次,旋转后PD位置 (m,3,3) @ n*(3) =(n,m,3)
        #     R_Nv.append(Rmat @ Nv)                             # (m,3,3) @ n*(3) =(n,m,3)
        # R_pd_pos, R_Nv = np.asarray(R_pd_pos), np.asarray(R_Nv)   

        # # 对PD坐标张量扩充维度,以便使用广播
        # pd_pos = np.expand_dims(np.expand_dims(pd_pos, axis=-2), axis=-2)   # (n,3) -> (n,1,1,3) 
        # tp_pos = np.expand_dims(np.expand_dims(tp_pos, axis=-2), axis=-2)   # (n,3) -> (n,1,1,3) 
        # pd_Nv  = np.expand_dims(np.expand_dims(pd_Nv, axis=-2), axis=-2)    # (n,3) -> (n,1,1,3) 
        # R_pd_pos = np.expand_dims(R_pd_pos, axis=-2)                        # (n,m,3) -> (n,m,1,3) 
        # R_Nv = np.expand_dims(R_Nv, axis=-2)                                # (n,m,3) -> (n,m,1,3) 
        # P = np.expand_dims(P,-1)                                            # (n,1) -> (n,1)

        # G = 0 # NLOS旋转前后信道增益比例系数 
        
        # # 遍历每一面反射墙壁参数:(l1*w1,3), (l1*w1,2)
        # for w_pos, angle in room.get_reflect_wall_args():
        #     w_alpha, w_beta = np.split(angle, indices_or_sections=2, axis=-1)   # (l1*w1,2) -> (l1*w1,1) + (l1*w1,1)
        #     w_alpha, w_beta = np.squeeze([w_alpha, w_beta])                     # (l1*w1,1) -> (l1*w1) 

        #     # 墙壁反射面元法向量与x轴和z轴的夹角,角度制转弧度制
        #     w_alpha_rad, w_beta_rad = np.radians([w_alpha, w_beta])             # (l1*w1)
            
        #     # 墙壁反射面元法向量
        #     Nx = np.cos(w_alpha_rad) * np.sin(w_beta_rad)
        #     Ny = np.sin(w_alpha_rad) * np.sin(w_beta_rad)
        #     Nz = np.cos(w_beta_rad)

        #     Nw = np.stack([Nx,Ny,Nz], axis=-1)               # 墙壁反射面元法向量 (l1*w1,3)
        #     Nw_norm = np.linalg.norm(Nw, axis=-1)            # 墙壁反射点法向量模 (l1*w1)
        #     if Nw.ndim > 1:
        #         Nw_norm = np.expand_dims(Nw_norm, axis=-1)   # (l1*w1,1)
        #     Nw = Nw/Nw_norm                                  # 墙壁反射点的单位法向量 (l1*w1,3)

        #     #⭐未旋转前
        #     ## 墙壁面元发射端
        #     Vwr = pd_pos - w_pos                             # 墙壁面元d到PD的方向向量 (n,1,1,3) - (l1*w1,3) -> (n,1,l1*w1,3)
        #     d = np.linalg.norm(Vwr, axis=-1)                 # PD到墙壁面元的距离 (n,1,l1*w1)
        #     Vwr_dot = np.sum(Vwr * Nw, axis=-1)              # 向量内积 (n,1,l1*w1)
        #     Vwr_dot = np.where(Vwr_dot>0, Vwr_dot, 0)        # 满足墙壁反射条件 (发射角小于90)

        #     ## PD 接收端             
        #     Vrw = -Vwr                                               # PD到墙壁面元方向向量 (n,1,l1*w1,3)
        #     Vrw_dot = np.sum(Vrw * pd_Nv, axis=-1)                   # 向量内积 (n,1,l1*w1)

        #     mark1 = np.all(Vrw==0, axis=-1)                          # 异常点处理:判断墙壁反射面元和参考点是否重合(方向向量是否为零向量) (l*w*h,l1*w1)
        #     cos_pd_r_angle_rad = np.where(mark1, 1, Vrw_dot / d)     # PD接收角的余弦值   (n,l1*w1)
        #     pd_r_angle_rad = np.arccos(cos_pd_r_angle_rad)           # PD接收器入射角(弧度制) (n,l1*w1)
        #     pd_r_angle = np.degrees(pd_r_angle_rad)                  # 弧度制转为角度制 (n,l1*w1)
        #     Vrw_dot = np.where((pd_r_angle>=0) & (pd_r_angle<=fov), Vrw_dot, 0)  # 满足PD入射条件

        #     #⭐旋转后
        #     ## 墙壁面元发射端
        #     R_Vwr = R_pd_pos - w_pos                             # 墙壁面元d到PD的方向向量 (n,m,1,3) - (l1*w1,3) -> (n,m,l1*w1,3)
        #     R_d = np.linalg.norm(R_Vwr, axis=-1)                 # PD到墙壁面元的距离 (n,m,l1*w1)
        #     R_Vwr_dot = np.sum(R_Vwr * Nw, axis=-1)              # 向量内积 (n,m,l1*w1)
        #     R_Vwr_dot = np.where(R_Vwr_dot>0, R_Vwr_dot, 0)      # 满足墙壁反射条件 (发射角小于90)

        #     ## PD 接收端             
        #     R_Vrw = -R_Vwr                                       # PD到墙壁面元方向向量 (n,m,l1*w1,3)
        #     R_Vrw_dot = np.sum(R_Vrw * R_Nv, axis=-1)            # 向量内积 (n,m,l1*w1) 

        #     mark2 = np.all(R_Vrw==0, axis=-1)                             # 异常点处理:判断墙壁反射面元和参考点是否重合(方向向量是否为零向量) (n,m,l1*w1) 
        #     R_cos_pd_r_angle_rad = np.where(mark2, 1, R_Vrw_dot / R_d)    # PD接收角的余弦值   (n,l1*w1)
        #     R_pd_r_angle_rad = np.arccos(R_cos_pd_r_angle_rad)            # PD接收器入射角(弧度制) (n,l1*w1)
        #     R_pd_r_angle = np.degrees(R_pd_r_angle_rad)                   # 弧度制转为角度制 (n,l1*w1)
        #     R_Vrw_dot = np.where((R_pd_r_angle>=0) & (R_pd_r_angle<=fov), R_Vrw_dot, 0)  # 满足PD入射条件

        #     # 异常点处理:判断墙壁反射面元和参考点是否重合    
        #     Vwr_dot = np.where(Vwr_dot==0, 1, Vwr_dot)
        #     Vrw_dot = np.where(Vrw_dot==0, 1, Vrw_dot)
        #     d = np.where(Vwr_dot==0, 0, d)      
        #     R_d = np.where(R_d==0, 1, R_d)       
        #     R_Vrw_dot = np.where(R_d==0, 0, R_Vrw_dot)       
            
        #     # 代入计算 
        #     Gw = (d/R_d)**4 * np.abs(R_Vwr_dot/Vwr_dot) * np.abs(R_Vrw_dot/Vrw_dot)  # 比例系数值 (n,m,l1*w1)

        #     Gw = np.sum(Gw, axis=-1)    # 反射(NLOS)链路Gw求和 (n,m,l1*w1)-> (n,m) 
        #     G += Gw                     # 对所有反射面元比例系数值求和 (n,m) 

        # # 计算功率
        # R_P = G * P                     # (n,m)

        # # 旋转后的PD接收功率 (n,m)
        # R_P = np.reshape(R_P,-1)        # (n,m) -> (n*m)

        # return R_P
