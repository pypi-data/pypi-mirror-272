from typing import Protocol
import hashlib


class GenerateUniqueIdProtocol(Protocol):
    def run(self, function_src: str) -> str: ...


class GenerateUniqueId(GenerateUniqueIdProtocol):
    def run(self, function_src):
        m = hashlib.md5()
        m.update(function_src.encode())
        return str(int(m.hexdigest(), 16))[0:32]
