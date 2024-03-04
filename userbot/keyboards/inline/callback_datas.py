from aiogram.utils.callback_data import CallbackData

start_kb_callback = CallbackData("start", "button")
choose_module_callback = CallbackData("choose_module", "module_id", "course_id", "pos", "temp")
choose_homework_callback = CallbackData("choose_homework", "homework_id", "pos", "temp")
choose_lesson_callback = CallbackData("choose_lesson", "lesson_id", "pos", "temp")
choose_answer_callback = CallbackData("choose_answer", "chosen", "qtype", "size", "right_answers", "homework_id")
settings_user_callback = CallbackData("user_settings", "button")
yes_no_callback = CallbackData("yes_no", "res", "student_id")

admin_kb_callback = CallbackData("admin", "button")
settings_admin_callback = CallbackData("admin_settings", "button")
choose_access_callback = CallbackData("choose_access", "chosen")
choose_group_callback = CallbackData("choose_group", "groups", "group_id", "pos", "temp")