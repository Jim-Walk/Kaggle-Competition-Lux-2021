from kaggle_environments import make

# run another match but with our empty agent
env = make("lux_ai_2021", configuration={"seed": 562124210, "loglevel": 2},
           debug=True)
steps = env.run(["./agent.py", "./agent.py"])

env.render(mode="ipython", width=1000, height=800)
