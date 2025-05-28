def get_unit(l1: list) -> str:
    unit = None
    for element in l1:
        if 'MPH' in element:
            unit = 'MPH'
            break
        elif 'KMH' in element:
            unit = 'KMH'
            break
        
    if unit is None:
        unit = 'No unit has been found'
    return unit