def metric_business_all_users(data, cashback: dict, users_count: int):
    user_data = data.copy()
    for category, percent in cashback.items():
        user_data.loc[user_data['category'] == category, ['pred_sum', 'real_sum']] = \
            user_data.loc[user_data['category'] == category, ['pred_sum', 'real_sum']] * percent

    #     for user in user_data['party_rk'].unique():
    #         potentional_cashback_all_user_sum += sum(user_data[user_data['party_rk'] == user].nlargest(3,'real_sum')['real_sum'])
    #         real_cashback_all_user_sum += sum(user_data[user_data['party_rk'] == user].nlargest(3,'pred_sum')['real_sum'])

    potentional_cashback_all_user_sum = int(
        sum(user_data.groupby('party_rk')['real_sum'].apply(lambda grp: grp.nlargest(3).sum())))
    real_cashback_all_user_sum = int(
        sum(user_data.groupby('party_rk').apply(lambda grp: grp.nlargest(3, 'pred_sum')['real_sum'].sum())))

    delta = potentional_cashback_all_user_sum - real_cashback_all_user_sum
    average_delta = int(delta / users_count)
    average_real_cashback = int(real_cashback_all_user_sum / users_count)
    return {
        'real_cashback_all_user_sum': real_cashback_all_user_sum,
        'potentional_cashback_all_user_sum': potentional_cashback_all_user_sum,
        'delta': delta,
        'average_delta': average_delta,
        'average_real_cashback': average_real_cashback
    }


def metric_business_selected_users(data, cashback: dict, users: list):
    users_cashback_list = []
    for user in users:
        user_data = data[data['party_rk'] == user]

        for category, percent in cashback.items():
            user_data.loc[user_data['category'] == category, ['pred_sum', 'real_sum']] = \
                user_data.loc[user_data['category'] == category, ['pred_sum', 'real_sum']] * percent

        potentional_cashback = user_data.nlargest(3, 'real_sum')
        real_cashback = user_data.nlargest(3, 'pred_sum')

        users_cashback_list.append({'party_rk': user,
                                    'cashback_category_pred': real_cashback['category'].tolist(),
                                    'real_cashback': int(sum(real_cashback['real_sum'])),
                                    'potentional_cashback': int(sum(potentional_cashback['real_sum']))})

    return users_cashback_list

