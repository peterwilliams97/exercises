"""
  Convert a Weka formatted .cvs file to a Google Predict one
"""
import sys, os, os.path, csv

def wekaToPredict(weka_filename):
    """ Convert a Weka formatted .cvs file to a Google
        Predict .csv file by moving class from last 
        column to first
    """
    parts = os.path.splitext(weka_filename)
    predict_filename = parts[0] + '.gp' + parts[1]
    print 'wekaToPredict:', weka_filename,'=>', predict_filename
    weka = csv.readCsvRaw(weka_filename)
    predict = [[w[-1]] + w[:-1] for w in weka]
    csv.writeCsv(predict_filename, predict) 
    
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'Usage weka2predict weka_filename'
        exit()
    else:
        weka_filename = sys.argv[1]
        
    print sys.argv[0]
    wekaToPredict(weka_filename)
