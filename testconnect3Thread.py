def getAllMsg(master,stop):
    while stop.empty():
        try:
            #ESC_TELEMETRY manda informazioni solo quando il motore e' armato.
            message = master.recv_match(type='ESC_TELEMETRY_1_TO_4').to_dict()
            print("rpm motor 4: %s" % message['rpm'][3])
        except:
            pass