from LiteVkApi import Vk
from all_json import SETTINGS
import periods


keyboard_schema = [{"Сколько минут до звонка?": "2"}]


def is_member(user_id, vk_session):
    return vk_session.VkMethod("groups.isMember",
                               {"group_id": SETTINGS["group_id"], "user_id": user_id})


def get_text_time():
    now_time = periods.get_now_time()
    period = periods.get_period(now_time)
    if period:
        remaining_time = periods.get_time_to_period_finish(now_time, period)
        if period.period_type == periods.LESSON:
            text = f"""Сейчас {period.number} урок.\nДо звонка {remaining_time.seconds // 60} минут."""
        elif period.period_type == periods.BREAK:
            text = f"""Сейчас перемена.\nСледующий урок {period.number + 1}-й.\nДо звонка {remaining_time.seconds // 60} минут."""

        return text
    else:
        return "До уроков еще далеко :)"


def get_answer(message, user_id, vk_session):
    if not is_member(user_id, vk_session):
        return "Упс! Походу ты не подписан на группу. Подпишись и возвращайся :)"
    return get_text_time()


def main():
    while True:
        vk_session = Vk.login(SETTINGS['group_id'], SETTINGS['token'])

        keyboard = vk_session.new_keyboard(keyboard_schema)

        try:
            while True:
                if vk_session.check_new_msg():
                    event = vk_session.get_event()
                    message, user_id = event.text, event.user_id

                    text = get_answer(message, user_id, vk_session)
                    vk_session.send_keyboard(keyboard, user_id, text)

        except Exception as e:
            print(e)


if __name__ == '__main__':
    main()
