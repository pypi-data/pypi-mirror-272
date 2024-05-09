import matplotlib.pyplot as plt
import numpy as np
from ..model import LED
from ..model import PD
from ..model import Room

class VLP_Model:
    def __init__(self,**kwargs):
        # 房间
        room = kwargs["Room"]
        self.room = Room(*room['size'].values(), *room['test_plane'].values(), *room['wall'].values())

        # PD
        pd = kwargs["PD_Info"] 
        pd1 = pd["PD1"]   
        pd2 = pd["PD2"]   
        pd3 = pd["PD3"]   
        pd4 = pd["PD4"]   
        
        # 获取PD位置和法向量
        pd1_pos, pd1_Nv = PD.recv_frame_model(l=pd["l"], alpha=pd1["alpha"], beta=pd1["beta"], center_tp_pos=self.room.get_tp_pos())  
        pd2_pos, pd2_Nv = PD.recv_frame_model(l=pd["l"], alpha=pd2["alpha"], beta=pd2["beta"], center_tp_pos=self.room.get_tp_pos()) 
        pd3_pos, pd3_Nv = PD.recv_frame_model(l=pd["l"], alpha=pd3["alpha"], beta=pd3["beta"], center_tp_pos=self.room.get_tp_pos())  
        pd4_pos, pd4_Nv = PD.recv_frame_model(l=pd["l"], alpha=pd4["alpha"], beta=pd4["beta"], center_tp_pos=self.room.get_tp_pos()) 
        
        self.pd1 = PD(n=pd["n"], fov=pd["fov"], Ar=pd["Ar"], Ts=pd["Ts"], pos=pd1_pos, Nv=pd1_Nv) 
        self.pd2 = PD(n=pd["n"], fov=pd["fov"], Ar=pd["Ar"], Ts=pd["Ts"], pos=pd2_pos, Nv=pd2_Nv)
        self.pd3 = PD(n=pd["n"], fov=pd["fov"], Ar=pd["Ar"], Ts=pd["Ts"], pos=pd3_pos, Nv=pd3_Nv) 
        self.pd4 = PD(n=pd["n"], fov=pd["fov"], Ar=pd["Ar"], Ts=pd["Ts"], pos=pd4_pos, Nv=pd4_Nv) 
        
        # LED
        led = kwargs["LED_Info"] 
        led1 = led["LED1"]
        self.led1 = LED(theta=led["theta"], signal=led["signal"], **led1)

    def get_data(self):
        """计算PD接收LED功率
        outshape: 输出数据形状,默认shape=(n,)(为None不改变形状)
        """
        # PD接收各LED的信号 (l*w*h)
        P_PD1 = self.pd1.recv_led_signal(led=self.led1, room=self.room) 
        P_PD2 = self.pd2.recv_led_signal(led=self.led1, room=self.room)
        P_PD3 = self.pd3.recv_led_signal(led=self.led1, room=self.room) 
        P_PD4 = self.pd4.recv_led_signal(led=self.led1, room=self.room) 

        # 待测点位置
        Xr, Yr, Zr = self.room.get_tp_pos(fmt='c')  #（l*w*h）
        
        return (P_PD1, P_PD2, P_PD3, P_PD4, Xr, Yr, Zr)  
      
    def show(self,z,savepath=...,showfig=True):
        """绘图
        z: 第三维度数据
        """
        xr, yr, _ = self.room.get_tp_grid()
        z = np.reshape(z, xr.shape)  
        ax = plt.axes(projection='3d')
        ax.plot_surface(xr, yr, z, cmap='viridis', edgecolor='none')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        if savepath != ...:
            plt.savefig(savepath)
        if showfig:
            plt.show()

