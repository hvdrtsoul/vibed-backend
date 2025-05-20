from celery import shared_task

@shared_task
def reward_user_async(user_id, tokens):
    from streaming.views import reward_user_with_tokens
    reward_user_with_tokens(user_id, tokens)
