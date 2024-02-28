from fpl_auto import evaluate as eval
from fpl_auto import team
t = team.team('2023-24')
p_list = [
    [56, 38, 66, 35, 49, 44, 50, 50, 32, 31, 45, 59, 42, 29, 64, 43, 26, 44, 36, 53, 44, 65, 20, 68, 64, 70, 79, 70, 62, 75, 69, 76, 72, 75, 62, 83, 90, 89],
    [47, 52, 51, 55, 31, 60, 46, 46, 52, 46, 22, 43, 42, 51, 54, 61, 42, 42, 40, 56, 37, 42, 38, 37, 49, 49, 64, 59, 61, 57, 59, 63, 62, 67, 57, 78, 75],
    [32, 29, 24, 28, 30, 75, 55, 53, 59, 32, 21, 13, 21, 42, 34, 40, 43, 19, 43, 34, 43, 29, 23, 33]
]
xp_list = [
    [35.65, 59.73, 73.52, 81.89999999999999, 66.53, 59.56, 53.53, 61.65, 82.77000000000001, 61.85000000000001, 63.63, 95.97, 107.54, 79.55000000000001, 72.06, 78.23, 70.44, 64.71, 54.120000000000005, 74.87, 80.07, 74.97999999999999, 86.55000000000001, 65.2, 78.21, 73.60999999999999, 47.82, 58.87, 70.84, 59.33, 56.660000000000004, 73.43, 68.7, 72.52, 73.57000000000001, 63.12, 38.58, 83.65],
    [53.93, 55.359999999999985, 67.26, 83.99000000000001, 65.53999999999999, 68.31, 0, 0, 66.45, 70.53, 78.45, 85.7, 87.25999999999999, 99.64000000000001, 71.98, 89.09, 90.12, 94.02000000000001, 63.0, 67.79, 59.959999999999994, 86.24000000000001, 73.35, 79.17999999999999, 66.52, 19.54, 63.35, 61.03999999999999, 53.25, 50.73, 82.46, 64.08, 62.699999999999996, 99.64999999999999, 47.529999999999994, 47.61, 62.010000000000005, 63.919999999999995],
    [45.09, 42.83, 51.06, 50.35, 52.989999999999995, 49.92999999999999, 84.22000000000001, 90.21, 102.81999999999998, 85.00999999999999, 62.150000000000006, 46.480000000000004, 41.83, 30.749999999999996, 43.830000000000005, 70.89, 61.220000000000006, 61.9, 40.39, 61.86000000000001, 55.77, 71.85999999999999, 72.96, 80.58999999999999, 48.12]
]
seasons = ['2021-22', '2022-23', '2023-24']

eval.box_plot_by_season(p_list, seasons)

all_p = [[2, 2, 0, 2, 0, 1, 1, 1, 20, 0, 13], [6, 2, 1, 0, 6, 0, 1, 10, 0, 1, 2], [1, 0, 6, 2, 2, 1, 4, 2, 1, 1, 8], [2, 1, 4, 1, 1, 4, 1, 2, 1, 6, 8], [8, 8, 8, 2, 0, 0, 3, 2, 3, 1, 5], [2, 18, 1, 14, 0, 11, 1, 3, 2, 24, 5], [6, 48, 7, 1, 0, 0, 3, 3, 2, 2, 6], [6, 24, 6, 7, 2, 1, 1, 3, 0, 13, 1], [2, 40, 6, 0, 0, 7, 2, 3, 0, 1, 6], [6, 0, 2, 6, 1, 0, 1, 2, 0, 13, 0], [2, 9, 0, 4, 1, 0, 2, 4, 4, 0, 2], [3, 1, 5, 1, 0, 0, 2, 3, 2, 0, 0], [6, 1, 5, 1, 2, 0, 2, 1, 8, 0, 0], [2, 12, 0, 1, 8, 1, 14, 4, 2, 0, 0], [1, 1, 5, 6, 6, 1, 8, 1, 1, 0, 2], [2, -1, 5, 6, 6, 1, 8, 2, 1, 2, 4], [6, 8, 2, 6, 10, 4, 9, 2, 3, 0, 2], [2, 2, 1, 1, 2, 0, 3, 2, 0, 2, 1], [6, 5, 4, 0, 0, 1, 2, 2, 2, 1, 7], [1, 2, 0, 1, 1, 24, 4, 7, 1, 6, 0], [8, 6, 1, 7, 5, 2, 2, 2, 0, 24, 8], [2, 1, 7, -1, 6, 2, 2, 1, 0, 4, 10], [2, 1, 9, 1, 6, 14, 13, 2, 1, 0, 1], [6, 2, 4, 1, 1, 1, 8, 8, 1, 6, 1]]

# #eval.box_plot_by_week(all_p, 1, 25, '2023-24')

eval.point_distribution(p_list[0], seasons[0])
eval.point_distribution(p_list[1], seasons[1])
eval.point_distribution(p_list[2], seasons[2])

eval.plot_cumulative_points(p_list[0], seasons[0])
eval.plot_cumulative_points(p_list[1], seasons[1])
eval.plot_cumulative_points(p_list[2], seasons[2])

print(f'Sum of avg list = {sum(t.get_avg_score())}')
print(f'avg p per week of avg list = {sum(t.get_avg_score()) / len(t.get_avg_score())}')