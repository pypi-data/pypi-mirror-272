from .ezalpy import System
from .ezalpy import Download
from .ezalpy import Manipulate

_beta_class = []
__all__ = ['System', 'Download', 'Manipulate']

def include_beta(class_name):
    """Include a Beta Class, look for this in the albeta.py
    
    Example: include_beta('example')
    """
    global _beta_class

    try:
        module = __import__('ezalpybeta', fromlist=[class_name])
        class_object = getattr(module, class_name)

        globals()[class_name] = class_object

        __all__.append(class_name)
        _beta_class.append(class_name)
    except ImportError:
        print(f"Beta Class {class_name}, doesn`t exist and can`t import.")