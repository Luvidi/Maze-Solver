import cv2
import numpy as np
import time

def pos(r, c, cellSize) :
    return [int(cellSize/2+cellSize*r-1), int(cellSize/2+cellSize*c-1)]

def findWall(maze, mazeSize, cellSize) :
    print("Finding wall...")
    wall = []
    for row in range(mazeSize[0]):
        for col in range(mazeSize[1]):
            for d in [[0,1],[1,0]]:
                if row==mazeSize[0]-1 and d[0]==1:
                    continue
                if col==mazeSize[1]-1 and d[1]==1:
                    continue
                pos1 = pos(row, col, cellSize)
                
                for i in range(cellSize) :
                    pos2 = [int(pos1[0]+i*d[0]), int(pos1[1]+i*d[1])]
                    
                    if maze[pos2[0]][pos2[1]][0] == 0:
                        wall.append([[row, col], 
                                      [row+d[0], col+d[1]]])
                        break
    return wall

def drawWall(maze, wall, cellSize, color=(0,0,255)) :
    print("Drawing wall...")
    for w in wall:
        mid = [(w[0][0]+w[1][0])/2, (w[0][1]+w[1][1])/2]
        cv2.circle(maze, pos(mid[1], mid[0], cellSize), 5, color, -1)
    return maze

def legalMove(path, dest, wall, mazeSize) :
    pos1 = path[-1]
    legal = [[pos1, dest] not in wall,
             [dest, pos1] not in wall,
             dest[0]>=0,
             dest[0]<mazeSize[0],
             dest[1]>=0,
             dest[1]<mazeSize[1],
             dest not in path]
    
    return all(legal)

def nextPos(path, wall, mazeSize) :
    legal = []
    for d in [[0,1],[1,0],[0,-1],[-1,0]]:
        dest = [path[-1][0]+d[0], path[-1][1]+d[1]]
        if legalMove(path, dest, wall, mazeSize) :
            legal.append(dest)
    return legal

def solve(mazeSize, start, end, wall) :
    print("Solving...")
    path = [start]
    nextList = []
    visited = []
    
    while len(path) :
        nextP = nextPos(visited+path, wall, mazeSize)
        
        if end in nextP :
            return path+[end]

        if len(nextP) :
            nextList.append(nextP[1:])
            path.append(nextP[0])
            visited.append(path[-1])
        else :
            if len(nextList[-1]) :
                path.pop()
                path.append(nextList[-1].pop())
                visited.append(path[-1])
            else :
                path.pop()
                nextList.pop()
    return []

def drawPath(maze, path, cellSize, color=(0,0,255)) :
    print("Drawing path...")
    for i in range(len(path)-1) :
        p1 = pos(path[i][0], path[i][1], cellSize)
        p2 = pos(path[i+1][0], path[i+1][1], cellSize)
        cv2.line(maze, p1[::-1], p2[::-1], color, 2)
    return maze

def pathAnimation(maze, path, cellSize, speed=8, color=(0,0,255)) :
    print("Creating animation...")
    frames = []
    for i in range(len(path)-1) :
        for t in range(cellSize//speed+1) :
            p1 = pos(path[i][0], path[i][1], cellSize)[::-1]
            p2 = pos(path[i+1][0], path[i+1][1], cellSize)[::-1]
            p2 = [(p1[0]*(cellSize-t*speed)+p2[0]*t*speed)//cellSize, (p1[1]*(cellSize-t*speed)+p2[1]*t*speed)//cellSize]
            cv2.line(maze, p1, p2, color, 2)
            frames.append(maze.copy())
    return frames

def writeVideo(filename, frames, fps=30) :
    print("Saving video...")
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    writer = cv2.VideoWriter(filename, fourcc, fps, (frames[0].shape[1], frames[0].shape[0]))
    for frame in frames :
        writer.write(frame)
    writer.release()

def writeImg(filename, frame) :
    print("Saving image...")
    cv2.imwrite(filename, frame)

if __name__ == '__main__':   
    filename = "maze20x20.png"
    mazeSize = [20, 20]
    start = [0, 9]
    end = [19, 10]
    
    maze = cv2.imread(filename)
    
    cellSize = 32
    maze = cv2.resize(maze, (cellSize * mazeSize[0], cellSize * mazeSize[1]))
    maze2 = maze.copy()
    maze = cv2.threshold(maze, 127, 255, cv2.THRESH_BINARY)[1]
    
    st = time.time()
    wall = findWall(maze, mazeSize, cellSize)
    
    path = solve(mazeSize, start, end, wall)
    en = time.time()
    print("Solved in {}s".format(en-st))
    
    frames = pathAnimation(maze2.copy(), path, cellSize, color=(255,0,0))
    writeVideo("solved.mp4", frames)
    
    maze3 = drawPath(maze2.copy(), path, cellSize, color=(255,0,0))
    writeImg("solved.png", maze3)
    
    for frame in frames :
        cv2.imshow("Maze", frame)
        cv2.waitKey(1000//30)
           
    cv2.waitKey(0)