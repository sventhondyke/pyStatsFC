#!/usr/bin/python2.7
from operator import itemgetter
import httplib2, urllib, json, time, string, copy
from datetime import date, timedelta

__KEY__ = 'free' # obviously chnage this is you have a paid API key

class Struct:
    ''' Structure object for data items. '''
    def __init__(self, **entries): 
        self.__dict__.update(entries)
    def __repr__(self): return '%s\n------ *** ------' % str('\n'.join('%s : %s' % (k, repr(v)) for (k, v) in self.__dict__.iteritems()))
    
class SFCError(Exception):
    ''' Some branded errors. '''
    pass

class StatsFC(object):
    ''' StatsFC base object. '''
    def __init__(self, competition, data, limit=''):
        self.base_url = "http://api.statsfc.com/{0}/{1}.json?key={2}&{3}".format(competition, data, __KEY__, urllib.urlencode({'limit':limit}))
        self.headers = {'Content-type': 'application/json;charset=utf-8', 'Accept-Encoding': 'compress, gzip'}
        
    def request(self, additional_params={}, maximimum_retries=10):
        success = False
        retries = 0
        while not success and retries < maximimum_retries:                          
            http = httplib2.Http()
            request_url = self.base_url + '&' + urllib.urlencode(additional_params)
            self.http_headers, response = http.request(request_url, headers=self.headers)
            if self.http_headers['status'] == '403':
                try:
                    retry_after = self.http_headers['retry_after']
                    time.sleep(retry_after)
                    retries =+ 1
                except KeyError :
                    pass
            elif self.http_headers['status'] == '200':
                success = True                                        
                self.response = json.loads(response)
                if 'error' in self.response:
                    raise SFCError(self.response['error'])
            else:
                raise SFCError(self.http_headers['status'])
            
class Table(StatsFC):
    ''' Table object '''
    def __init__(self, competition):
        super(Table, self).__init__(competition, 'table')
        self.request()
        self.rows = [Struct(**data) for data in self.response]
    
    def __iter__(self):
        return iter(self.rows)
    
    def __getitem__(self,i):
        return sorted(self.rows, key=itemgetter('position'))[i]
    
    def position(self, pos):
        ''' allows reference of one-based position in table '''
        if (pos < 1) or (pos > len(self.rows)):
            raise SFCError("Position {pos} is out of the range of 1-{num_teams}".format(pos=pos, num_teams=len(self.rows)))
        else:
            return self.rows[pos-1]
        
class Matches(StatsFC):
    ''' Fixtures or Results object. 
    
    date_from & date_to need to be either datetime.date objects or 'yyyy-mm-dd' strings
    
    '''
    def __init__(self, competition, type, **kwargs):
        super(Matches, self).__init__(competition, type, limit=kwargs.get('limit',''))     
        self.from_date = kwargs.get('date_from',date.today())
        self.to_date = kwargs.get('date_to',date.today()+timedelta(days=365))
        self.team = kwargs.get('team','')
        self.request(additional_params={'from':self.from_date, 'to':self.to_date, 'team':self.team})
        self.items = [Struct(**data) for data in self.response]
        
    def __iter__(self):
        return iter(self.items)      

class Live(StatsFC):
    ''' Live Matches object. '''
    def __init__(self, competition, **kwargs):
        super(Live, self).__init__(competition, 'live', limit=kwargs.get('limit',''))     
        self.team = kwargs.get('team','')
        self.request(additional_params={'team':self.team})
        self.items = [Struct(**data) for data in self.response]
        
    def __iter__(self):
        return iter(self.items)            
        
class Form(StatsFC):
    ''' Form object. '''
    def __init__(self, competition, **kwargs):
        super(Form, self).__init__(competition, 'form')     
        self.request()
        self.items = [Struct(**data) for data in self.response]
        
    def __iter__(self):
        return iter(self.items)

class TopScorers(StatsFC):
    ''' Top Scorers object. '''
    def __init__(self, competition, **kwargs):
        super(TopScorers, self).__init__(competition, 'top-scorers')     
        self.request()
        self.items = [Struct(**data) for data in self.response]
        
    def __iter__(self):
        return iter(self.items)


    