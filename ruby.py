import numpy as np
import pandas as pd
pd.set_option('display.max_rows', None)
ruby=pd.read_csv('ruby.csv')
ruby=ruby.sort_values('group_code')
rubyi=np.arange(0,62,1)
rubyi=pd.DataFrame(rubyi)
ruby2=pd.merge(ruby,rubyi,left_index=True,right_index=True)
ruby2.columns=['area','label','ruby','group_code','population','pref','en','number']
ruby2['en']=ruby2['en'].str.replace(pat='ō',repl='o')
ruby2['en']=ruby2['en'].str.replace(pat='Ō',repl='O')
ruby2['en']=ruby2['en'].str.replace(pat='ū',repl='u')

ruby2.to_csv('ruby2.csv')