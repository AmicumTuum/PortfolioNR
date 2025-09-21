import pandas as pd

# df = pd.DataFrame({'Name': ['Manchester City', 'Real Madrid', 'Liverpool',
#                             'FC Bayern München', 'FC Barcelona', 'Juventus'],
#                    'League': ['English Premier League (1)', 'Spain Primera Division (1)',
#                               'English Premier League (1)', 'German 1. Bundesliga (1)',
#                               'Spain Primera Division (1)', 'Italian Serie A (1)'],
#                    'TransferBudget': [176000, 188500, 90000,
#                                       100000, 180500, 105000]})

# df.to_excel('./teams.xlsx', sheet_name='eight.xlsx', index=False)
# print('Успешно')

df = pd.read_excel("eight.xlsx")
print(df.head())
df.drop(labels = [2],axis = 0, inplace = True)
print(df.head())
df.to_excel('./eight_edited.xlsx', sheet_name='eight.xlsx', index=False)