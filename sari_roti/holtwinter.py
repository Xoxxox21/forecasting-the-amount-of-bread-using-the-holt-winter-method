# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt
# from statsmodels.tsa.holtwinters import ExponentialSmoothing

# df = pd.read_csv('/home/fauzan/Documents/TA/TGA/dropperkue.csv',index_col='tanggal',parse_dates=True)

# final_model = ExponentialSmoothing(df['dropping'],trend='multiplicative',seasonal='multiplicative',seasonal_periods=7).fit()
# # print(final_model.summary())
# # forecast_predictions = final_model.forecast(8)
# # # y = [2990, 2710, 2540, 3300, 2990]
# # # x = [18, 19, 20, 21, 22]
# # plt.plot(x, y)

# # plt.xlabel('Tanggal (Januari)')
# # plt.ylabel('Harga')

# # plt.title('Harga Emiten ANTM')
# # plt.grid(True)

# # plt.show()
# #     df['total_sales'].plot(legend=True,label='MAIN',figsize=(6,4))
# #     forecast_predictions.plot(legend=True,label='FORECAST_PREDICTION',figsize=(6,4))
# #     plt.show()
