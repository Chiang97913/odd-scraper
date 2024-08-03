
def parse_part(part):
    attributes = part.split(';')
    part_dict = {}
    for attribute in attributes:
        if '=' in attribute:
            key, value = attribute.split('=',1)
            part_dict[key.strip()] = value.strip()
    return part_dict

def convert_to_dict(input_string):
    parts = input_string.split('|')
    main_dict = {'MG': []}
    current_mg = None
    current_ma = None
    for part in parts:
        if not part.strip():
            continue
        if part.startswith("CL;"):
            main_dict['CL']=parse_part(part[3:])
        if part.startswith("EV;"):
            main_dict['EV']=parse_part(part[3:])
        if part.startswith('MG;'):
            current_mg = parse_part(part[3:])
            current_mg['MA'] = []
            main_dict['MG'].append(current_mg)
            current_ma = None  # Reset current MA
        elif part.startswith('MA;'):
            if current_mg is not None:
                current_ma = parse_part(part[3:])
                current_ma['PA'] = []
                current_mg['MA'].append(current_ma)
        elif part.startswith('PA;'):
            if current_ma is not None:
                current_ma['PA'].append(parse_part(part[3:]))
    return main_dict
