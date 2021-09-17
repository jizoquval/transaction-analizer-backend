import asyncio
import re


def check_same_cashback_persent(cashback_categories):
    value = cashback_categories[0]
    if value == 0.03 or value == 0.05 or value == 0.1:
        for cashback in cashback_categories:
            if cashback != value:
                return False
        return True
    else:
        return False


def get_calculated_metric_for_all_usrs(persent, month):
    if month == 1:
        if persent == 0.03:
            return 


def metric_business_all_users_aproximate(data, unique_party_rk, cashback: dict, num_user: int = 4000):
    sample_users = unique_party_rk.sample(num_user, random_state=42)
    user_data = data.merge(sample_users, on='party_rk', how='inner')

    for category, percent in cashback.items():
        user_data.loc[user_data['category'] == category, ['pred_sum', 'real_sum']] = \
            user_data.loc[user_data['category'] == category,
                          ['pred_sum', 'real_sum']] * percent

#     for user in user_data['party_rk'].unique():
#         potentional_cashback_all_user_sum += sum(user_data[user_data['party_rk'] == user].nlargest(3,'real_sum')['real_sum'])
#         real_cashback_all_user_sum += sum(user_data[user_data['party_rk'] == user].nlargest(3,'pred_sum')['real_sum'])

    potentional_cashback_all_user_sum = int(sum(user_data.groupby(
        'party_rk')['real_sum'].apply(lambda grp: sum(grp.nlargest(3)))))
    real_cashback_all_user_sum = int(sum(user_data.groupby('party_rk').apply(
        lambda grp: sum(grp.nlargest(3, 'pred_sum')['real_sum']))))

    delta = potentional_cashback_all_user_sum - real_cashback_all_user_sum

    return {
        'real_cashback_all_user_sum': int(real_cashback_all_user_sum/num_user),
        'potentional_cashback_all_user_sum': int(potentional_cashback_all_user_sum/num_user),
        'delta': int(delta/num_user),
        'cashback_ratio': int(real_cashback_all_user_sum/potentional_cashback_all_user_sum * 100),
    }


async def metric_business_all_users(data, cashback: dict, users_count: int):
    user_data = calculate_cashback(data, cashback)

    potentional_cashback_all_user_sum_task = asyncio.create_task(
        calculate_potential_cashback(user_data))
    real_cashback_all_user_sum_task = asyncio.create_task(
        calculate_real_cashback(user_data))

    potentional_cashback_all_user_sum = await potentional_cashback_all_user_sum_task
    real_cashback_all_user_sum = await real_cashback_all_user_sum_task

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
                user_data.loc[user_data['category'] == category,
                              ['pred_sum', 'real_sum']] * percent

        potentional_cashback = user_data.nlargest(3, 'real_sum')
        real_cashback = user_data.nlargest(3, 'pred_sum')

        users_cashback_list.append({'party_rk': user,
                                    'cashback_category_pred': real_cashback['category'].tolist(),
                                    'real_cashback': int(sum(real_cashback['real_sum'])),
                                    'potentional_cashback': int(sum(potentional_cashback['real_sum']))})

    return users_cashback_list


def calculate_cashback(data, cashback: dict):
    user_data = data.copy()
    for category, percent in cashback.items():
        user_data.loc[user_data['category'] == category, ['pred_sum', 'real_sum']] = \
            user_data.loc[user_data['category'] == category,
                          ['pred_sum', 'real_sum']] * percent
    return user_data


async def calculate_potential_cashback(user_data):
    return int(
        sum(
            user_data.groupby('party_rk')['real_sum'].apply(
                lambda grp: grp.nlargest(3).sum())
        )
    )


async def calculate_real_cashback(user_data):
    return int(
        sum(
            user_data.groupby('party_rk').apply(
                lambda grp: grp.nlargest(3, 'pred_sum')['real_sum'].sum())
        )
    )
