import os
import glob
import importlib
import numpy as np
from typing import Any, Callable, Dict, List, Optional, overload, Union
from PyExpUtils.utils.permute import set_at_path


@overload
def findExperiments(key: str, path: Optional[str] = None) -> Dict[str, Any]: ...
@overload
def findExperiments(path: Optional[str] = None) -> List[str]: ...

def findExperiments(key: Optional[str] = None, path: Optional[str] = None):
    if path is None:
        main_file = importlib.import_module('__main__').__file__
        path  = os.path.dirname(main_file)

    files = glob.glob(f'{path}/**/*.json', recursive=True)

    if key is None:
        return files

    out = {}
    kparts = key.split('/')
    for i, fname in enumerate(files):
        # remove the common experiment path leading up to here
        end = fname.replace(path, '')
        # if there is a nested structure, we might have a leading '/' now,
        # so for consistency, remove that
        if end.startswith('/'): end = end[1:]

        fparts = end.split('/')

        out_key = ''
        for kpart, fpart in zip(kparts, fparts):
            wrapped = kpart.startswith('{') and kpart.endswith('}')

            if not wrapped:
                continue

            if out_key == '':
                out_key = fpart

            else:
                out_key += f'.{fpart}'

        out_key += f'.[{i}]'
        set_at_path(out, out_key, fname)

    return out

def getCurveReducer(reducer: Union[str, Callable[[np.ndarray], float]]) -> Callable[[np.ndarray], float]:
    if reducer == 'auc':
        return np.mean

    if reducer == 'end':
        return lambda m: np.mean(m[-int(m.shape[0] * .1):])

    if isinstance(reducer, str):
        raise Exception("Unknown reducer type")

    return reducer
