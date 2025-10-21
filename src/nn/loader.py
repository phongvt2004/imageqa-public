import yaml
from . import router
from .model import *

def load(modelSpecFilename):
    """
    Need the following items in the model spec file:
    costFn
    decisionFn
    stages
    specs
    :param modelSpecFilename:
    :return:
    """
    with open(modelSpecFilename) as f:
        modelDict = yaml.load(f, Loader=yaml.FullLoader)

    for stageDict in modelDict['specs']:
        router.addStage(stageDict)

    modelStages = []
    for s in modelDict['stages']:
        modelStages.append(router.routeStage(s))
    costFn=router.routeFn(modelDict['costFn'])

    if 'decisionFn' in modelDict:
        decisionFn = router.routeFn(modelDict['decisionFn'])
    else:
        decisionFn = None
    outputList = modelDict['outputs'].split(',')
    for i in range(len(outputList)):
        outputList[i] = outputList[i].strip()
    model = GraphModel(
        name=modelDict['name'] if 'name' in modelDict else None,
        stages=modelStages,
        outputStageNames=outputList,
        costFn=costFn,
        decisionFn=decisionFn,
        specFilename=modelSpecFilename)

    return model