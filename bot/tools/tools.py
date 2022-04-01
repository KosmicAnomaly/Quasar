# https://gist.github.com/RobertSudwarts/acf8df23a16afdb5837f?permalink_comment_id=3070256#gistcomment-3070256
def degree_to_cardinal(degrees: float):
    directions = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE",
                  "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    compass = round(degrees / (360.0 / 16))
    return directions[compass % 16]
