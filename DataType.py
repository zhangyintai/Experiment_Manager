# For controlling experiments for the ion trap lab led by Prof. Yiheng Lin
# The code is written by Yintai Zhang, School of Physical Sciences, USTC
# Last updated: March 4th, 2019

Infinity = 2 ** 64 - 1

class FVar(object):

    def __init__(self, name, lb, ub, var, llb, uub):

        self.name = name.replace(' ','')
        self.lb = lb
        self.ub = ub
        self.llb = llb
        self.uub = uub
        self.step = 0
        self.scan = 0
        self.times = 1

        self.set_lb(lb)
        self.set_ub(ub)

        self.var = var
    
    def set_var(self, var):
        if var < self.uub and var > self.llb:
            self.var = var
            if self.var > self.ub:
                self.ub = (self.uub + self.var) / 2
            if self.var < self.lb:
                self.lb = (self.llb + self.var) / 2
    
    def set_lb(self, lb):
        if lb >= self.llb:
            self.lb = lb

    def set_ub(self, ub):
        if ub <= self.uub:
            self.ub = ub
    
    def set_all(self, var, lb, ub):
        self.set_var(var)
        self.set_lb(lb)
        self.set_ub(ub)
    
    def set_step(self, step):
        
        if step > self.lb - self.ub and step < self.ub - self.lb:
            self.step = step
        else:
            self.step = 0
            self.scan = 0
    
    def set_scan(self, state):
        self.scan = state
    
    
    def set_times(self, times):
        self.times = times

class TVar(object):

    def __init__(self, name, lb, ub, var, llb, uub):
        self.name = name.replace(' ','')
        self.lb = lb
        self.ub = ub
        self.llb = llb
        self.uub = uub
        self.step = 0
        self.scan = 0
        # self.channel = -1
        self.times = 1

        self.set_lb(lb)
        self.set_ub(ub)

        self.var = var
    
    def set_var(self, var):
        if var < self.uub and var > self.llb:
            self.var = var
            if self.var > self.ub:
                self.ub = (self.uub + self.var) / 2
            if self.var < self.lb:
                self.lb = (self.llb + self.var) / 2
    
    def set_lb(self, lb):
        if lb >= self.llb:
            self.lb = lb

    def set_ub(self, ub):
        if ub <= self.uub:
            self.ub= ub
    
    def set_all(self, var, lb, ub):
        self.set_var(var)
        self.set_lb(lb)
        self.set_ub(ub)

    def set_step(self, step):
        
        if step > self.lb - self.ub and step < self.ub - self.lb:
            self.step = step
        else:
            self.step = 0
            self.scan = 0
    
    def set_scan(self, state):
        self.scan = state
    
    def set_times(self, times):
        self.times=times

class AmpVar(object):

    def __init__(self, name, lb, ub, var, llb, uub):
        self.name = name.replace(' ','')
        self.lb = lb
        self.ub = ub
        self.llb = llb
        self.uub = uub
        self.step = 0
        self.scan = 0
        # self.channel = -1
        self.times = 1

        self.set_lb(lb)
        self.set_ub(ub)

        self.var = var
    
    def set_var(self, var):
        if var < self.uub and var > self.llb:
            self.var = var
            if self.var > self.ub:
                self.ub = (self.uub + self.var) / 2
            if self.var < self.lb:
                self.lb = (self.llb + self.var) / 2
    
    def set_lb(self, lb):
        if lb >= self.llb:
            self.lb = lb

    def set_ub(self, ub):
        if ub <= self.uub:
            self.ub= ub
    
    def set_all(self, var, lb, ub):
        self.set_var(var)
        self.set_lb(lb)
        self.set_ub(ub)

    def set_step(self, step):
        
        if step > self.lb - self.ub and step < self.ub - self.lb:
            self.step = step
        else:
            self.step = 0
            self.scan = 0
    
    def set_scan(self, state):
        self.scan = state

    
    def set_times(self, times):
        self.times = times

class PhVar(object):

    def __init__(self, name, lb, ub, var, llb, uub):
        self.name = name.replace(' ','')
        self.lb = lb
        self.ub = ub
        self.llb = llb
        self.uub = uub
        self.step = 0
        self.scan = 0
        # self.channel = -1
        self.times = 1

        self.set_lb(lb)
        self.set_ub(ub)

        self.var = var
    
    def set_var(self, var):
        if var < self.uub and var > self.llb:
            self.var = var
            if self.var > self.ub:
                self.ub = (self.uub + self.var) / 2
            if self.var < self.lb:
                self.lb = (self.llb + self.var) / 2
    
    def set_lb(self, lb):
        if lb >= self.llb:
            self.lb = lb

    def set_ub(self, ub):
        if ub <= self.uub:
            self.ub= ub
    
    def set_all(self, var, lb, ub):
        self.set_var(var)
        self.set_lb(lb)
        self.set_ub(ub)

    def set_step(self, step):
        
        if step > self.lb - self.ub and step < self.ub - self.lb:
            self.step = step
        else:
            self.step = 0
            self.scan = 0
    
    def set_scan(self, state):
        self.scan = state

    
    def set_times(self, times):
        self.times = times

class OVar(object):
    def __init__(self, name, lb, ub, var, llb, uub):
        self.name = name.replace(' ','')
        self.lb = lb
        self.ub = ub
        self.llb = llb
        self.uub = uub
        self.step = 0
        self.scan = 0
        # self.channel = -1
        self.times = 1

        self.set_lb(lb)
        self.set_ub(ub)

        self.var = var
    
    def set_var(self, var):
        if var < self.uub and var > self.llb:
            self.var = var
            if self.var > self.ub:
                self.ub = (self.uub + self.var) / 2
            if self.var < self.lb:
                self.lb = (self.llb + self.var) / 2
    
    def set_lb(self, lb):
        if lb >= self.llb:
            self.lb = lb

    def set_ub(self, ub):
        if ub <= self.uub:
            self.ub= ub
    
    def set_all(self, var, lb, ub):
        self.set_var(var)
        self.set_lb(lb)
        self.set_ub(ub)

    def set_step(self, step):
        
        if step > self.lb - self.ub and step < self.ub - self.lb:
            self.step = step
        else:
            self.step = 0
            self.scan = 0
    
    def set_scan(self, state):
        self.scan = state  
    
    def set_times(self, times):
        self.times = times

class Experiment(FVar, TVar, AmpVar, PhVar):

    def __init__(self, typ_code, typ, exp_code, name):
        
        self.typ_code = typ_code
        self.exp_code = exp_code
        self.typ = typ  
        self.name = name
        self.enable = False
        self.config = ""
        self.window_open = False
        self.FVar_list = []
        self.TVar_list = []
        self.AmpVar_list = []
        self.PhVar_list = []
    
    def set_name(self, name):
        self.name = name
    
    def set_config(self, dir):
        self.config = dir
    
    def set_enable(self):
        self.enable = True
    
    def set_disable(self):
        self.enable = False
    
    def ReadVar(self, FVar_list, TVar_list, AmpVar_list, PhVar_list):
        self.FVar_list = FVar_list
        self.TVar_list = TVar
        self.AmpVar_list = AmpVar
        self.PhVar_list = PhVar_list

class Device(object):
    
    def __init__(self, name, no, port, typ_code, channels):

        self.no = no
        self.name = name
        self.port = port
        self.typ_code = typ_code
        '''
        DDS 0
        TTL 1
        AWG 2
        '''
        self.channels = channels
        self.channel_list = []
        self.channel_flag = []
        
        for i in range (0, channels):
            self.channel_flag.append(False)
    
    def channel_on(self, i):
        if i < self.channels - 1:
            self.channel_flag[i] = True
    
    def channel_off(self, i):
        if i < self.channels - 1:
            self.channel_flag[i] = False

class Channel(object):

    def __init__(self, device_no, device_channel_no):
        self.device_no = device_no
        self.device_channel_no = device_channel_no
