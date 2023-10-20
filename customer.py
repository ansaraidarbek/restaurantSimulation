import simpy
import random
from random import seed

def customer(env, name, restaurant, arrival_rate, **duration):
    while True:

        # change 1: customer arrival follows poisson distribution
#        yield env.timeout(random()*10)
        interarrival_time = random.expovariate(arrival_rate)
        yield env.timeout(interarrival_time)

        print(f'{name} enters the restaurant and for the waiter to come at {round(env.now, 2)}')
        with restaurant.request() as req:
            yield req

            print(f"Sits are available. {name} get sitted at {round(env.now, 2)}")
            yield env.timeout(duration['get_sitted'])

            print(f"{name} starts looking at the menu at {round(env.now, 2)}")
            yield env.timeout(duration['choose_food'])

            print(f'Waiters start getting the order from {name} at {round(env.now, 2)}')
            yield env.timeout(duration['give_order'])

            # change 2: food department from kitchen follows poisson distribution
            print(f'{name} starts waiting for food at {round(env.now, 2)}')
#            yield env.timeout(duration['wait_for_food'])
            serving_departure_rate = random.expovariate(1/duration['wait_for_food'])
            yield env.timeout(serving_departure_rate)

            print(f'{name} starts eating at {round(env.now, 2)}')
            yield env.timeout(duration['eat'])

            print(f'{name} starts paying at {round(env.now, 2)}')
            yield env.timeout(duration['pay'])

            print(f'{name} leaves at {round(env.now, 2)}')


seed(1)
env = simpy.Environment()

# Model restaurant that can only allow 2 customers at once
restaurant = simpy.Resource(env, capacity=4)
durations = {'get_sitted': 1, 'choose_food': 10, 'give_order': 5, 'wait_for_food': 20, 'eat': 45, 'pay': 10}


customer_arrival_rate = 10/60 # num customers per hour

for i in range(5):
    env.process(customer(env, f'Customer {i}', restaurant, customer_arrival_rate, **durations))

env.run(until=95)
