#This is a the list of all defined variables!
f  =  50.0
f_lb  =  0.0
f_ub  =  100.0
f_times  =  1
f_step  =  0
f_type  = 'fvar'
f_name = 'f'
f_scan = False

n_fvar = 1

t1  =  20.0
t1_lb  =  0.0
t1_ub  =  40.0
t1_times  =  1
t1_step  =  0
t1_type  = 'tvar'
t1_name = 't1'
t1_scan = False

t2  =  30.0
t2_lb  =  0.0
t2_ub  =  60.0
t2_times  =  1
t2_step  =  0
t2_type  = 'tvar'
t2_name = 't2'
t2_scan = False

t3  =  40.0
t3_lb  =  0.0
t3_ub  =  80.0
t3_times  =  1
t3_step  =  0
t3_type  = 'tvar'
t3_name = 't3'
t3_scan = False

n_tvar = 3

amp_ramsey  =  1.0
amp_ramsey_lb  =  0.0
amp_ramsey_ub  =  1.0
amp_ramsey_times  =  1
amp_ramsey_step  =  0
amp_ramsey_type  = 'ampvar'
amp_ramsey_name = 'amp_ramsey'
amp_ramsey_scan = False

amp_detect  =  1.0
amp_detect_lb  =  0.0
amp_detect_ub  =  1.0
amp_detect_times  =  1
amp_detect_step  =  0
amp_detect_type  = 'ampvar'
amp_detect_name = 'amp_detect'
amp_detect_scan = False

amp_pumping  =  1.0
amp_pumping_lb  =  0.0
amp_pumping_ub  =  1.0
amp_pumping_times  =  1
amp_pumping_step  =  0
amp_pumping_type  = 'ampvar'
amp_pumping_name = 'amp_pumping'
amp_pumping_scan = False

n_ampvar = 3

phvar  =  0.0
phvar_lb  =  0.0
phvar_ub  =  2.0
phvar_times  =  1
phvar_step  =  0
phvar_type  = 'phvar'
phvar_name = 'phvar'
phvar_scan = False
n_phvar = 1

n_ovar = 0


#___________________________________________
var_list = [f, t1, t2, t3, amp_ramsey, amp_detect, amp_pumping, phvar, ]
var_lb_list = [f_lb, t1_lb, t2_lb, t3_lb, amp_ramsey_lb, amp_detect_lb, amp_pumping_lb, phvar_lb, ]
var_ub_list = [f_ub, t1_ub, t2_ub, t3_ub, amp_ramsey_ub, amp_detect_ub, amp_pumping_ub, phvar_ub, ]
var_step_list = [f_step, t1_step, t2_step, t3_step, amp_ramsey_step, amp_detect_step, amp_pumping_step, phvar_step, ]
var_times_list = [f_times, t1_times, t2_times, t3_times, amp_ramsey_times, amp_detect_times, amp_pumping_times, phvar_times, ]
var_scan_list = [f_scan, t1_scan, t2_scan, t3_scan, amp_ramsey_scan, amp_detect_scan, amp_pumping_scan, phvar_scan, ]
var_type_list = [f_type, t1_type, t2_type, t3_type, amp_ramsey_type, amp_detect_type, amp_pumping_type, phvar_type, ]
var_name_list = [f_name, t1_name, t2_name, t3_name, amp_ramsey_name, amp_detect_name, amp_pumping_name, phvar_name, ]
#____________________________________________
#END
