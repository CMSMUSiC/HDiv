from get_event_classes import get_event_classes

with open('puplication_eventclasses.py', 'w') as f:

    event_classes, SF_InvMass, SF_SumPt, SF_MET = get_event_classes("/disk1/ykaiser/sharing/Lucas/bg.root","/disk1/ykaiser/sharing/Lucas/bg_2000.root")
    event_classes = list(event_classes)
    #print(event_classes)
    #for i in range(len(SF_InvMass)):
    #     print("Event " + str(i) + ":" + str(event_classes[i]))
    #     print("\t Signal fraction for InvMass:" + str(SF_InvMass[i])) 
    #     print("\t Signal fraction for SumPt:" + str(SF_SumPt[i])) 
    #     print("\t Signal fraction for MET:" + str(SF_MET[i])) 
    f.write('event_classes = ' + str(event_classes) + "\n")
    f.write('SF_InvMass = ' + str(SF_InvMass)+ "\n")
    f.write('SF_SumPt = ' + str(SF_SumPt)+ "\n")
    f.write('SF_MET = ' + str(SF_MET)+ "\n")


