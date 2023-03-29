#'The `entry` dictionary can contain groups (e.g. currency, country_code) that are not yet in the `stats`.')
def add_entry_to_stats(stats: dict, entry: dict) -> dict:
    stats['count'] += 1
    for key, val in entry.items(): #str, int
        prop = { 'count' : 1, 'amount' : entry['amount'], 'num_items' : entry['num_items']}

        if key in stats and isinstance(stats[key], int): #property
            stats[key] += val
        elif key in stats and isinstance(stats[key], dict): #group
            group_stat = stats[key][val]
            group_stat = dict_merge(group_stat, prop)
            stats[key][val] = group_stat
        else:
            stats[key] = { val : prop}
    return stats

#'It has to support nested objects of any depth.'
def merge_stats(*args: dict) -> dict:
    stats = {}
    for stat in args:
        stats = dict_merge(stats, stat)
    return stats

#recursive function
def dict_merge( stat1, stat2 ):
    for k, v in stat2.items():
        if (k in stat1 and isinstance(stat1[k], dict) and isinstance(v, dict)):  #noqa
            dict_merge(stat1[k], v)
        elif (k in stat1 and isinstance(stat1[k], int) and isinstance(v, int)):
            stat1[k] += v
        else:
            stat1[k] = v
    return stat1

