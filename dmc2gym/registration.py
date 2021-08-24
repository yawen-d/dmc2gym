# ADDED BY Yawen Duan (https://github.com/kmdanielduan) to be able to 
# move the registration process in __init__.py to registration.py

"""Helper functions for dm_control environment registrations"""

import gym
from gym.envs.registration import register as gym_reg


def register_suite(
    suite_module,
    tag=None,
    **register_kwargs,
):
    """Register all environments in a dm_control based suite with tag"""
    assert hasattr(suite_module, "load"), f"{suite_module} doesn't have load() attribute."

    for domain_name, task_name in suite_module._get_tasks(tag):
        register_env(suite_module, domain_name, task_name, **register_kwargs)


def register_env(
        # a suite module that contains load() function that returns a dm_control.rl.control.Environment object
        suite_module,
        # dm_control env kwargs
        domain_name,
        task_name,
        task_kwargs=None,
        environment_kwargs=None,
        visualize_reward=False,
        # step_kwargs
        frame_skip=1,
        from_pixels=False,
        # render_kwargs
        height=84,
        width=84,
        camera_id=0,
        # observation_kwargs
        channels_first=True,
        # others
        # TODO(yawen): build a unit test of fixed horizon to check which of 
        # time_limit and episode_length actually have effects on episode length
        episode_length=1000 
):
    """Register a single dm_control based environment by identifier (domain_name, task_name)"""
    assert hasattr(suite_module, "load"), f"{suite_module} doesn't have load() attribute."
    env_id = 'DMC/%s-%s-v0' % (domain_name, task_name)

    if from_pixels:
        assert not visualize_reward, 'cannot use visualize reward when learning from pixels'

    # shorten episode length
    max_episode_steps = (episode_length + frame_skip - 1) // frame_skip

    # we hope each environment can only be registered once, flag error when it's registered multiple times
    assert env_id not in gym.envs.registry.env_specs, f"Environment {env_id} already in in gym.envs.registry.env_specs"
    gym_reg(
        id=env_id,
        entry_point='dmc2gym.wrappers:DMCWrapper',
        kwargs=dict(
            # suite module
            suite_module=suite_module, 
            # env kwargs
            domain_name=domain_name,
            task_name=task_name,
            task_kwargs=task_kwargs,
            environment_kwargs=environment_kwargs,
            visualize_reward=visualize_reward,
            # step_kwargs
            frame_skip=frame_skip,
            from_pixels=from_pixels,
            # render_kwargs
            height=height,
            width=width,
            camera_id=camera_id,
            # observation_kwargs
            channels_first=channels_first,
        ),
        max_episode_steps=max_episode_steps,
    )