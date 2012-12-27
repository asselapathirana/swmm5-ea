import diff_match_patch as dmp

class slotDiff():
    
    def isjunk(self,string):
        "Return True if we don't care about this string"
        return string == ' '
    def __init__(self, swmmfile, slotfile):
        self.swmmfile=swmmfile
        self.slotfile=slotfile
        self.dmp=dmp.diff_match_patch()

    def testDiff(self):
        with open(self.swmmfile,"r") as f1, open(self.slotfile,"r") as f2:
            before=f1.read()
            after=f2.read()
            #dmp.diff_main(before,after)
            k=self.dmp.diff_main(after,before)
            self.dmp.diff_cleanupSemantic(k)
            k1=[x[1].strip() for x in k if x[0]==1]
            k1=[x for x in k1 if x!='']
            k2=[x[1].strip() for x in k if x[0]==-1]
            k2=[x for x in k2 if x!=''] 
            if len(k1)!=len(k2):
                return False
            for i,j in zip(k1,k2):
                print i , "=>", j
            pass  
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