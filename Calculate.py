import logging
import math
import sys
import pandas as pd
import numpy as np
from log import *  
from global_const import *


# This function returns a list of ratios for a specific operation
def findRatio(x, y):
    return y / x

def getOperationRatios(points):
    '''
    Input: 
    revenueStructure: [{x:x, y:y}]
    '''
    ratios = []
    prevPt = points[0]
    for i in range(1, len(points)):
        x_value = points[i][FLOWPERDAY]
        y_value = points[i]['dollarsPerDay']
        pt = findRatio(
            x_value, y_value)
        ratios.append(pt)
    return ratios

def findOperationRatios(points, opId):
    '''
    Input: 
    revenueStructure: [{x:x, y:y}]
    '''
    ratios = []
    prevPt = points[0]
    for i in range(1, len(points)):
        x_value = points[i][FLOWPERDAY]
        y_value = points[i]["dollarsPerDay"]
        pt = {"id": opId, "r": findRatio(
            x_value, y_value), "high": x_value, "low": prevPt[FLOWPERDAY]}
        ratios.append(pt)
        prevPt = points[i]
    return ratios


# def findAllOperationRatiosSorted(operations):
#     ratios_list = []
#     for operation in operations:
#         ratios_list.insert(
#             *findOperationRatios(operation["revenueStructure"], operation['id']))
#     return ratios_list.sort(reverse=True, key=lambda elem: elem.r)

def selectOptimalWaterFlow(flowRateIn, operations, ratiosSorted):
    results = {}
    maxInFlow = flowRateIn
    log(f'total: {maxInFlow}', file_path)
    #factorySet = set(list(map(lambda elem: elem["id"], operations)))
    isContinued = True
    while isContinued:
        factorySet = set(ratiosSorted['id'])
        for idx, pt in ratiosSorted.iterrows():
            if maxInFlow <= 0:
                isContinued = False
                break
            log(f'maxInFlow: {maxInFlow}', file_path)
            # ignore all visited ratios
            if pt["mark"] == 1:
                continue
            id = pt["id"]
            if id not in factorySet:
                continue
            
            # assign the water flow to the factory with id
            # if pt["ratio"] < 0:
            #     results['id'] = {"ratio": 0, FLOWPERDAY: 0, "id": id}
            #     continue

            # calc how much flow to give
            allocFlow = min(maxInFlow, pt[FLOWPERDAY])
            log(f'allocFlow: {allocFlow}', file_path)

            if allocFlow < pt[FLOWPERDAY] - INTERVAL:
                continue
            if id in results and results[id][FLOWPERDAY] < allocFlow:
                # replace more flow in the factory with old flow
                maxInFlow = maxInFlow + results[id][FLOWPERDAY] - allocFlow
            elif id not in results:
                # no replacement. First time
                maxInFlow -= allocFlow
            elif maxInFlow == allocFlow:
                maxInFlow -= allocFlow
                allocFlow = results[id][FLOWPERDAY] + allocFlow
            else:
                continue
            results[id] = {"ratio": pt["ratio"], FLOWPERDAY: allocFlow, "id": id}
            factorySet.remove(id)
            pt["mark"] = 1

    log(f'used: {flowRateIn-maxInFlow}', file_path)
    return list(results.values())



