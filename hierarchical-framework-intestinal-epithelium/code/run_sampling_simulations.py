
# coding: utf-8

# #Sampling simulations
# OJM

# In[1]:

import numpy as np
import pandas as pd
import numpy.linalg as la
import scipy as sp
from scipy import stats
import scipy.interpolate as interpolate
import scipy.special as special
import matplotlib as mpl
import matplotlib.pyplot as plt
import emcee
import os
import errno
import george
from george import kernels
get_ipython().magic(u'matplotlib inline')


# In[2]:

#TODO - add into modules?
get_ipython().magic(u'run data_analysis_functions.ipynb')
get_ipython().magic(u'run simulation_functions.ipynb')


# In[3]:

def sample_sim(data_dir='../data-working/TXT_BrdU/',sample_type='BrdU',
                          actual_out_times= np.array([60.,120.,360.,600.,1080.,1920.]),times_to_fit_i=[5],precision_time=4,
                          p0=np.array([1.0,2.0,0.01,0.01,0.01]),p_var_i=[],x_min=0.,x_max=100.,
                          k=3,s=15,nx=100,n_walkers=10,n_dim=4,n_burn=10,n_sample=10):
    """
    sampling solution to inverse problem
    -
    notes
    a key difficulty is choosing proper comparison grid
    also, systematic regularisation - dependence on number of parameters etc? determining reg. parameter
    best passing of parameters etc
    -
    structure
    initial condition
    data for fitting
    model definition
    residuals function
    likelihood
    prior
    posterior
    
    
    """
    #---
    #get initial condition
    files_in_dir= os.listdir(data_dir)
    files_in_dir.sort() #assumes files have same name format!!

    start= actual_out_times[0]
    time_format= '%0'+('%1d' % precision_time)+'d'
    file_ic= get_data_file(data_dir,time_format%start)
    
    density_results= process_and_fit_label_data_file(data_dir=data_dir,file_to_fit=file_ic,
                                                     sample_type=sample_type,x_max=x_max,
                                                     do_plot=False)
    initial_profile_f= density_results[-1]
    
    #---
    #data for comparison. NOTE - ignore initial profile [todo - change?]
    #TODO - use times_to_fit_i???
    #x_data_to_fit= np.tile(np.arange(x_min,x_max),(actual_out_times.size-1,1))
    x_data_to_fit= np.tile(np.arange(x_min,x_max),(len(times_to_fit_i),1))
    x_data_to_fit= np.transpose(x_data_to_fit)
    #print 'x data'
    #print x_data_to_fit
    label_data_at_x_data= np.zeros(x_data_to_fit.shape)
    sample_size_at_x_data= np.zeros(x_data_to_fit.shape)

    for i in range(0,len(times_to_fit_i)):
        current_time= actual_out_times[times_to_fit_i[i]]
        file_current= get_data_file(data_dir,time_format%current_time)
        print file_current
        data_result= process_and_fit_label_data_file(data_dir=data_dir,file_to_fit=file_current,sample_type=sample_type,k=k,s=s,x_max=100,do_plot=False)
        sample_size_result= get_sample_sizes_for_data_file(data_dir=data_dir,file_to_fit=file_current,sample_type=sample_type,k=k,s=s,x_max=100,do_plot=False)
        #careful here - data grid concept needs to be tidied up.
        label_data_at_x_data[:,i]= np.append(data_result[0],np.zeros(x_max-data_result[0].size))
        sample_size_at_x_data[:,i]= np.append(sample_size_result,np.zeros(x_max-sample_size_result.size))
    
    #convert between experimental times and simulation times 
    norm_out_times= (actual_out_times-min(actual_out_times))/(max(actual_out_times)-min(actual_out_times))
    
    #---
    #function for one sim.
    def model(p_var_model):
        """
        simulation model
        -
        notes:
        output formats for each quantity are -
        [column of results at time 1|column of results at time 2|...etc...]
        uses arguments from outer function - bad practice?
        bit of a hack with 'global' vs. local arguments.
        inputs - only the 'substantive' part - not the 'noise parameters'
        TODO - split 'noise' and 'substantive' out. First, fix noise.
        """
        p= np.copy(p0) #careful of python 'labels/tags' vs 'containers'.
        p[p_var_i]= np.copy(p_var_model[p_var_i]) #WHAT TO DO HERE? careful of python 'labels/tags' vs 'containers'.
        #print 'test p0 changing:' 
        #print p==p0
        #print p[p_fixed_i]== p0[p_fixed_i]
        #print 'here'
        velocity_f= velocity_from_integrated_proliferation(proliferation_profile(p=p,x_max=x_max))
        controller= setup(nx=nx,initial_profile_f=initial_profile_f,velocity_f=velocity_f,norm_out_times=norm_out_times)
        #controller.verbosity= 0
        controller.run()

        #extract (all) simulation results
        output_shape= [np.size(controller.frames[0].state.q[0,:],axis=0),np.size(controller.frames,axis=0)]
        #print output_shape
        labels= np.zeros(output_shape)
        x_centres= np.zeros(output_shape)
        velocity= np.zeros(output_shape)
        for i in range(0,np.size(controller.out_times,axis=0)):
            labels[:,i]= controller.frames[i].state.q[0,:]
            #don't actually vary with time!
            x_centres[:,i]= controller.frames[0].state.grid.c_centers[0]
            velocity[:,i]= controller.frames[0].state.aux[0,:]

        return labels, velocity, x_centres

    #---
    #residuals function
    def residuals(p_var_current,flatten_residual=True,return_model=False):#,p0=np.array([1.0,2.0,0.01,0.01,0.01]))#,p_fixed_i=[]):#,x_data_to_fit=x_data_to_fit,label_data_to_fit=label_data_to_fit,times_to_fit=[]):
        """
        residuals between model solutions and data
        -
        notes
        data and model results are matrices/arrays!
        in 'column vector' storage format? Each column vector is a space grid; column index is a time?
        added 'return_model' option (default off for compat.) so can return model values as well (for any extra calc.).
        -
        Plan
        general outline
        -at a given time
        [vectorised]
        --at a set of data comparison x points
        ---get data values
        ---get solution values (via interp.)
        ---compute residual and store as column vector in residual matrix
        -(in another function) square values and sum to get a single scalar
        approach
        -test cell to consider a vector of data values and test sim and calc residual
        """
        #get solutions at all fit times
        results= model(p_var_model=p_var_current)
        labels_model= results[0][:,times_to_fit_i] #note: changed indexing
        x_centres_model= results[2][:,times_to_fit_i] #note: changed indexing
        
        #print 'labels_model'
        #print labels_model

        #data grid. TODO - do better. Note: don't include initial condition so one index smaller.
        #use e.g. structured arrays?? For now - collect all but only compare subset. Inefficient.
        #label_model_at_x_data_current= np.zeros(x_data_to_fit.shape[0])
        residual_at_x_data= np.zeros(x_data_to_fit.shape)
        label_model_at_x_data= np.zeros(x_data_to_fit.shape)
        #times_to_fit_i is relative to original time scale - need to subtract one for 'data fitting' scale (aleady discar. t0)
        #for i in np.subtract(times_to_fit_i,1): #shift times_to_fit_i index referencing so t > t0
        for i in range(0,len(times_to_fit_i)):
            #TODO - assert i>0
            #print 'i'
            #print i
            #label_model_at_x_data_current= np.interp(x_data_to_fit[:,i],x_centres_model[:,i],labels_model[:,i])
            label_model_at_x_data[:,i]= np.interp(x_data_to_fit[:,i],x_centres_model[:,i],labels_model[:,i])
            residual_at_x_data[:,i]= label_data_at_x_data[:,i]-label_model_at_x_data[:,i]
        #print 'label model at x pre flat'
        #print label_data_at_x_data
        if flatten_residual:
            if return_model:
                return np.ravel(residual_at_x_data.T), np.ravel(label_model_at_x_data.T) #ravel flattens into single vector
            return np.ravel(residual_at_x_data.T) #ravel flattens into single vector
        else:
            if return_model:
                return residual_at_x_data, label_model_at_x_data
            return residual_at_x_data
        
    #---
    def lnlike(p_var_current):
        """
        notes
        data is available in larger function (hack for now)
        TODO 
        - rewrite normal likelihood
        - write binomial likelihood
        - make sure using 'exact data' not interpolated (for both of above)
        """
        #print 'likelihood'
        #print p_var_current
        # the log-likelihood is pretty much sum of squared residuals
        y_bar_resid, y_bar_model= residuals(p_var_current=p_var_current,return_model=True)
        
        sample_size= np.ravel(sample_size_at_x_data.T)
        y_bar_data= np.ravel(label_data_at_x_data.T)
        sigma= np.sqrt(np.divide(y_bar_model*(1.-y_bar_model),sample_size)) #note: may include inf or nan - deal with later
        #print 'sigma'
        #print sigma
        #print 'mean sigma'
        #print np.ma.mean(sigma)
        #print 'resid/sigma'
        #print np.divide(resid,sigma)
        #print 'model'
        #print model
        #print 'resid'
        #print resid
        #print 'sample size'
        #print (np.ravel(sample_size_at_x_data.T))
        #print np.ravel(sample_size_at_x_data.T)
        #sigma=0.1 #temp! DOES THIS VARY?
        #print sigma
        #denom= np.power(sigma,2)
        #numpy.ma.
        #ll= -0.5*(np.sum(np.power(np.divide(resid,sigma),2))+np.sum(np.ma.log(np.power(sigma,2)*2.*np.pi)))
        
        #ll= -0.5*(np.power(la.norm(np.divide(y_bar_resid,sigma),2),2)+np.sum(np.ma.log(np.power(sigma,2)*2.*np.pi)))
        ll= np.ma.sum(sample_size*(y_bar_data*np.ma.log(y_bar_model)+(1.-y_bar_data)*np.ma.log(1.-y_bar_model))) 
        #ll= BINOMIAL...
        #print lp
        return ll
    
    def lnprior(p_var_current):
        """
        """
        # The parameters are stored as a vector of values, so unpack them?
        #CAREFUL OF SIGMA?
        #prior_type= 'uniform'
        #prior_type= 'gaussian-simple'
        prior_type= 'gaussian-with-cov'
        if prior_type=='uniform':
            # We're using only uniform priors (for now - try sparsity!)
            if np.logical_or((p_var_current<-2).any(),(p_var_current>2).any()):
                return -np.inf
            return 0 #prior up to constant -> log up to constant
        if prior_type=='gaussian-simple':
            #sigma_prior= 0.1#key is ratio to sigma in likelihood??
            sigma_prior= 2.0# typical variation in rates. Notes: 1.0 works well, 5.0 not so well - 'wiggly'
            denom= np.power(sigma_prior,2)
            #(la.norm(p_var-np.mean(p_var),ord=penalty_order)**penalty_order)
            #print 'lnprior'
            #print -0.5*(np.power(la.norm(np.divide(p_var_current-p_var0,denom),2),2)+len(p_var0)*np.log(denom*2*np.pi))
            return -0.5*(np.power(la.norm(np.divide(p_var_current-p0[p_var_i],denom),2),2)+len(p_var_i)*np.log(denom*2*np.pi))
            #return -0.5*(np.power(la.norm(np.divide(p_var_current-p_var0,denom),2),2)+len(p_var0)*np.log(denom*2*np.pi))
        if prior_type=='gaussian-with-cov':
            #use 'george' gaussian process package for now. Could do manual or could extend to proper gaussian process.
            #-correlation matrix 2.0 usual.
            #parameter_correlation_length= 2.0
            parameter_correlation_length= 5.0
            kernel = kernels.ExpSquaredKernel(0.5*parameter_correlation_length)
            #kernel = kernels.ExpSquaredKernel(0.5) #0.5 -> correlation length approx. 1 parameter; 2*L.
            gp = george.GP(kernel)
            correlation_matrix= gp.get_matrix(p_var_i)
            #-standard deviations
            sd_decay_region=3 #number of parameters from end over which sd decays.
            #sd_prior= 1.0*np.append(np.ones(len(p_var_i)-sd_decay_region),correlation_matrix[0,1:1+sd_decay_region]) #correlation_matrix[0,:]#
            sd_prior= 0.5*np.append(np.ones(len(p_var_i)-sd_decay_region),correlation_matrix[0,1:1+sd_decay_region]) #correlation_matrix[0,:]#
            #sd_prior= 1.0*np.append(np.ones(len(p_var_i)-1),0.3) #correlation_matrix[0,:]#
            var_prior= np.outer(sd_prior,sd_prior)
            sigma= var_prior*correlation_matrix #note: element-wise product
            #sd=2.0
            #sigma= sd*gp.get_matrix(p_var_i)
            dist_dim = np.float(len(p_var_i))
            det = np.linalg.det(sigma)
            if det == 0:
                raise NameError("The covariance matrix can't be singular")
            #note: calculation is in log form.
            norm_const1 = -0.5*dist_dim*np.log(2.*np.pi)
            norm_const2 = -0.5*np.log(det)
            err = p_var_current-p0[p_var_i]
            #print 'here 2'
            #print err
            numerator = -0.5*np.dot(err,np.dot(np.linalg.inv(sigma),err))
            return norm_const1+norm_const2+numerator  
    
    def lnprob(p_var_current):
        """
        """
        lp = lnprior(p_var_current)
        if not np.isfinite(lp):
            return -np.inf
        return lp + lnlike(p_var_current)
    
    #Sampling starts
    import emcee
    flatten_residual= True
    p_var0= np.copy(p0[p_var_i])
    
    #start walkers from where? could be p0 or maximum likelihood/optimised solution.
    #n_walkers,n_dim = n_walkers,n_dim #50
    #p_var0 = [p_var0+1.e-4*np.random.randn(n_dim) for i in range(n_walkers)]
    p_var0 = [p_var0+1.e-2*np.random.randn(n_dim) for i in range(n_walkers)]
    
    #create sampler
    sampler = emcee.EnsembleSampler(n_walkers,n_dim,lnprob)
    #burn
    import time as timer
    t0 = timer.time()
    pos_post_burn,prob_post_burn,state_post_burn = sampler.run_mcmc(p_var0, n_burn) #50
    t1 = timer.time()
    t_burn= t1-t0
    print 'burn time: '
    print t_burn
    #post-burn
    sampler.reset()
    t0 = timer.time()
    pos,prob,state = sampler.run_mcmc(pos_post_burn, n_sample) #1000
    t1 = timer.time()
    t_sampler= t1-t0
    print 'sample time: '
    print t_sampler
    return sampler, t_burn, t_sampler


# a= np.array([0,1,2,3])
# a.shape

# a= np.array([0.,1.,2.,3.])
# b= 3.*a
# print np.sum(3.*a)
# print np.sum(b)
# print np.log(a)

# a= np.array([0.,1.,2.,3.])
# b= np.power(a,2)
# print np.log(a)
# print b
# print np.log(b)
# print np.divide(1.,2.)
# print np.divide(a,np.log(a))

# In[5]:

#sampling approach here
#BrdU
#data_dir='../data-working/TXT_BrdU/'
#sample_type='BrdU'
#actual_out_times= np.array([120.,360.,600.])#,1920.])
##times_to_fit_i=[1,2]
#times_to_fit_i=[1,2]

#AraC
data_dir='../data-working/TXT_AraC_01_IdU/'
sample_type='AraC'
#actual_out_times= np.array([1080,1260.,1500.])
#actual_out_times= np.array([1260.,1500.])#,1620.])
actual_out_times= np.array([1140.,1260.])#,1620.])
#actual_out_times= np.array([1140.,1260.,1500.])#,1620.])
#times_to_fit_i=[1,2]
times_to_fit_i=[1]

#GLP2_01
#Low
#data_dir='../data-working/TXT_GLP2_01_Ileums/Low/'
#sample_type='GLP2_01_Ileums_Low'
#actual_times= np.array([1500,2400.])
#Med
#data_dir='../data-working/TXT_GLP2_01_Ileums/Med_Full/'
#sample_type='GLP2_01_Ileums_Med'
#actual_out_times= np.array([60.,1020.,1620.])#,2460.])
#High
#data_dir='../data-working/TXT_GLP2_01_Ileums/High_Full/'
#sample_type='GLP2_01_Ileums_High'
#actual_out_times= np.array([60.,1020.,2460.])
#times_to_fit_i= [1,2]

#p0=np.random.uniform(low=-1.0,high=1.0,size=3)
#p0= np.append(p0,np.zeros(17))
#p0= np.array([0.5,0.5,0.5,0.5])
#p0= np.array([0.0,0.0,0.0,0.0])
#p0= np.array([0.5,1.5,0.5,0.0,0.0])#decent guess at solution, based on opt.
p0= np.array([0.1,0.1,0.1,0.0,0.0])#decent guess at solution, based on opt.
p_var_i= [0,1,2,3,4]
p0= np.append(p0,np.zeros(15))

print 'num free parameters'
print len(p_var_i)
print 'num fixed parameters'
print len(p0)-len(p_var_i)

#p0[p_var_i]= [0.50270828, 1.58121376, 0.17217782, -0.0203373] #from optimisation run!

p_start= np.copy(p0)
print 'p0: ' 
print p0

n_dim=len(p_var_i)
#minimal test #(10,2,2 = about 30-40 sec? For 4 parameters.)
#n_walkers= 10
#n_burn=2
#n_sample=2
#medium test (20, 100, 100 = about one hour? For 4 parameters)
#n_walkers= 20
#n_burn=100
#n_sample=100
#--TO USE--
#(100, 100, 100 = about 5 hours for 4 parameters)
#n_walkers= 100 
#n_burn=100
#n_sample=100
#(50, 100, 100 = about 2.5 hours for 4 parameters?) More like 2.7 these days? Similar for 5 param.
n_walkers= 50 
n_burn=100
n_sample=100

sampler, t_burn, t_sampler= sample_sim(p0=p0,p_var_i=p_var_i,n_walkers=n_walkers,n_dim=n_dim,
                                       n_burn=n_burn,n_sample=n_sample,data_dir=data_dir,sample_type=sample_type,
                                       actual_out_times=actual_out_times,times_to_fit_i=times_to_fit_i)
print 'times (burn, sampler, total): '
print t_burn
print t_sampler
t_total= t_burn+t_sampler
print t_total


# In[6]:

import triangle
tri_plot = triangle.corner(sampler.flatchain, labels=['p'+str(p_var_i[i]) for i in range(0,len(p_var_i))])
#tmp.savefig()
#                      truths=[alpha_true, beta_x_true, beta_y_true, eps_true])


# In[35]:

#save triangle plot

#sample_type= 'BrdU'
output_path= '../figures/proliferation_profiles/'
save_path= output_path+sample_type+'/'
save_fig= True
if save_fig:
    try:
        os.makedirs(save_path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(save_path):
            pass
        else: raise
    tri_plot.savefig(save_path+'mcmc-proliferation-rates-'+sample_type+'.pdf')
tri_plot.show()


# In[36]:

#save sampler outputs
import pickle

#sample_type= 'BrdU'
output_path= '../raw-output/'
save_path= output_path+sample_type+'/'
save_raw= True
if save_raw:
    try:
        os.makedirs(save_path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(save_path):
            pass
        else: raise
    pickle.dump( sampler.chain, open( save_path+"sampler_chain_"+sample_type+".p", "wb" ) )
    pickle.dump( sampler.flatchain, open( save_path+"sampler_flat_chain_"+sample_type+".p", "wb" ) )
    pickle.dump( sampler.acceptance_fraction, open( save_path+"sampler_acceptance_fraction_"+sample_type+".p", "wb" ) )


# In[22]:

1./np.divide(1.,0.0)


# In[16]:

a= [0,1,2]
b= np.array([0,2,3,4])
c= np.array([[0,1,4,3],[0,1,2,3]])
print len(a)
print len(b)
print c
print b[a]
print c[:,a]


# In[9]:

for i in a:
    print i


# In[21]:

for i in range(0,len(a)):
    print i
print len(a)


# In[54]:




# In[ ]:



