import diff_match_patch as dmp

class slotDiff():
    """ Routines to compare two files a, b where b is obtained by ONLY replacing some numeric values in a by
    @!f(vx)!@ where f(vx) is any function of v1, v2, v3, ... 
    At the moment there is a bug: 
    when a number is replaced by a slot whose first element is that number, test fails!
    e.g. 0.01 => @!0.01*v1!@ fails!
    still: .4 => @!.4*v1!@ does not fail. 
    """
    
    def isjunk(self,string):
        "Return True if we don't care about this string"
        return string == ' '
    def __init__(self, swmmfile, slotfile):
        self.swmmfile=swmmfile
        self.slotfile=slotfile
        self.dmp=dmp.diff_match_patch()
        self.dmp.Diff_Timeout = 1.0

    def testDiff(self, verbose=False):
        with open(self.swmmfile,"r") as f1, open(self.slotfile,"r") as f2:
            before=f1.read()
            after=f2.read()
            #dmp.diff_main(before,after)
            return self.testDiffStr(after, before, verbose)

    def testDiffStr(self, after, before, verbose=False):
        k=self.dmp.diff_main(after,before)
        self.dmp.diff_cleanupSemantic(k)
        k1=[x[1].strip().split() for x in k if x[0]==1]
        # first split and flattern
        k1=[item for sublist in k1 for item in sublist]
        k1=[x for x in k1 if x!='']
        k2=[x[1].strip().split() for x in k if x[0]==-1]
        k2=[item for sublist in k2 for item in sublist]            
        k2=[x for x in k2 if x!=''] 
        failed=False
        if len(k1)!=len(k2):
            k1+=[None]*(len(k2)-len(k1))
            k2+=[None]*(len(k1)-len(k2))
        if (verbose):
            print "\n Differences:\n------------------"
            for i,j in zip(k1,k2):
                print i , "=>", j
            print"------------------"
        if failed:
            return False          
        #all k1 should be numbers
        if len([x for x in k1 if not self.isNumber(x)])>0:
            return False
        #all k2 should start and end with !@, !@ respectively. 
        if len([x for x in k2 if not self.isSlot(x)])>0:
            return False
        
        # now its OK
        return True
            
            
    def isSlot(self,val):
        if val[:2]=="@!" and val[-2:]=="!@":
            return True
        else:
            return False
    
    def isNumber(self,val):
        try:
            float(val)
        except:
            return False
        return True
        

if __name__=="__main__":
    sd=slotDiff("..\\examples\\storage_example\\StorageEx.inp","..\\examples\\storage_example\\StorageEx.inp_")
    print sd.testDiff()