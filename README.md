# Kaggle Competition: Lux AI 2021
## Absent Intelligence

### Contributors
- [Karthika Chermathurai]()
- [Lukas Alius]()
- [Taliah Horner](linkedin.com/in/taliahhorner)
- [Jim Walker](https://www.linkedin.com/in/thejimwalker)
- [Abishek Kargawi]()

Entry for the [Lux AI 2021 Kaggle Competition](https://www.kaggle.com/c/lux-ai-2021/)

## Rewards

`w()`: weight increasing as game continues

`d()`: distance

|Shit                    | Bad  |Fine   |Good   |Optimal   |
|---|---|---|---|---|
|w(o.cities > p.cities)  | worker--                  |road close to city   |collect resource   |City survives night   |
|                        | d(city,resources) = high  | cart ++             |  p.units > o.units | w(p.cities > o.cities)   |
|                        |                           |                     |  research++   | |
|                        |                           |                     |  d(city,resources) = low   | |
|                        |                           |                     |  worker++   | |
