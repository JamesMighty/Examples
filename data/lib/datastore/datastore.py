import json
import pickle
import uuid
from datetime import datetime
from typing import Any, Iterable, KeysView, Mapping, Union


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

        outp = json.dumps(self, indent=4)
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

class DatastoreProvider:

    def __init__(self, attr_name, payload={}) -> None:
        self._attr_name = attr_name
        self.datastore.update(payload)
    
    @property
    def datastore(self) -> Datastore:
        return self.__getattribute__(self._attr_name)

class DatastoreRootProvider(DatastoreProvider):

    def __init__(self, payload={}) -> None:
        self._datastore = Datastore()
        self.datastore.update(payload)
    
    @property
    def datastore(self) -> Datastore:
        return self._datastore

class DatastoreSubscriber():

    def __init__(self, id:str=None) -> None:
        if id:
            self.id = id
        else:
            self.id = str(uuid.uuid4())
        self._is_subscribed = False

    @property
    def is_subscribed(self) -> bool:
        return self._is_subscribed

    @property
    def datastore(self) -> Datastore:
        return self._provider.datastore[self.id]
    
    @property
    def parent_datastore(self) -> Datastore:
        return self._provider.datastore
    
    def subscribe(self, provider: DatastoreRootProvider, payload:Iterable={}):
        if not self.is_subscribed:
            self._provider = provider
            self.datastore["_subtype"] = self.__class__.__name__
            self.datastore["_subbases"] = [_class.__name__ for _class in self.__class__.__bases__]
            self.datastore["_subfrom"] = datetime.utcnow().timestamp()
            self._is_subscribed = True
            self.datastore.update(payload)
    
    def unsubscribe(self, pop_datastore=False):
        if self.is_subscribed:
            if pop_datastore:
                self._provider.datastore.pop(self.id)
            else:
                self.datastore.pop("_subtype")
                self.datastore.pop("_subbases")
                self.datastore.pop("_subfrom")
            self._provider = None
            self._is_subscribed = False


class DumpDatastore(Datastore):

    def __init__(self,file_path:str, payload: dict={}, create_meta: bool=True) -> None:
        super().__init__(payload=payload, create_meta=create_meta)
        self._file_path = file_path
    
    def dump(self):
        pickle.dump(self,self._file_path)
        

    