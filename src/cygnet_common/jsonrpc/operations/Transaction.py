from cygnet_common.Structures import BaseDict
from cygnet_common.jsonrpc.helpers.Switch import OVSwitch
from cygnet_common.jsonrpc.helpers.Port import OVSPort
from cygnet_common.jsonrpc.helpers.Bridge import OVSBridge
from cygnet_common.jsonrpc.helpers.Interface import OVSInterface

class Transaction(BaseDict):


    def __init__(self, op, timeout=0):
        self._instance = None
        self['op'] = op
        self['timeout'] = timeout
        return


    @property
    def instance(self):
        return self._instance

    @instance.setter
    def instance(self, value):
        assert type(value) in [OVSwitch, OVSBridge, OVSPort, OVSInterface]
        self._instance = value


class WaitTransaction(Transaction):

    def __init__(self, instance, timeout=0):
        super(WaitTransaction, self).__init__('wait', timeout)
        self.instance = instance
        self['rows'] = list()
        self['columns'] = list()
        self['until'] = '=='
        self['where'] = list()
        self['table'] = None

    @table.setter
    def table(self, instance_type):
        self['table'] = {
                OVSPort:'Port',
                OVSBridge:'Bridge',
                OVSwitch: 'Open_vSwitch'
                }[instance_type]

    @instance.setter
    def instance(self, value):
        assert type(value) in [OVSwitch, OVSBridge, OVSPort]
        self.table = type(value)
        uuid_row = {
                OVSPort:'interfaces',
                OVSBridge:'ports',
                OVSwitch:'bridges'
                }[type(value)]
        self.rows = {uuid_row:value.getattr(uuid_row)}
        target = ['uuid', value.uuid]
        condition = ['_uuid','==',target]
        self['where'].append(condition)

    @rows.setter
    def rows(self, row_dict):
        '''
        Since Instance is always either Port, Bridge, Switch
        The row_value is always going to be a dict holding
        uuids of its network substances and itself.
        '''
        self['rows'] = list()
        for row_name, row_value in row_dict.iteritems():
            row = dict()
            row[row_name] = list()
            [row[row_name].extend(["uuid",uuid]) for uuid in row_value.iterkeys()]
            self['rows'].append(row)
