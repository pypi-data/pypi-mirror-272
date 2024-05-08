from gym.envs.registration import register

register(
    id='thc_MG_env-v0',
    entry_point='thc_MG_env.envs.env_thc:TwohoirzontalcartEnv_chen',
    max_episode_steps=300,
)