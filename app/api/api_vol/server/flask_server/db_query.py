

class DBQuery():
    def __init__(self, session=None, model=None):
        if model and session:
            self.session = session
            self.model = model
        else:
            raise Exception('must have a valid session and ORM data model')
        
    def query(self):
        NotImplemented
    
    
class AgentQuery(DBQuery):
    def __init__(self, session=None, model=None):
        super().__init__(session=session, model=model)
        
    def query_floating_time_range(self, value, bufferLength):
        model = self.model
        queried_data = self.session.query(model).filter(model.vts < value+bufferLength).filter(model.vts >= value)
        res = {}
        for el in queried_data:
            pack = {'lon':el.vlon, 'lat':el.vlat, 'name':el.vname }
            # pack = [el.vname, el.vlon, el.vlat]
            if el.vts in res:
                res[el.vts].append(pack)
            else:
                res[el.vts] = [pack]
        return res