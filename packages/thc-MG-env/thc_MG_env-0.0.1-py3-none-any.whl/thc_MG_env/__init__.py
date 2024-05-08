from gym.envs.registration import register

register(
    id='thc_MG_env-v0',
    entry_point='thc_MG_env.envs:HTCEnv',
    max_episode_steps=300,
)