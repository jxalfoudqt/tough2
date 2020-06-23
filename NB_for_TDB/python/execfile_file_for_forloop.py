import os
import numpy as np
cwd = os.getcwd()

#volume_parameter          = np.array([1.e20])
volume_parameter          = np.array([1.e20])
compressibility_parameter = np.array([1.e-10])
relative_error_parameter  = np.array([1.e-8])
porosity_parameter        = np.array([0.99])
maximum_dt_parameter      = np.array([500])

p=0
while p<len(volume_parameter):
    s=0
    while s<len(compressibility_parameter):
        k=0
        while k<len(relative_error_parameter):
            o=0
            while o<len(porosity_parameter):
                q=0
                while q<len(maximum_dt_parameter):
                    execfile(cwd+'/python/pre_process.py')
                    execfile(cwd+'/python/running_model.py')
                    execfile(cwd+'/python/parsing_outputfile.py')
                    execfile(cwd+'/python/post_process.py')                    
                    q+=1                
                o+=1            
            k+=1        
        s+=1
    p+=1
	
# p=0
# while p==0:
    # s=0
    # while s==0:
        # k=0
        # while k==0:
            # o=0
            # while o==0:
                # q=0
                # while q==0:
                    # execfile(cwd+'/python/pre_process.py')
                    # execfile(cwd+'/python/running_model.py')
                    # execfile(cwd+'/python/parsing_outputfile.py')
                    # execfile(cwd+'/python/post_process.py')                    
                    # q+=1                
                # o+=1            
            # k+=1        
        # s+=1
    # p+=1