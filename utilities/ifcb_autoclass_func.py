# Autoclass function for occurrences IFCB
# Note need newer version of pandas than is on Research workspace.
# 2.2.2 works also need to upgrade numexp on RW
import pandas as pd
import ifcb_api_access 
import numpy as np
#
# code to get the target labels should be in seperate code
fname='target_classification_labels.csv'
target_labels=pd.read_csv(fname)
bin_id='D20210926T181303_IFCB158'
#
def get_bin_occurrences(bin_id,target_labels):
	bin_details=ifcb_api_access.get_bin_details(bin_id)
	if ifcb_api_access.bin_has_autoclass('D20230326T150748_IFCB158'):
		url='https://ifcb.caloos.org/del-mar-mooring/' # place holder for the moment will use SC Wharf
		file_name=bin_id+"_class_scores.csv"
		bin_url=url+file_name
		# read the autoclass file
		autoclass=pd.read_csv(bin_url)
		# names in pandas dataframe can not have spaces so need to change spaces to underscores
		# Note this code is not the best as it give warnings so probably a better way to do this.
		x=target_labels['label']
		lx=len(x)
		for i in np.arange(0,lx):
			x[i]=x[i].replace(' ','_')
		#
		# add the name pid to the list so we can keep it when we transform data
		y=pd.concat([pd.Series(['pid']),x])
		# reset the index so we don't have two "0"s
		y.reset_index(drop=True)
		# remove extraneous columns (this keeps only the columns with names in y above
		ax=autoclass[y]
		# set PID as the index so we may remove it for some work later
		a2=ax.set_index(['pid'],append=False)
		a2.index.name=None # now set index column name to blank
		az=a2.stack(future_stack=True) # this is why need the more modern version of pandas!
		ik=np.arange(0,len(az))
		# there may be a more elegant way of doing this but these were strings and I needed to convert them back
		for r in ik:
			junk=str(az[r:r+1]).split()
			if r==0:
				pid=[junk[0]]
				myclass=[junk[1]]
				score=[float(junk[2])]
			else:
				pid.append(junk[0])
				myclass.append(junk[1])
				score.append(float(junk[2]))
				# finally we have the table that Ian's autoclass code wants
		bigtable=pd.DataFrame({'pid':pid,'class':myclass,'score':score})
		ix=np.arange(0,3)
		zz=0
		for kk in ix:
			id1=bigtable['class']==target_labels['label'][kk]
			subtable=bigtable[['pid','class','score']][id1]
			id2=subtable['score'] >= target_labels['autoclass_threshold'][kk]
			smalltable=subtable[['pid','class','score']][id2]
			if smalltable.size > 0:
				if zz==0:
					classtable=smalltable
					zz=zz+1
				else:
					classtable.append(smalltable)
		return(classtable)

