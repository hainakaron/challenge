#Note: 'The `entry` dictionary can contain groups (e.g. currency, country_code) that are not yet in the `stats`.')
def add_entry_to_stats(stats: dict, entry: dict) -> dict:
    entry['count'] = 1

    item_stat = {} #for new group items
    for key in stats:
        if type(stats[key]) == int:
            item_stat[key] = entry[key]
            stats[key] += entry[key]

    for key, val in entry.items():
        if key not in item_stat:
            stats[key] = obj_merge( stats[key], { val: item_stat} ) if key in stats else { val: item_stat}
    
    return stats

#Note: 'It has to support nested objects of any depth.'.
def merge_stats(*args: dict) -> dict:
    stats = {}
    for stat in args:
        stats = obj_merge(stats, stat)
    return stats

def obj_merge( stat1: dict, stat2: dict ) -> dict:
    for k, v in stat2.items():
        if ( k in stat1 ):
            temp = stat1[k]
            
            addable_types = (int, float)#, complex)
            
            if isinstance(temp, dict) and isinstance(v, dict): #dict + dict
                obj_merge(temp, v)
            elif type(temp) in addable_types and type(v) in (int, float): #numbers + numbers
                stat1[k] += v
            #additional cases
            elif isinstance(temp, list) and isinstance(v, list): #list + list
                for i in v:
                    if i not in temp: #assuming stats1[k] already have unique items
                        stat1[k] += v
            elif type(temp) != type(v):
                stat1[k] = v
        else:
            stat1[k] = v
    return stat1