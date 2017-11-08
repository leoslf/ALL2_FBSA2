import os

def __import_pkgfiles():
    """Dynamically import all the public attributes of the python modules in the current directory. Returns a list of names."""
    ret = []
    _globals, _locals, = globals(), locals()
    pkg_path = os.path.dirname(__file__)
    pkg_name = os.path.basename(pkg_path)

    for filename in os.listdir(pkg_path):
        module_name, extension = os.path.splitext(filename)
        if module_name[0] != "_" and extension in (".py", "pyw"):
            subpkg = "{}.{}".format(pkg_name, module_name) # pkg relative
            module = __import__(subpkg, _globals, _locals, [module_name])
            mod_dict = module.__dict__
            names = (mod_dict["__all__"] if "__all__" in mod_dict else
                    [name for name in mod_dict if name[0] != '_']) # public
            ret.extend(names)
            _globals.update((name, mod_dict[name]) for name in names)

    return ret


if __name__  != "__main__":
    __all__ = ["__all__"] + __import_pkgfiles() # "__all__" in __all__
