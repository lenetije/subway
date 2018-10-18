from pprint import pprint

def subway(**lines):
    """Define a subway map. Input is subway(linename='station1 station2...'...).
    Convert that and return a dict of the form: {station:{neighbor:line,...},...}"""
    subway_map = {}
    for line,stations_string in lines.items():
        stations_list = stations_string.split(" ")
        for station in stations_list:
            if station not in subway_map:
                subway_map[station] = entry = {}
                if stations_list.index(station) != 0:
                    entry[stations_list[stations_list.index(station)-1]] = line
                if stations_list.index(station) < len(stations_list)-1:
                    entry[stations_list[stations_list.index(station)+1]] = line
            else:
                partial_value = subway_map.pop(station)
                if stations_list.index(station) != 0:
                    partial_value[stations_list[stations_list.index(station)-1]] = line
                if stations_list.index(station) < len(stations_list)-1:
                    partial_value[stations_list[stations_list.index(station)+1]] = line
                subway_map[station] = partial_value


    return subway_map

boston = subway(
    blue='bowdoin government state aquarium maverick airport suffolk revere wonderland',
    orange='oakgrove sullivan haymarket state downtown chinatown tufts backbay foresthills',
    green='lechmere science north haymarket government park copley kenmore newton riverside',
    red='alewife davis porter harvard central mit charles park downtown south umass mattapan')


def subway_successors(station, system=boston):
    """It takes the here variable and stores pairs of state/action.
    Every state is one of the stations currenty stored in the boston dictionary under the here key.
    Every action is the corresponding line."""
    return system[station]

def ride(here, there, system=boston):
    "Return a path on the subway system from here to there."
    return shortest_path_search(here, subway_successors, there)

def longest_ride(system):
    """"Return the longest possible 'shortest path'
    ride between any two stops in the system."""
    longest = []
    stations = system.keys()
    for here in stations:
        for there in stations:
            path = shortest_path_search(here, subway_successors, there)
            if len(path) > len(longest):
                longest = path
            else:
                pass
    return longest


def shortest_path_search(start, successors, goal):
    """Find the shortest path from start state to a state
    such that is_goal(state) is true."""
    if goal == start:
        return [start]
    explored = set() # set of states we have visited
    frontier = [ [start] ] # ordered list of paths we have blazed
    while frontier:
        path = frontier.pop(0)
        s = path[-1]
        for (state, action) in successors(s).items():
            if state not in explored:
                explored.add(state)
                path2 = path + [action, state]
                if goal == state:
                    return path2
                else:
                    frontier.append(path2)
    return []


def path_states(path):
    "Return a list of states in this path."
    return path[0::2]

def path_actions(path):
    "Return a list of actions in this path."
    return path[1::2]

def test_ride():
    assert ride('mit', 'government') == [
        'mit', 'red', 'charles', 'red', 'park', 'green', 'government']
    assert ride('mattapan', 'foresthills') == [
        'mattapan', 'red', 'umass', 'red', 'south', 'red', 'downtown',
        'orange', 'chinatown', 'orange', 'tufts', 'orange', 'backbay', 'orange', 'foresthills']
    assert ride('newton', 'alewife') == [
        'newton', 'green', 'kenmore', 'green', 'copley', 'green', 'park', 'red', 'charles', 'red',
        'mit', 'red', 'central', 'red', 'harvard', 'red', 'porter', 'red', 'davis', 'red', 'alewife']
    assert (path_states(longest_ride(boston)) == [
        'wonderland', 'revere', 'suffolk', 'airport', 'maverick', 'aquarium', 'state', 'downtown', 'park',
        'charles', 'mit', 'central', 'harvard', 'porter', 'davis', 'alewife'] or
        path_states(longest_ride(boston)) == [
                'alewife', 'davis', 'porter', 'harvard', 'central', 'mit', 'charles',
                'park', 'downtown', 'state', 'aquarium', 'maverick', 'airport', 'suffolk', 'revere', 'wonderland'])
    assert len(path_states(longest_ride(boston))) == 16
    return 'test_ride passes'

print test_ride()
print longest_ride(boston)
