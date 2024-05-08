from contextualized.analysis import print_acc_by_covars
import numpy as np
import pandas as pd
from contextualized.easy import ContextualizedClassifier

C = np.random.rand(10, 2)
X = np.random.rand(10, 2)
Y = np.random.randint(0, 2, size=(10, 2))
model = ContextualizedClassifier()
model.fit(C, X, Y)

covar_df = pd.DataFrame(C, columns=['C0', 'C1'])
print_acc_by_covars(Y, model.predict(C, X), covar_df)
print('done')
