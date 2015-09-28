
class OVSwitch(object):

    def __init__(self, state, uuid, switch_dict):
        assert type(uuid) in [unicode,str]
        assert type(switch_dict) is dict
        assert len(switch_dict) > 0

        self.uuid = uuid
        self.bridges = dict()
        for state, columns in switch_dict.iteritems():
            if state == 'new':
                for column, value in columns.iteritems():
                    if column == 'bridges':
                        bridges = []
                        [bridges.extend(val) for val in value[1]]
                        bridges = [bridge for bridge in bridges if bride != 'uuid']
                    elif type(value) is in [list, tuple] and value[0] == 'set':
                        state[column] = value[1]
                    else:
                        state[column] = value
        for bridge in bridges:
            self.bridges[bridge] = state.bridges[bridge]
