from sqlalchemy.orm import load_only


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
        
    def query_floating_time_range(self, time_value, buffer_length):
        model = self.model
        queried_data = self.session.query(model).filter(model.vts < time_value+buffer_length).filter(model.vts >= time_value)
        res = {}
        for el in queried_data:
            pack = {'lon':el.vlon, 'lat':el.vlat, 'name':el.vname }
            if el.vts in res:
                res[el.vts].append(pack)
            else:
                res[el.vts] = [pack]
        return res
    
    def query_emission_time_range(self, time_value, buffer_length, emission_ids = []):
        model = self.model
        queried_data = (self.session
                            .query(model)
                            .filter(model.vts < time_value+buffer_length)
                            .filter(model.vts >= time_value)
                            .with_entities(*[model.__dict__[col] for col in emission_ids]) # filter by columns in emission_ids list
                        )

        res = {}
    
        for el in queried_data:
            pack = {i:el.__getattribute__(i) for i in emission_ids}
            if el.vts in res:
                res[el.vts].append(pack)
            else:
                res[el.vts] = [pack]
        return res