
import pandas as pd
import numpy as np
import nasdaqdatalink
import matplotlib.pyplot as plt
from numpy.polynomial.polynomial import polyfit
plt.style.use("ggplot")

nasdaqdatalink.ApiConfig.api_key = "HvE35hWif-qXZ7NpE7aE"

data = nasdaqdatalink.get('FSE/BDT_X')

# convert the datetime index to ordinal values & store as new column, which can be used to plot a regression line
data['ordinal_date'] = data.index.map(pd.Timestamp.toordinal)


# Problem # 1 to 5

plt.plot(data['Close'], label='Close')
plt.plot(data['Close'].rolling('90d').mean(), label='90 Days Close')
plt.plot(data['Close'].rolling('30d').mean(), label='30 Days Close')
plt.plot(data['Close'].rolling('7d').mean(), label='7 Days Close')
plt.plot(data['Close'].resample('M', convention='end').mean(), label='Monthly Average Close')

consecutive_increase = data['Close'].rolling(5).apply(lambda x: np.all(np.diff(x) > 0))
consecutive_increase = consecutive_increase.loc[consecutive_increase == 1]
plt.plot(consecutive_increase, 'g^', label='consecutive increase')

consecutive_decrease = data['Close'].rolling(4).apply(lambda x: np.all(np.diff(x) < 0))
consecutive_decrease = consecutive_decrease.loc[consecutive_decrease == 1]
plt.plot(consecutive_decrease + 10, 'b^', label='consecutive decrease')  # adding 10 so as not to overlap with 
# consecutive increase

plt.legend(loc='best')
plt.title('Frankfurt Stock Exchange, Problem 1 to 5')
plt.xlabel("Date")
plt.ylabel("Close Price")

plt.savefig("problem_1_to_5.png")

# Plotting 'close' price and regression lines. i.e Problem # 6
plt.plot(data['Close'], label='Close')

last_90_data = data.tail(90)
b, m = polyfit(last_90_data['ordinal_date'], last_90_data['Close'], 1)
data['90_days_regression'] = b + m * data['ordinal_date']
plt.plot(data['90_days_regression'], label='90 days regression')

last_30_data = data.tail(30)
b, m = polyfit(last_30_data['ordinal_date'], last_30_data['Close'], 1)
data['30_days_regression'] = b + m * data['ordinal_date']
plt.plot(data['30_days_regression'], label='30 days regression')

last_7_data = data.tail(7)
b, m = polyfit(last_7_data['ordinal_date'], last_7_data['Close'], 1)
data['7_days_regression'] = b + m * data['ordinal_date']
plt.plot(data['7_days_regression'], label='7 days regression')


plt.legend(loc='best')
plt.title('Frankfurt Stock Exchange, Problem 6')
plt.xlabel("Date")
plt.ylabel("Close Price")

plt.savefig("problem_6.png")

