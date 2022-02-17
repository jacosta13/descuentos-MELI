import pandas as pd
import numpy as np 

import constants

import json

import requests

import os

import time


def nested_get(key: str, obj: dict):
    """
    Funcion para acceder a valores en diccionarios anidados.
    :param key: String con las llaves a seguir hasta el valor separadas por
        puntos.
    :param obj: Diccionario, String.
    :return: Valor en Diccionario.
    """
    try:
        current = obj
        for k in key.split("."):
            current = current[k]
            
        return current
    except (KeyError, ValueError, TypeError):
        
        return None
    
    
def direct_values_extraction(obj: dict, list_keys=constants.KEYS_DIRECT_VALUES):
    """
    Funcion para acceder a valores de llaves principales en el diccionario.
    :param list_keys: Lista de Strings con las llaves a seguir hasta el valor.
    :param obj: Diccionario, Lista.
    :return: DataFrame.
    """
    df = pd.DataFrame(
        columns=list_keys
    )
    
    for x in list_keys:
        value = nested_get(
            key=x, 
            obj=obj
        )
        
        df[x]=[value]
        
    return df


def keys_large_construction(obj=constants.KEYS_JSON_TYPES):
    """
    Funcion para construir las rutas de los sub json.
    :param list_keys: Diccionario donde sus llaves corresponden a las llaves
        de los subjson y como valor, el listado de llaves del sub json. 
    :param obj: Diccionario.
    :return: Lista.
    """   
    keys_large = []
    
    for key in obj.keys():
        for value in obj[key]:
            keys_large.append(key+"."+value)

    return keys_large


KEYS_LARGE = keys_large_construction(
    obj=constants.KEYS_JSON_TYPES
)

def sub_json_extraction(obj:dict, list_keys=KEYS_LARGE):
    """
    Funcion para acceder a valores de interes de las llaves que guardan jsons.
    :param list_keys: Lista de Strings con las llaves que guardan jsons como valores.
    :param obj: Diccionario.
    :return: DataFrame.
    """
    cols = [
        x.replace(".","_") for x in list_keys
    ]
    df = pd.DataFrame(
        columns=list_keys
    )
    
    for key in list_keys:
        value = nested_get(
            key=key, 
            obj=obj
        )
        df[key] = [value]
        
    df.columns = cols
        
    return df


def attribute_extraction(obj:dict, attributes_id=constants.ATTRIBUTES_IDS):
    """
    Funcion para acceder a valores de interes de la llave attributes.
    :param attributes_id: Lista de Strings con los attibutos de interes.
    :param obj: Json item.
    :return: DataFrame.
    """
    atts = obj["attributes"]
    data = {
        "NUM_ATTRIBUTEs":len(atts)
    }
    
    for x in atts:
        att_id = x["id"]
        value = None
        
        if att_id in attributes_id:
            
            data[att_id] = x["value_name"]
            
    df = pd.DataFrame(
        data=data,
        index=[0]
    )
    
    return df


def tags_extraction(obj:dict, list_tags=constants.TAGS):
    """
    Funcion para acceder a valores de interes de la llave attributes.
    :param list_tags: Lista de Strings con los tags de interes.
    :param obj: Json item.
    :return: DataFrame.
    """
    item_tags = obj["tags"]
    data = {
        "num_tags":len(item_tags)
    }
    
    for tag in list_tags:
        data[tag] = 1 if tag in item_tags else 0
        
    df = pd.DataFrame(
        data=data,
        index=[0]
    )
    
    return df  


def info_item(
    obj_item:dict,
    list_direct_values=constants.KEYS_DIRECT_VALUES,
    obj_keys_json_type=constants.KEYS_JSON_TYPES,
    attributes_id=constants.ATTRIBUTES_IDS,
    list_tags=constants.TAGS
):
    """
    Funcion que retorna la informacion relevante por item, de acuerdo a los parametros.
    :param: json del item junto con especificaciones para cada funcion.
    :return: DataFrame.
    """
    keys_large_json=keys_large_construction(obj_keys_json_type)
    
    df = pd.concat(
        [
            direct_values_extraction(
                obj=obj_item, 
                list_keys=list_direct_values
            ),
            sub_json_extraction(
                obj=obj_item,
                list_keys=keys_large_json
            ),
            attribute_extraction(
                obj=obj_item,
                attributes_id=attributes_id
            ),
            tags_extraction(
                obj=obj_item, 
                list_tags=list_tags
            )
        ],
        axis=1
    )
    
    return df


def items_request(obj:dict):
    """
    Funcion que estructura una tabla con la informacion de items por consulta
    :param: Consulta API.
    :return: DataFrame.
    """

    df = pd.DataFrame()
    try:
        for x in obj["results"]:
            df_temp = info_item(obj_item=x)
            df = pd.concat(
                [
                    df_temp,
                    df
                ],
                axis=0
            ).reset_index(drop=True)
    except:
        print("[ERROR]: No se pudo crear tabla de items")
        
    return df


def lote_items(
    category:str,
    site:str,
    size:int,
    file_name:str,
    discount:bool
):
    """
    Funcion que realiza sufientes consultas y las estructura para generar una tabla
        con un minimo de items
    :param: Detalles de consulta y numero de items.
    :return: DataFrame.
    """
    if discount:
        URL_TEMP = constants.URL_SITE_CAT_OFFSET_DISC
    else:
        URL_TEMP = constants.URL_SITE_CAT_OFFSET
        
    load = -1
    errores = 0
    while(load<size)&(errores<10):
        try:
            json_temp = requests.request(
                "GET",
                URL_TEMP.format(
                    site=site,
                    category=category,
                    offset=load+1
                )
            ).json()
                      
            df_temp = items_request(json_temp)
            
            if file_name in os.listdir():
                df_loaded_items = pd.read_csv(file_name)
            else:
                df_loaded_items = pd.DataFrame()
                
            df_loaded_items = pd.concat(
                [
                    df_temp,
                    df_loaded_items
                ],
                axis=0
            ).reset_index(drop=True)
            
            load = df_loaded_items.shape[0]
            df_loaded_items.to_csv(file_name,index=False)
            
        except(KeyError, ValueError, TypeError):
            print("[ERROR]: No se puedo cargar el volumen de datos.")
            time.sleep(3)
            errores = errores + 1
    print("[INFO]: Termino, revise la ruta "+file_name)