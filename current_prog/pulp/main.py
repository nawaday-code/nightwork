import tokaischeduling_PULPver3 as schedule
import os
def main():
    print(f'Root Dir is {os.getcwd()}')
    schedule.calc_schedule()

if __name__ == "__main__":
    main()