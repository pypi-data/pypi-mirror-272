# Copyright (c) 2024 구FS, all rights reserved. Subject to the MIT licence in `licence.md`.
LENGTH={        # m
    "ft": 0.3048,
    "in": 0.0254,
    "NM": 1852,
    "SM": 1609.344,
    "yd": 0.9144
}

AREA={          # m²
    "ft²": LENGTH["ft"]**2,
    "ha": 100**2,
    "in²": LENGTH["in"]**2,
    "SM²": LENGTH["SM"]**2
}

VOLUME={        # m³
    "ft³": LENGTH["ft"]**3,
    "gal": 0.003785411784,
    "in³": LENGTH["in"]**3,
    "l": 0.001,
    "qt": 0.003785411784/4
}

TIME={          # s
    "d": 86400,
    "h": 3600,
    "min": 60,
    "week": 7*86400,
    "year": 365.2425*86400
}

SPEED={         # m/s
    "c": 299792458,
    "ft/min": LENGTH["ft"]/TIME["min"],
    "ft/s": LENGTH["ft"]/1,
    "km/h": 1000/TIME["h"],
    "SM/h": LENGTH["SM"]/TIME["h"],
    "kt": LENGTH["NM"]/TIME["h"]
}

ACCELERATION={  # m/s²
    "g": 9.80665,
    "kt/s": SPEED["kt"]/1
}

FLOW={          # m³/s
    "gal/h": VOLUME["gal"]/TIME["h"],
    "l/h": VOLUME["l"]/TIME["h"]
}

MASS={          # kg
    "lb": 0.45359237,
    "oz": 0.028349523125,
    "st": 14*0.45359237
}

DENSITY={       # kg/m³
    "g/cm³": 1000
}
    
FORCE={         # kg*m/s² or N
    "kgf": 1*ACCELERATION["g"],
    "lbf": MASS["lb"]*ACCELERATION["g"]
}

PRESSURE={      # kg/(m*s²) or Pa
    "atm": 101325,
    "bar": 100000,
    "inHg": 3386.389,
    "lbf/ft²": FORCE["lbf"]/AREA["ft²"],
    "lbf/in²": FORCE["lbf"]/AREA["in²"],
    "mmHg": 133.322387415
}

ENERGY={        # kg*m²/s² or J
    "cal": 4.184,
    "hp*h": 75*ACCELERATION["g"]*TIME["h"],
    "W*h": 1*TIME["h"]
}

TORQUE={        # kg*m²/s² or Nm
    "kgf*m": 1*ACCELERATION["g"]*1,
    "lbf*in": MASS["lb"]*ACCELERATION["g"]*LENGTH["in"]
}

POWER={         # kg*m²/s³ or W
    "hp": 550*LENGTH["ft"]*MASS["lb"]*ACCELERATION["g"]/1,
    "ps": 75*1*ACCELERATION["g"]*1/1,
}