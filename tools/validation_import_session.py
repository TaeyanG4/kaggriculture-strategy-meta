"""Per-invocation reuse of validated immutable import provenance.

The original importer and bounded validator stay byte-identical. Each distinct
file is hashed, each ancestor is fully validated, and all file hashes are checked
again before a seal or database write. Only repeated work within this invocation
is reused; nothing is trusted across processes or after metadata changes.
"""
import copy
import sys
from pathlib import Path


class ValidationSession:
    def __init__(self):
        from tools import import_validation_league as bulk
        from tools import bounded_validation_import as bounded
        self.bulk,self.bounded=bulk,bounded
        self.original_digest=bulk.digest
        self.original_checked=bounded.checked_bounded
        self.original_atomic=bulk.atomic_json
        self.original_prepare=bulk.prepare_readonly
        self.files={};self.campaigns={};self.digest_hits=0;self.campaign_hits=0

    @staticmethod
    def signature(path):
        s=path.stat()
        return (s.st_dev,s.st_ino,s.st_size,s.st_mtime_ns,s.st_ctime_ns)

    def digest(self,path):
        p=Path(path).resolve();sig=self.signature(p)
        if p in self.files:
            before,value=self.files[p]
            self.bulk.require(sig==before,'File changed during import: '+str(p))
            self.digest_hits+=1;return value
        value=self.original_digest(p)
        self.bulk.require(self.signature(p)==sig,'File changed while hashing: '+str(p))
        self.files[p]=(sig,value);return value

    def verify_all(self):
        # Recompute every unique hash before allowing persistent mutation.
        for p,(sig,value) in self.files.items():
            self.bulk.require(self.signature(p)==sig,'File changed during import: '+str(p))
            self.bulk.require(self.original_digest(p)==value,'File hash changed during import: '+str(p))
            self.bulk.require(self.signature(p)==sig,'File changed while rechecking: '+str(p))

    def checked(self,path,ancestors=()):
        p=Path(path).resolve()
        self.bulk.require(p not in ancestors,'Cyclic bounded cache provenance')
        if p in self.campaigns:
            self.campaign_hits+=1
            return copy.deepcopy(self.campaigns[p])
        result=self.original_checked(p,ancestors=ancestors)
        self.campaigns[p]=copy.deepcopy(result)
        return result

    def atomic(self,path,value):
        # Sealing and writing receipts must use a still-valid frozen snapshot.
        self.verify_all()
        return self.original_atomic(path,value)

    def prepare(self,*args,**kwargs):
        result=self.original_prepare(*args,**kwargs)
        self.verify_all()
        return result

    def __enter__(self):
        self.old_alias=sys.modules.get('bounded_validation_import')
        sys.modules['bounded_validation_import']=self.bounded
        self.bulk.digest=self.digest;self.bounded.checked_bounded=self.checked
        self.bulk.atomic_json=self.atomic;self.bulk.prepare_readonly=self.prepare
        return self

    def __exit__(self,*args):
        self.bulk.digest=self.original_digest;self.bounded.checked_bounded=self.original_checked
        self.bulk.atomic_json=self.original_atomic;self.bulk.prepare_readonly=self.original_prepare
        if self.old_alias is None:sys.modules.pop('bounded_validation_import',None)
        else:sys.modules['bounded_validation_import']=self.old_alias

