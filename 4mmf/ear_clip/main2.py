import triangle as trg
import sys
import time

preset = [(0,0), (0,50), (0,100), (50,50), (50,0), (50,100), (100,0), (100,50), (100,100)]


def main():
    points = preset
    print("Number of points: {0} \n".format(len(points)))
    #start = time.clock()
    (ears, rev) = trg.ears_finding(points)
    print(ears)
    print(rev)
    edges = trg.ears_clipping(points, ears, 'index', rev)
    #end = time.clock()
    #print ("Elapsed time: {0} seconds \n".format(end - start))
    print(edges)


if __name__ == "__main__":
    main()