def spn_value(point1, point2):
    delta = str(abs(float(point2) - float(point1)))
    return ",".join([delta, delta])