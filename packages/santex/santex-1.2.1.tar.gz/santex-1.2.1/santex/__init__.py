import importlib

class ImportSantex:
    @property
    def Material(self):
        from santex.material.material import Material
        return Material

    @property
    def EBSD(self):
        from santex.ebsd.ebsd import EBSD
        return EBSD

    @property
    def Tensor(self):
        from santex.tensor.tensor import Tensor
        return Tensor

    @property
    def Anisotropy(self):
        from santex.anisotropy.anisotropy import Anisotropy
        return Anisotropy

    @property
    def Isotropy(self):
        from santex.isotropy.isotropy import Isotropy
        return Isotropy

_lazy_loader = ImportSantex()

def __getattr__(name):
    try:
        return getattr(_lazy_loader, name)
    except AttributeError:
        raise AttributeError(f"module 'santex' has no attribute '{name}'")
