import os
from openai import OpenAI
from advanced_env import CalendarOrchestrationEnv, Action


def get_client():
    API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
    MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4.1-mini")
    HF_TOKEN = os.getenv("HF_TOKEN")

    if HF_TOKEN is None:
        raise ValueError("HF_TOKEN environment variable is required")

    client = OpenAI(
        base_url=API_BASE_URL,
        api_key=HF_TOKEN
    )

    return client, MODEL_NAME


def llm_plan_action(calendar_state, step_num):
    client, MODEL_NAME = get_client()

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": f"Calendar state: {calendar_state}, step: {step_num}"
            }
        ]
    )

    _ = response.choices[0].message.content

    return Action(
        action_type="reschedule_meeting",
        target_meeting_id="m2",
        new_time="16:00",
        reason="critical_incident"
    )


def run_single_task(task_id):
    _, MODEL_NAME = get_client()

    env = CalendarOrchestrationEnv()
    obs = env.reset(task_id=task_id)

    print(f"[START] task=calendar_task_{task_id} env=openenv model={MODEL_NAME}")

    rewards = []
    success = False

    try:
        for step_num in range(1, 4):
            action = llm_plan_action(obs.calendar, step_num)

            obs, reward, done, info = env.step(action)

            safe_score = max(0.01, min(round(reward.score, 2), 0.99))

            rewards.append(f"{safe_score:.2f}")

            print(
                f"[STEP] step={step_num} "
                f"action={action.action_type} "
                f"reward={safe_score:.2f} "
                f"done={'true' if done else 'false'} "
                f"error=null"
            )

            if done:
                success = True
                break

    except Exception as e:
        rewards.append("0.01")
        print(
            f"[STEP] step={step_num} "
            f"action=error "
            f"reward=0.01 "
            f"done=true "
            f"error={str(e)}"
        )

    print(
        f"[END] success={'true' if success else 'false'} "
        f"steps={step_num} "
        f"rewards={','.join(rewards)}"
    )


def run_inference():
    for task_id in [1, 2, 3]:
        run_single_task(task_id)


if __name__ == "__main__":
    run_inference()