import time
import math
from pathlib import Path 
start_time = time.time()
cwd = Path(__file__).parent
path = cwd.joinpath("in.txt")
file = open(path, "r").read().splitlines()

robot_types = ["geode", "obsidian", "ore", "clay"] # sorted by priority
blueprints = list[dict[str, dict[str, int]]]()

for line in file:
    _, t = line.split(": ")
    terms = t[:-1].split(".")
    blueprint = dict[str, dict[str, int]]()
    for term in terms:
        r, c = term.split(" costs ")
        robot = r.split()[1]
        costTerms = c.split(" and ")
        robotCost = dict[str, int]()
        for costTerm in costTerms:
            cost, type = costTerm.split()
            robotCost[type] = int(cost)
        blueprint[robot] = robotCost
    blueprints.append(blueprint)


evalMap = dict[tuple, int]()
def evaluateBlueprint(blueprint: dict[str, dict[str, int]], maxReq: dict[str, int], robots: dict[str, int], ores: dict[str, int], t:int) -> int:
    if(t == 0):
        return ores["geode"] if "geode" in ores else 0
    
    keyList = list[int]([t,0,0,0,0,0,0,0,0])
    for i, type in enumerate(robot_types):
        if(type in robots):
            keyList[i+1] = robots[type]
        if(type in ores):
            keyList[i+5] = ores[type]
    key = tuple(keyList)
    if(key in evalMap):
        return evalMap[key]
    
    robotToBuild = ""
    for robot in robot_types:
        if(robot in maxReq and robot in robots and robots[robot] >= maxReq[robot]):
            continue
        robotCost = blueprint[robot]
        for type in robotCost:
            if(type not in ores or robotCost[type] > ores[type]):
                break
        else:
            robotToBuild = robot
        if(robotToBuild != ""):
            break
    
    for robot in robots:
        if(robot in ores):
            ores[robot] += robots[robot]
        else:
            ores[robot] = robots[robot]
    
    result = 0
    if robotToBuild != "":
        robot = robotToBuild
        updatedRobots = robots.copy()
        if(robot in updatedRobots):
            updatedRobots[robot] += 1
        else:
            updatedRobots[robot] = 1
        updatedOres = ores.copy()
        for type in blueprint[robot]:
            updatedOres[type] -= blueprint[robot][type]
        robotResult = evaluateBlueprint(blueprint, maxReq, updatedRobots, updatedOres, t - 1)
        result = max(result, robotResult)
    
    else:
        dontBuildRobotsResult = evaluateBlueprint(blueprint, maxReq, robots, ores, t - 1)
        result = max(result, dontBuildRobotsResult)
    evalMap[key] = result
    return result


result = 1
for i,blueprint in enumerate(blueprints):
    if(i >= 3):
        break
    evalMap.clear()
    maxReq = dict[str, int]()
    for robot in blueprint:
        for type in blueprint[robot]:
            if(type not in maxReq or blueprint[robot][type] > maxReq[type]):
                maxReq[type] = blueprint[robot][type]
    evalResult = evaluateBlueprint(blueprint, maxReq, { "ore": 1 }, {}, 32)
    print(evalResult)
    if(evalResult > 0):
        result *= evalResult
    



print("--- %s seconds ---" % (time.time() - start_time))
print("result", result)