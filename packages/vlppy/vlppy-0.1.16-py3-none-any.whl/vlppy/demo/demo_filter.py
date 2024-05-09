import numpy as np
import matplotlib.pyplot as plt
from ..signal import filter,plot

def main():
    print("This is a demo about filter!")
    Fs = 13000 # 采样频率,单位为Hz
    N = 1024  # 采样点数
    t = np.arange(N) * 1/Fs  # 产生一个以采样时间为间隔的时间序列

    print("Generate a cosine signal containing 3KHz, 4KHz and 5KHz.")
    # 产生多个子信号
    f1 = 3000
    f2 = 4000
    f3 = 5000
    Amp = 10

    U1 = Amp * np.cos(2 * np.pi * f1 * t)
    U2 = Amp * np.cos(2 * np.pi * f2 * t)
    U3 = Amp * np.cos(2 * np.pi * f3 * t)

    # 叠加
    U = U1 + U2 + U3 

    # 显示信号的波形
    plot.signal_wave(t,U1,U2,U3,U,xlab='t(s)',ylab=['U1','U2','U3','U'])
    plot.signal_fft_wave(t,U1,U2,U3,U,xlab='f(Hz)',ylab=['U1','U2','U3','U'])

    # 滤波器设计
    Fc = f1 # 滤波频率
    print(f"A {int(Fc/1000)}KHz bandpass filter is used to filter this signal.")
    ft = filter.ButterFilter(Fc,Fs,[200,400],[3,64])        # 巴特沃斯带通滤波器
    # ft = filter.BesselFilter(Fc,Fs,10,400)                  # 贝塞尔滤波器
    # ft = filter.ChebyFilter(Fc,Fs,[300,450],[3,64],cheby=2) # 切比雪夫II型滤波器
    # ft = filter.EllipFilter(Fc,Fs,[300,450],[3,64])         # 椭圆滤波器
    # ft = filter.FIR_Filter(Fc,Fs,30,300,window='hamming')   # Fir滤波器
    ft.show_wave(N)

    # 滤波
    Ulf = ft.filter(U)

    # 滤波信号波形
    plot.signal_wave(t,Ulf,xlab='t(s)',ylab='Ulf')
    plot.signal_fft_wave(t,Ulf,xlab='f(Hz)',ylab='Ulf')

if __name__ == '__main__':
    main()

