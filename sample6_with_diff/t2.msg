 =========================================================================
 i T O U G H 2 _ 4  R U N  date: Fri  5 Jul 03:01:36 BST 2019
 =========================================================================

Command submitted: /home/osboxes/bin/itough2 -tough2 -to sam6_0.listing sam6 4

cp: missing destination file operand after '/home/osboxes/it2_2897'
Try 'cp --help' for more information.
Note: The following floating-point exceptions are signalling: IEEE_DENORMAL
STOP iTOUGH2 terminated in iTOUGH2Wrapper

 ---     0 error(s) and  0 warning(s) detected
cp: cannot stat '*.csv': No such file or directory
cp: cannot stat '*.gnu': No such file or directory
 FILE /tmp/parallel.info DOES NOT EXIST. ASSUME THIS IS A SERIAL RUN OR THIS IS THE PARENT PROCESS.
 HAVE READ UNKNOWN BLOCK LABEL "     " --- IGNORE THIS, AND CONTINUE READING INPUT DATA

 PRIMARY VARIABLE NO. 2 HOLDS SATURATION (RIGHT?)

                        ************************************************************************************
                        *                       EVALUATE FLOATING POINT ARITHMETIC                         *
                        ************************************************************************************
                        *                                                                                  *
                        * FLOATING POINT PROCESSOR HAS APPROXIMATELY 15 SIGNIFICANT DIGITS                 *
                        *                                                                                  *
                        * DEFAULT VALUE OF INCREMENT FACTOR FOR NUMERICAL DERIVATIVES IS DFAC = 1.0537E-08 *
                        * DEFAULT VALUE FOR DFAC WILL BE USED                                              *
                        *                                                                                  *
                        ************************************************************************************


 ==================================================================
      S T A T U S   O F   i T O U G H 2   S I M U L A T I O N
 ==================================================================

 Date                        :  5-Jul-19  03:01
 iTOUGH2 file                : invdir
 TOUGH2 file                 : sam6
 Working directory           : /home/osboxes/local_2/tough2/tough2/sample6
 Temporary directory         : /home/osboxes/it2_2897
 UNIX command line arguments : -tough2 -to sam6_0.listing sam6 4
 Comment                     : First guess.                                                                   

 Iterations completed        :              0    Iterations to go      1
 TOUGH2 runs completed       :              1    Unsuccessful steps    0
 TOUGH2 runs to go (approx.) :              1    Log(Levenberg)        0
 CPU time used [sec]         :           1.60    for last step      1.56
                                        @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
                                        @                                             @
                                        @   @  @@@@@   @@   @  @   @@@  @  @   @@@@   @
                                        @        @    @  @  @  @  @     @  @  @    @  @
                                        @   @    @    @  @  @  @  @ @@  @@@@     @@   @
                                        @   @    @    @  @  @  @  @  @  @  @    @@    @
                                        @   @    @     @@    @@    @@@  @  @  @@@@@@  @
                                        @                                             @
                                        @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

                                     iTOUGH2 V7.1, FEBRUARY 3, 2017 FOR LINUX, S. FINSTERLE
                                COPYRIGHT (C) 2016, THE REGENTS OF THE UNIVERSITY OF CALIFORNIA
                                     THROUGH LAWRENCE BERKELEY NATIONAL LABORATORY
                                                  ALL RIGHTS RESERVED

 ==================================================================================================================================
                                          >>>>>>>>>>>>>  5-Jul-19  03:01 <<<<<<<<<<<<<
 ==================================================================================================================================
 iTOUGH2 INPUT FILE            :  invdir
 TOUGH2 INPUT FILE             :  sam6
 WORKING DIRECTORY             :  /home/osboxes/local_2/tough2/tough2/sample6
 TEMPORARY DIRECTORY           :  /home/osboxes/it2_2897
 EQUATION OF STATE MODULE      :  4 --> Non-isothermal, water and air, with vapor pressure lowering
 COMPONENTS                    :  WATER     AIR       HEAT                                    
 PHASES                        :  GAS       LIQUID                        
 TOUGH2 TITLE                  :  sam6: Ventilation experiment                                                    
 ==================================================================================================================================

 **********************************************************************************************************************************
                                                              INPUT
 **********************************************************************************************************************************


 PARAMETERS
 ==========

 ----------------------------------------------------------------------------------------------------------------------------------
  # ANNOTATION      PARAMETER TYPE    ROCKS  PRIOR INFO. INIT. GUESS    STD. DEV.  LOWER BOUND  UPPER BOUND   MAX. STEP   INDEX
 ----------------------------------------------------------------------------------------------------------------------------------
 ----------------------------------------------------------------------------------------------------------------------------------


 OBSERVATIONS
 ============


 TIMES:     0  [sec]                                         
 -------------------



 ----------------------------------------------------------------------------------------------------------------------------------
 SET ANNOTATION      DATATYPE        ELEME/CONNE       STD. DEV. MIN. TIME MAX. TIME LOG(V/M/S) #DATA     #CALI     FACTOR  IOBS
 ----------------------------------------------------------------------------------------------------------------------------------
 ----------------------------------------------------------------------------------------------------------------------------------


 --------------------------------------------------
 Number of datasets                    :    0
 Number of calibration times           :    0                                          
 Number of calibration points          :    0
 Number of predictions                 :    0
 Number of dummy observations          :    0
 Number of specified parameters        :    0
 Number of TOUGH-related parameters    :    0
 Number of TOUGH-independent parameters:    0
 Number of inactive parameters         :    0
 Number of tied parameters             :    0
 Number of adjustable parameters   (n) :    0
 Number of superparameters (max.)      :    0
 Number of parameters with prior info. :          0
 Number of regularization terms        :          0
                                              -----
 Total number of observations      (m) :          0                                    
                                              =====
 Degree of freedom               (m-n) :    0
 --------------------------------------------------


 COMPUTATIONAL PARAMETERS
 ========================

 Algorithm or application mode                   :                   Forward Run                                                  
 Maximum number of iTOUGH2 iterations            :                             1
 Maximum number of TOUGH2 calls                  :                             1
 Maximum number of uphill steps                  :                            10
 Maximum size of scaled parameter step           :                     unlimited
 Initial Levenberg parameter                     :                      1.00E+00
 Marquardt parameter                             :                     -1.00E+01
 Finite difference quotient for Jacobian         :                       forward
 Diagonal of Tikhonov matrix                     :                         (n/a)
 Automatic FD update of Jacobian                 :                             0
 Skip iterations with FD update of Jacobian      :                             0
 Broyden rank-one update of Jacobian             :                             0
 Increment factor for computing derivatives      :                      1.00E-02
 Simple parameter bounds enforced by             :         Hard parameter bounds
 Variance for error analysis                     :                  a posteriori
 Format of plotfile                              :                       Tecplot
 Objective Function                              :                 Least-Squares


 COMPUTER SYSTEM
 ===============

 Machine type                                    : Linux               
 UNIX script file name                           : /home/osboxes/bin/itough2                                                       
 UNIX command line arguments                     : -tough2 -to sam6_0.listing sam6 4
 Host name                                       : osboxes
 User name                                       : osboxes
 Compilation date                                : Thu 25 Apr 05:48:14 BST 2019            
 Compiler                                        : gfortran             
 Compiler options                                : -c -O3 -fsign-zero -ffree-line-length-none                      
 Executable                                      : /home/osboxes/itough2/Executable/itough2.lnx


 --- End of iTOUGH2 input job:     1 lines read,    0.04 CPU-seconds used


 **********************************************************************************************************************************
                                                              OUTPUT
 **********************************************************************************************************************************


 SOLVE DIRECT PROBLEM                                        

 I  = NEW ITERATION        J  = JACOBIAN           S  = STEP      U  = UNSUCCESSFUL STEP
 PS = PARAMETER SELECTION  PU = PARAMETER UPDATE   B  = BOUNDS    M  = MESSAGE

 ----------------------------------------------------------------------------------------------------------------------------------
 ITER TOUGH2 OBJ FUNC. MAX. RESID. EQU.

 >>>>>  Forward run terminated at simulation time  8.64000000E+07 [sec] <<<<<


 ---   433rd iTOUGH2 run completed on  5-Jul-19  03:01 ---  CPU time used =       1.61 sec. :)
  

 ---     0 error(s) and  0 warning(s) detected
