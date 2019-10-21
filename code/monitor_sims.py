# A module to show progress of simulations running in the background

import os
import sys
import time

#locate log files
event_name = sys.argv[1]
agn_log_file = '../events/%s/logs/sim_agn.log' %event_name
kn_log_file = '../events/%s/logs/sim_kn.log' %event_name
ia_log_file = '../events/%s/logs/sim_ia.log' %event_name
cc_log_file = '../events/%s/logs/sim_cc.log' %event_name

#determine which sims are being run
agn_running = True if 'agn' in sys.argv else False
ia_running = True if 'ia' in sys.argv else False
cc_running = True if 'cc' in sys.argv else False
kn_running = True if 'kn' in sys.argv else False

#start monitoring
running = agn_running or kn_running or ia_running or cc_running
agn_phase1, agn_phase2, agn_phase3 = True, False, False
kn_phase1, kn_phase2, kn_phase3, kn_phase4 = True, False, False, False
ia_phase1, ia_phase2, ia_phase3 = True, False, False
cc_phase1, cc_phase2, cc_phase3 = True, False, False

#let the sims get started
time.sleep(5)

while running:

    """
    AGN Progress Tracking
    """
    if agn_running:
        agn_log = open(agn_log_file, 'r')
        agn_info = agn_log.readlines()

        #check for errors and exit the loop if necessary
        for line in agn_info[-30:]:
            if line.find('FATAL') != -1:
                print("WARNING: ERROR found in sim_agn.log")
                agn_running = False

        last_line = agn_info[-1]
        agn_log.close()

        if agn_phase3 or (not agn_phase1 and last_line.find('Finished writing') == -1):
            agn_phase1 = False
            agn_phase2 = False
            agn_phase3 = True
            agn_running = False ## it should finish up in time where this is okay
            agn_progress = 'Finishing'
        elif agn_phase2 or last_line.find('Finished writing') != -1:
            agn_phase1 = False
            agn_phase2 = True
            info = [x for x in last_line.split(' ') if x != '' and x != '\t' and x != '\n']
            total = info[4]
            completed = info[2]
            agn_progress = '%.2f %%' % (float(completed) / float(total) * 100.0)
        elif agn_phase1 == True:
            agn_progress = 'Initializing'
        else:
            print("\nNot sure how we got here, last status was:")
            print("\tPhase1: %i, Phase2: %i, Phase3: %i" %(int(agn_phase1), int(agn_phase2), int(agn_phase3)))
            print("\tLast line: %s" %last_line)
            agn_running = False
    else:
        agn_progress = 'Done!'
            
            
    """
    Ia Progress Tracking
    """
    if ia_running:
        ia_log = open(ia_log_file, 'r')
        ia_info = ia_log.readlines()

        #check for errors and exit the loop if necessary
        for line in ia_info[-30:]:
            if line.find('FATAL') != -1:
                print("WARNING: ERROR found in sim_ia.log")
                ia_running = False

        last_line = ia_info[-1]
        ia_log.close()

        if ia_phase3 or (not ia_phase1 and last_line.find('Finished generating') == -1):
            ia_phase1 = False
            ia_phase2 = False
            ia_phase3 = True
            ia_running = False ## it should finish up in time where this is okay
            ia_progress = 'Finishing'
        elif ia_phase2 or last_line.find('Finished generating') != -1:
            ia_phase1 = False
            ia_phase2 = True
            info = [x for x in last_line.split(' ') if x != '' and x != '\t' and x != '\n']
            total = info[4]
            completed = info[2]
            ia_progress = '%.2f %%' % (float(completed) / float(total) * 100.0)
        elif ia_phase1 == True:
            ia_progress = 'Initializing'
        else:
            print("\nNot sure how we got here, last status was:")
            print("\tPhase1: %i, Phase2: %i, Phase3: %i" %(int(ia_phase1), int(ia_phase2), int(ia_phase3)))
            print("\tLast line: %s" %last_line)
            ia_running = False
    else:
        ia_progress = 'Done!'

    """
    CC Progress Tracking
    """
    if cc_running:
        cc_log = open(cc_log_file, 'r')
        cc_info = cc_log.readlines()

        #check for errors and exit the loop if necessary
        for line in cc_info[-30:]:
            if line.find('FATAL') != -1:
                print("WARNING: ERROR found in sim_cc.log")
                cc_running = False

        ####last_line must pick the final 'Finished generating' line
        last_lines = cc_info[-70:]
        last_lines.reverse()
        found_last_line = False
        for line in last_lines:
            if line.find('Finished generating') != -1:
                last_line = line
                found_last_line = True
                break
        if not found_last_line:
            last_line = last_lines[0]
        cc_log.close()

        if cc_phase3 or (not cc_phase1 and last_line.find('Finished generating') == -1):
            cc_phase1 = False
            cc_phase2 = False
            cc_phase3 = True
            cc_running = False ## it should finish up in time where this is okay
            cc_progress = 'Finishing'
        elif cc_phase2 or last_line.find('Finished generating') != -1:
            cc_phase1 = False
            cc_phase2 = True
            info = [x for x in last_line.split(' ') if x != '' and x != '\t' and x != '\n']
            total = info[4]
            completed = info[2]
            cc_progress = '%.2f %%' % (float(completed) / float(total) * 100.0)
        elif ia_phase1 == True:
            cc_progress = 'Initializing'
        else:
            print("\nNot sure how we got here, last status was:")
            print("\tPhase1: %i, Phase2: %i, Phase3: %i" %(int(cc_phase1), int(cc_phase2), int(cc_phase3)))
            print("\tLast line: %s" %last_line)
            cc_running = False
    else:
        cc_progress = 'Done!'
    
            
    """
    KN Progress Tracking
    """
    if kn_running:
        kn_log = open(kn_log_file, 'r')
        kn_info = kn_log.readlines()

        #check for errors and exit the loop if necessary
        for line in kn_info[-30:]:
            if line.find('FATAL') != -1:
                print("WARNING: ERROR found in sim_kn.log")
                kn_running = False

        last_lines = kn_info[-10:]
        last_lines.reverse()
        found_last_line = False
        for line in last_lines:
            if line.find('Finished writing') != -1 or line.find('Read  (ised=') != -1:
                last_line = line
                found_last_line = True
                break
        if not found_last_line:
            last_line = last_lines[0]
        
        #last_line = kn_info[-2]
        kn_log.close()
        
        if kn_phase4 or (not kn_phase1 and not kn_phase2 and last_line.find('Finished writing') == -1):
            kn_phase1 = False
            kn_phase2 = False
            kn_phase3 = False
            kn_phase4 = True
            kn_running = False ## it should finish up in time where this is okay
            kn_progress = 'Finishing'
        elif kn_phase3 or last_line.find('Finished writing') != -1:
            kn_phase1 = False
            kn_phase2 = False
            kn_phase3 = True
            info = [x for x in last_line.split(' ') if x != '' and x != '\t' and x != '\n']
            total = info[4]
            completed = info[2]
            kn_progress = '%.2f %%' % (float(completed) / float(total) * 20.0 + 80.0)
        elif kn_phase2 or last_line.find('Read  (ised=') != -1:
            kn_phase1 = False
            kn_phase2 = True
            info = [x for x in last_line.split(' ') if x != '' and x != '\t' and x != '\n'][1]
            more_info = info.split('=')[-1].split(')')[0].split('/')
            total = more_info[1]
            completed = more_info[0]
            kn_progress = '%.2f %%' % (float(completed) / float(total) * 80.0)
        elif kn_phase1 == True:
            kn_progress = 'Initializing'
        else:
            print("\nNot sure how we got here, last status was:")
            print("\tPhase1: %i, Phase2: %i, Phase3: %i, Phase4: %i" %(int(kn_phase1), int(kn_phase2), int(kn_phase3), int(kn_phase4)))
            print("\tLast line: %s" %last_line)
            kn_running = False
    else:
        kn_progress = 'Done!'

            
    #output progress
    progress = 'Simulating:  AGN -- %s | KN -- %s | Ia -- %s | CC -- %s |                          ' %(agn_progress, kn_progress, ia_progress, cc_progress)
    sys.stdout.write('\r%s' %progress)
    sys.stdout.flush()

    running = agn_running or kn_running or ia_running or cc_running
    time.sleep(2)
    
sys.stdout.write('\rSimulating:  AGN -- Done! | KN -- Done! |  Ia -- Done!  |  CC -- Done!  |                         \n')
sys.stdout.flush()
