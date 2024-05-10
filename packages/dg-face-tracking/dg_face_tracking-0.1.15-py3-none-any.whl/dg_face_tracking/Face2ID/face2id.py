import degirum as dg
import numpy as np
import json

from typing import Union

from pathlib import Path
Path(__file__).resolve()

from .face2id_proc import Face2ID_Proc, unknown, error, docker_path2db


# Global Face to ID processing instance
gl_proc: Union[Face2ID_Proc, None] = None


def result2json(result: str):
    label, err_msg = (result, "") if error not in result else ("", result)
    return json.dumps({"label": label, "error": err_msg})


def face2id(img: Union[str, np.ndarray],
            deployment: str = "docker",
            async_support: bool = False,
            path2db: str = docker_path2db,
            target: str = None,
            verbose: bool = False) -> str:
    """
    Face image to Person ID
    img : str or ndarray: face image as base64 encoded png or numpy array
    deployment: ["cloud", "local", "docker"]
    async_support: bool: do we need to enable async support
    path2db: str: path to face embeddings database
    target: target label, if available, for db training
    verbose: bool: for testing purpose only
    return: json '{"label": "<some label or empty string>", "error": "<error message or empty string>"}'.
    """
    global gl_proc

    if img is None:
        return result2json(f"{error}: nNone image is passed to face2id processor")

    if gl_proc is None:
        # instantiate processor
        try:
            gl_proc = Face2ID_Proc(deployment=deployment, async_support=async_support, path2db=path2db, verbose=verbose)
        except Exception as e:
            return result2json(f"{error}: unable to create face2id processor: {str(e)}")

    try:
        # identify the face image
        label = gl_proc.face2id(img, target=target)
        return result2json(label)
    except Exception as e:
        gl_proc.stop()
        gl_proc = None
        return result2json(f"{error}: unresolved exception {str(e)}")


def face2id_reset(deployment: str = "docker",
                  path2db: str = docker_path2db):
    """
    Reset face embeddings database to default state. If default is not available, set an empty db
    deployment: ["cloud", "local", "docker"]
    path2db: str: path to face embeddings database
    """
    global gl_proc
    if gl_proc is None:
        try:
            gl_proc = Face2ID_Proc(deployment=deployment, path2db=path2db)
        except Exception as e:
            return json.dumps({"success": False})

    if gl_proc.reset_db():
        return json.dumps({"success": True})
    else:
        return json.dumps({"success": False})


def face2id_info():
    global gl_proc
    if gl_proc is not None:
        info = gl_proc.get_info()
        if isinstance(info, dict):
            return json.dumps(info)
        else:
            return json.dumps({"face2id_info": "wrong info format" })
    else:
        return json.dumps({"face2id_info": "processor is not loaded" })


def face2id_stop():
    """
    Stop Face image to Person processing instance and dump embeddings db
    """
    global gl_proc

    if gl_proc is not None:
        gl_proc.stop()
        gl_proc = None


