def spn_value(json_response):
    toponym = json_response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]
    toponym_size = (toponym["boundedBy"]["Envelope"]["lowerCorner"], toponym["boundedBy"]["Envelope"]["upperCorner"])
    low, up = toponym_size[0].split(" "), toponym_size[1].split(" ")
    delta = str(abs(float(up[0]) - float(low[0])))
    return ",".join([delta, delta])