# https://towardsdatascience.com/introduction-to-linear-regression-in-python-c12a072bedf0

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import statsmodels.formula.api as smf

# Import and display first five rows of advertising dataset
advert = pd.read_csv('advertising.csv')
print(advert.head())



# Initialise and fit linear regression model using `statsmodels`
model = smf.ols('sales ~ TV', data=advert)
model = model.fit()
print("model.params ==> ")
print(model.params)
# # Sales = 7.032 + 0.047*TV --

# # Predict values
# sales_pred = model.predict()
#
#
# # Plot regression against actual data
# plt.figure(figsize=(12, 6))
# plt.plot(advert['TV'], advert['sales'], 'o')           # scatter plot showing actual data
# plt.plot(advert['TV'], sales_pred, 'r', linewidth=2)   # regression line
# plt.xlabel('TV Advertising Costs')
# plt.ylabel('Sales')
# plt.title('TV vs Sales')

# plt.show()


# new_X = 400
# pred_new_X = model.predict({"TV": new_X})
# print("pred_new_X"+str(pred_new_X))