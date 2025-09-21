import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import seaborn as sns
data = pd.read_csv('data.csv')
# Вывод заголовка таблицы
#print(data.head())

# Вывод типов переменных
#print(data.info())

# Переименование и изменения типа на число
data = data.replace({'Not Available': np.nan})
# Просматриваем столбцы
for col in list(data.columns):
 # Выбираем столбцы, которые должны быть числовыми
    if ('ft²' in col or 'kBtu' in col or 'Metric Tons CO2e' in col or 'kWh' in 
col or 'therms' in col or 'gal' in col or 'Score' in col):
# Преобразуем к float
        data[col] = data[col].astype(float)
#print(data)

# Поиск пустых значений и их удаление
def missing_values_table(data):
   mis_val = data.isnull().sum()
   mis_val_percent = 100 * data.isnull().sum() / len(data)
   mis_val_table = pd.concat([mis_val, mis_val_percent], axis=1)
   mis_val_table_ren_columns = mis_val_table.rename(
   columns = {0 : 'Пустые значения', 1 : '% от общего количества'})
   mis_val_table_ren_columns = mis_val_table_ren_columns[
       mis_val_table_ren_columns.iloc[:,1] != 0].sort_values(
   '% от общего количества', ascending=False).round(1)
   print ("Датафрейм содержит " + str(data.shape[1]) + " columns.\n"     
       "Из них " + str(mis_val_table_ren_columns.shape[0]) +
           " столбцов с пустыми значениями.")
   thresh = len(mis_val_table_ren_columns) * 0.5
   data.dropna(thresh=thresh, axis=1, inplace=True)
   return mis_val_table_ren_columns

# Вызов функции
missing_values_table(data)

# Построение гистограммы 
plt.style.use('fivethirtyeight')
plt.hist(data['ENERGY STAR Score'].dropna(), bins = 100, edgecolor = 'k')
plt.xlabel('Score'); plt.ylabel('Number of Buildings')
plt.title('Energy Star Score Distribution')
plt.show()

# Создать список зданий
data['Largest Property Use Type'] = data['Largest Property Use Type'].astype('category')
data['Largest Property Use Type'] = data['Largest Property Use Type'].cat.codes
types = data.dropna(subset=['ENERGY STAR Score'])
types = types['Largest Property Use Type'].value_counts()
types = list(types[types.values > 100].index)
# График распределения по категориям зданий
figure(figsize=(8, 6), dpi=80)
# График для каждого здания
for b_type in types:
    # Select the building type
    subset = data[data['Largest Property Use Type'] == b_type]
    # Density plot енргопотребления
    sns.kdeplot(subset['ENERGY STAR Score'].dropna(),
               label = b_type, fill = False, alpha = 0.8)
    # label the plot
plt.xlabel('ENERGY STAR Score', size = 20); plt.ylabel('Density', size = 20) 
plt.title('Density Plot of ENERGY STAR Score by Building Type', size = 28)
plt.show()
correlation =  data[data.columns].corr(numeric_only=True)['ENERGY STAR Score'].sort_values(ascending=False)
print(correlation)

# 5
# Copy the original data
features = data.copy()

# Select the numeric columns
numeric_subset = data.select_dtypes('number')

# Create columns with log of absolute values of numeric columns
for col in numeric_subset.columns:
   # Skip the Energy Star Score column
   if col == 'ENERGY STAR Score':
       next
   else:
       # Take the absolute value before taking the logarithm
       numeric_subset['log_' + col] = np.log1p(abs(numeric_subset[col]))

# Select the categorical columns
categorical_subset = data[['Borough', 'Largest Property Use Type']]

# One hot encode
categorical_subset = pd.get_dummies(categorical_subset)

# Join the two dataframes using concat
# Make sure to use axis = 1 to perform a column bind
features = pd.concat([numeric_subset, categorical_subset], axis = 1)

# Extract the columns to  plot
plot_data = features[['ENERGY STAR Score', 'Site EUI (kBtu/ft²)', 
                      'Weather Normalized Source EUI (kBtu/ft²)', 
                      'Total GHG Emissions (Metric Tons CO2e)']]


plot_data = plot_data.drop_duplicates(keep = False)

# Replace the inf with nan
plot_data = plot_data.replace({np.inf: np.nan, -np.inf: np.nan})

# Rename columns 
plot_data = plot_data.rename(columns = {'Site EUI (kBtu/ft²)': 'Site EUI', 
                                        'Weather Normalized Source EUI (kBtu/ft²)': 'Weather Norm EUI',
                                        'Total GHG Emissions (Metric Tons CO2e)': 'Total GHG Emissions'})

# Drop na values
plot_data = plot_data.dropna()

# Function to calculate correlation coefficient between two columns
def corr_func(x, y, **kwargs):
    r = np.corrcoef(x, y)[0][1]
    ax = plt.gca()
    ax.annotate("r = {:.2f}".format(r),
                xy=(.2, .8), xycoords=ax.transAxes,
                size = 20)

# если не смогу пофиксить
# for i, column in enumerate(plot_data.columns[:-1]):
#     plt.figure(figsize=(8, 6))
#     plt.scatter(plot_data[column], plot_data['Total GHG Emissions'], alpha=0.5)
#     plt.title(f'Scatter plot of Total GHG Emissions vs {column}')
#     plt.xlabel(column)
#     plt.ylabel('Total GHG Emissions')
#     plt.show()

g = sns.pairplot(plot_data)
g.map_lower(corr_func, cmap = plt.cm.Reds_r)
g.map_upper(corr_func, cmap = plt.cm.Reds_r)
plt.show()

# # Create the pairgrid object
# grid = sns.PairGrid(data = plot_data, height = 3)

# # Upper is a scatter plot
# grid.map_upper(plt.scatter, color = 'red', alpha = 0.6)

# # Diagonal is a histogram
# grid.map_diag(plt.hist, color = 'red', edgecolor = 'black')

# # Bottom is correlation and density plot
# grid.map_lower(corr_func)
# grid.map_lower(sns.kdeplot, cmap = plt.cm.Reds_r)

# # Title for entire plot
# plt.suptitle('Pairs Plot of Energy Data', size = 36, y = 1.02)
# plt.show()
# Remove any columns with all na values

features  = features.dropna(axis=1, how = 'all')
print(features.shape)