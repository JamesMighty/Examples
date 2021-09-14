
from datetime import datetime
import json
from typing import Any, KeysView, Mapping, Union
import uuid
import pickle


class Datastore(dict):

    def __init__(self, payload:dict=None, create_meta:bool=True) -> None:
        if create_meta:
            meta = {
                "_created": datetime.utcnow().timestamp(),
                "_type": self.__class__.__name__
            }
            self.update(meta)
        if payload:
            self.update(payload)
    
    def __getitem__(self, k) -> Union['Datastore',Any]:
        if not k in self:
            super().__setitem__(k,Datastore())
            # print(f"implicitly created datastore for {k}")
        return super().__getitem__(k)
    
    def __str__(self) -> str:
        outp = None
        try:
            outp = json.dumps(self, indent=4)
        except Exception as e:
            outp = super().__str__()
        return outp

    def filter(self, names: list, white_list=True, show_private=False) -> 'Datastore':
        """[summary]\n
        filters out specified vars names based on whether act as whitelist/blacklist\n
        implicitly ignores private vars (starts with '_')\n
        """
        payload = {}
        for key in self:
            if key.startswith("_"):
                if show_private:
                    payload[key] = self[key]
            else:
                if white_list:
                    if key in names:
                        payload[key] = self[key]
                else:
                    if not key in names:
                        payload[key] = self[key]
        return Datastore(payload=payload, create_meta=False)
    
    def privates(self) -> 'Datastore':
        """[summary]
        returns all private vars (starts with '_')
        """
        payload = {}
        for key in self:
            if key.startswith("_"):
                payload[key] = self[key]
        return Datastore(payload=payload, create_meta=False)
    
    def publics(self) -> 'Datastore':
        """[summary]
        returns all public vars
        """
        payload = {}
        for key in self:
            if not key.startswith("_"):
                payload[key] = self[key]
        return Datastore(payload=payload, create_meta=False)
    
    def translate(self, names: dict) -> 'Datastore':
        """[summary]
        returns translated variable names into new names as declared by specified dict, not specified names are preserved
        """
        payload = {}
        for name in self:
            if name in names:
                payload[names[name]] = self[name]
            else:
                payload[name] = self[name]
        return Datastore(payload=payload, create_meta=False)
    
    def first(self) -> Any:
        """[summary]
        returns first item, if none return None
        Returns:
            Any: [description]
        """
        if len(self) > 0:
            return self[0]
        else:
            return None

class PointerDatastore(Datastore):

    def __init__(self, object: object, wrapper) -> None:
        super().__init__(create_meta=True)
        self._reference = object
        self._wrapper = wrapper
    
    @property
    def _dict(self):
        object_dict = self._reference.__dict__ if self._wrapper==None else self._wrapper(self._reference)
        whole_dict = object_dict.update(self)
        return whole_dict
    
    def __getitem__(self, k) -> Union['Datastore', Any]:
        if k in self._dict:
            return self._dict[k]
        else:
            return super().__getitem__(k)
    
    def keys(self) -> KeysView[Any]:
        return self._dict.keys()

    
    def __str__(self) -> str:
        _dict = self._reference.__dict__ if self._wrapper==None else self._wrapper(self._reference)
        try:
            return json.dumps(_dict, indent=4)
        except:
            return _dict.__str__()

class DatastoreProvider():

    def __init__(self) -> None:
        self._datastore = Datastore()
    
    @property
    def datastore(self) -> Datastore:
        return self._datastore

class DatastoreSubscriber():

    def __init__(self, provider: DatastoreProvider, id=str(uuid.uuid4())) -> None:
        self._provider = provider
        self.id = id
        self.datastore["_subtype"] = self.__class__.__name__
        self.datastore["_subbases"] = [_class.__name__ for _class in self.__class__.__bases__]
        self.datastore["_subfrom"] = datetime.utcnow().timestamp()

    @property
    def datastore(self) -> Datastore:
        return self._provider.datastore[self.id]

class DumpDatastore(Datastore):

    def __init__(self,file_path:str, payload: dict={}, create_meta: bool=True) -> None:
        super().__init__(payload=payload, create_meta=create_meta)
        self._file_path = file_path
    
    def dump(self):
        pickle.dump(self,self._file_path)
        

    