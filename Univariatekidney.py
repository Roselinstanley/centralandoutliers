import pandas as pd
import numpy as np
class univar:
    quan=[]
    qual=[]
    def __init__(self,dataset):
        self.dataset=dataset
        self.Lesser=[]
        self.Greater=[]
    def quanqual(self):
        for cname in self.dataset.columns:
            if((cname!='pcv')and(cname!='wc')and(cname!='rc')and(self.dataset[cname].dtype=='O')):
                self.qual.append(cname)
            else:
                self.quan.append(cname)             
        return self.qual,self.quan
    def centraltendency(self):
        global centraluni
        centraluni=pd.DataFrame(index=["Mean","Median","Mode","Q1:25","Q2:50","Q3:75","Q4:100","IQR","1.5*IQR","Lesser","Greater","Min","Max"],columns=self.quan)
        for cname in self.quan:
            centraluni[cname]["Mean"]=self.dataset[cname].mean()
            centraluni[cname]["Median"]=self.dataset[cname].median()
            centraluni[cname]["Mode"]=self.dataset[cname].mode()[0]
            centraluni[cname]["Q1:25"]=self.dataset.describe()[cname]["25%"]
            centraluni[cname]["Q2:50"]=self.dataset.describe()[cname]["50%"]
            centraluni[cname]["Q3:75"]=self.dataset.describe()[cname]["75%"]
            centraluni[cname]["Q4:100"]=np.percentile(self.dataset[cname],100)
            centraluni[cname]["IQR"]=centraluni[cname]["Q3:75"]-centraluni[cname]["Q1:25"]
            centraluni[cname]["1.5*IQR"]=1.5*centraluni[cname]["IQR"]
            centraluni[cname]["Lesser"]=centraluni[cname]["Q1:25"]-centraluni[cname]["1.5*IQR"]
            centraluni[cname]["Greater"]= centraluni[cname]["Q3:75"]+centraluni[cname]["1.5*IQR"]
            centraluni[cname]["Min"]=self.dataset[cname].min()
            centraluni[cname]["Max"]=self.dataset[cname].max()
        return centraluni
    def outlierscheck(self):
        for cname in self.quan:
            if centraluni[cname]["Min"] < centraluni[cname]["Lesser"]:
                self.Lesser.append(cname)
            if centraluni[cname]["Max"] > centraluni[cname]["Greater"]:
                self.Greater.append(cname)
        return self.Lesser,self.Greater
    def replacingoutliers(self):
        for cname in self.Lesser:
            self.dataset[cname][self.dataset[cname] < centraluni[cname]["Lesser"]]=centraluni[cname]["Lesser"]
        for cname in self.Greater:
            self.dataset[cname][self.dataset[cname] > centraluni[cname]["Greater"]]=centraluni[cname]["Greater"] 
        return self.dataset
                
                
                
    
    
