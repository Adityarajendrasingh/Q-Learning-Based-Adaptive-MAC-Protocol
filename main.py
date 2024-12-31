import config
from run import run
from simulation import run_multiple_simulations
from token_mac import run_token_simulation
import matplotlib.pyplot as plt

def q_learn_run():
    throuput = []
    Arrival = []  # To store reqNO values
    succ_ene = []
    fail_ene = []
    delay = []

    for reqNO in range(4, 100, 16):
        # Run the simulation with the current reqNO
        rewards, window_size, through, failure, success = run(500, 100, reqNO)

        # Calculate averages
        avg_rewards = sum(rewards) / len(rewards)
        avg_window_size = sum(window_size) / len(window_size)
        avg_through = sum(through) / len(through)
        avg_ene_succ = sum(success)/len(success)
        avg_ene_fail = sum(failure)/len(failure)

        d = avg_window_size * config.SLOT_DURATION
        delay.append(d)
        # Store the current reqNO and avg_through for plotting
        Arrival.append(reqNO)
        throuput.append(avg_through)
        succ_ene.append(avg_ene_succ)
        fail_ene.append(avg_ene_fail)

        # Print results for the current reqNO
        print(f"Arrival Rate: {reqNO}")
        print(f"  Average Rewards: {avg_rewards}")
        print(f"  Average Window Size: {avg_window_size}")
        print(f"  Average Throughput: {avg_through}")
        print(f"  Average ene succ: {avg_ene_succ}")
        print(f"  Average ene fail: {avg_ene_fail}")
        print(f"  Delay: {d}")

    return throuput, Arrival, succ_ene, fail_ene, delay

def hybrid_mac(window):
    throuput = []
    fail = []
    succ = []
    delay = []
    print(f"Hybrid Mac size {window}")
    for reqNO in range(4, 100, 16):
        coll_slot, succ_slot, idle_slot, avg_send, thr, fail_ene, succ_ene = run_multiple_simulations(reqNO, window, 5, 0.05)
        throuput.append(thr)
        fail.append(fail_ene)
        succ.append(succ_ene)
        d = window * config.SLOT_DURATION
        delay.append(d)
        print(f"Arrival Rate: {reqNO}")
        print(f"Throughput: {thr}")
        print(f"fail: {fail_ene}")
        print(f"Succ: {succ_ene}")
        print(f"Delay: {d}")

    return throuput, fail, succ, delay

def token(window):
    throuput = []
    fail = []
    succ = []
    delay = []
    print(f"Token MAC size {window}")
    for reqNO in range(4, 100, 16):
        sent, failed, avg_delay = run_token_simulation(sim_time=500, num_nodes=10, slot_duration=config.SLOT_DURATION, window_size=window)
        throuput.append(sent / 500)  # Normalize throughput
        fail.append(failed)
        succ.append(sent)
        delay.append(avg_delay)
        print(f"Arrival Rate: {reqNO}")
        print(f"Throughput: {sent / 500}")
        print(f"Fail Energy: {failed}")
        print(f"Success Energy: {sent}")
        print(f"Delay: {avg_delay}")

    return throuput, fail, succ, delay


if __name__ == "__main__":
    throuput_request,Arrival_Rate, succ_ene, fail_ene, delay = q_learn_run()  # To store reqNO values
    throuput_request_4, fail_ene_4, succ_ene_4, delay_4 = hybrid_mac(4)
    throuput_request_8, fail_ene_8, succ_ene_8, delay_8 = hybrid_mac(8)
    throuput_request_12, fail_ene_12, succ_ene_12, delay_12 = hybrid_mac(12)
    throuput_request_16, fail_ene_16, succ_ene_16, delay_16 = hybrid_mac(16)
    throuput_request_20, fail_ene_20, succ_ene_20, delay_20 = hybrid_mac(20)
    throuput_request_24, fail_ene_24, succ_ene_24, delay_24 = hybrid_mac(24)
    throuput_request_28, fail_ene_28, succ_ene_28, delay_28 = hybrid_mac(28)
    throuput_request_32, fail_ene_32, succ_ene_32, delay_32 = hybrid_mac(32)

    # throuput_request_token_4, fail_ene_token_4, succ_ene_token_4, delay_token_4 = token(4)
    # throuput_request_token_8, fail_ene_token_8, succ_ene_token_8, delay_token_8 = token(8)
    # throuput_request_token_12, fail_ene_token_12, succ_ene_token_12, delay_token_12 = token(12)
    # throuput_request_token_16, fail_ene_token_16, succ_ene_token_16, delay_token_16 = token(16)
    # throuput_request_token_20, fail_ene_token_20, succ_ene_token_20, delay_token_20 = token(20)
    # throuput_request_token_24, fail_ene_token_24, succ_ene_token_24, delay_token_24 = token(24)
    # throuput_request_token_28, fail_ene_token_28, succ_ene_token_28, delay_token_28 = token(28)
    # throuput_request_token_32, fail_ene_token_32, succ_ene_token_32, delay_token_32 = token(32)

    plt.figure(figsize=(12, 8))

    # Q-Learning throughput
    plt.plot(Arrival_Rate, throuput_request, marker='o', linestyle='-', label='Q-Learning')

    # Hybrid MAC throughput for different window sizes
    plt.plot(Arrival_Rate, throuput_request_4, marker='x', linestyle='--', label='Hybrid MAC (Window=4)')
    plt.plot(Arrival_Rate, throuput_request_8, marker='s', linestyle='-.', label='Hybrid MAC (Window=8)')
    plt.plot(Arrival_Rate, throuput_request_12, marker='^', linestyle=':', label='Hybrid MAC (Window=12)')
    plt.plot(Arrival_Rate, throuput_request_16, marker='d', linestyle='-', label='Hybrid MAC (Window=16)')
    plt.plot(Arrival_Rate, throuput_request_20, marker='h', linestyle='--', label='Hybrid MAC (Window=20)')
    plt.plot(Arrival_Rate, throuput_request_24, marker='*', linestyle='-.', label='Hybrid MAC (Window=24)')
    plt.plot(Arrival_Rate, throuput_request_28, marker='v', linestyle=':', label='Hybrid MAC (Window=28)')
    plt.plot(Arrival_Rate, throuput_request_32, marker='P', linestyle='dotted', label='Hybrid MAC (Window=32)')

    # Token MAC throughput for different window sizes
    # plt.plot(Arrival_Rate, throuput_request_token_4, marker='<', linestyle='--', label='Token MAC (Window=4)')
    # plt.plot(Arrival_Rate, throuput_request_token_8, marker='>', linestyle='-.', label='Token MAC (Window=8)')
    # plt.plot(Arrival_Rate, throuput_request_token_12, marker='1', linestyle=':', label='Token MAC (Window=12)')
    # plt.plot(Arrival_Rate, throuput_request_token_16, marker='2', linestyle='-', label='Token MAC (Window=16)')
    # plt.plot(Arrival_Rate, throuput_request_token_20, marker='3', linestyle='--', label='Token MAC (Window=20)')
    # plt.plot(Arrival_Rate, throuput_request_token_24, marker='4', linestyle='-.', label='Token MAC (Window=24)')
    # plt.plot(Arrival_Rate, throuput_request_token_28, marker='8', linestyle=':', label='Token MAC (Window=28)')
    # plt.plot(Arrival_Rate, throuput_request_token_32, marker='+', linestyle='dotted', label='Token MAC (Window=32)')

    # Set graph attributes
    plt.title('Throughput vs Arrival Rate for Different Methods')
    plt.xlabel('Arrival Rate')
    plt.ylabel('Average Throughput')
    plt.grid(True)
    plt.legend()
    plt.show()

    # Plot graphs for fail_ene, succ_ene, and delay
    plt.figure(figsize=(12, 8))

    # Fail energy graph
    plt.plot(Arrival_Rate, fail_ene, marker='o', linestyle='-', label='Q-Learning Fail Energy')
    plt.plot(Arrival_Rate, fail_ene_4, marker='x', linestyle='--', label='Hybrid MAC Fail Energy (Window=4)')
    plt.plot(Arrival_Rate, fail_ene_8, marker='s', linestyle='-.', label='Hybrid MAC Fail Energy (Window=8)')
    plt.plot(Arrival_Rate, fail_ene_12, marker='^', linestyle=':', label='Hybrid MAC Fail Energy (Window=12)')
    plt.plot(Arrival_Rate, fail_ene_16, marker='d', linestyle='-', label='Hybrid MAC Fail Energy (Window=16)')
    plt.plot(Arrival_Rate, fail_ene_20, marker='h', linestyle='--', label='Hybrid MAC Fail Energy (Window=20)')
    plt.plot(Arrival_Rate, fail_ene_24, marker='*', linestyle='-.', label='Hybrid MAC Fail Energy (Window=24)')
    plt.plot(Arrival_Rate, fail_ene_28, marker='v', linestyle=':', label='Hybrid MAC Fail Energy (Window=28)')
    plt.plot(Arrival_Rate, fail_ene_32, marker='p', linestyle='dotted', label='Hybrid MAC (Window=32)')

    # plt.plot(Arrival_Rate, fail_ene_token_4, marker='1', linestyle='--', label='Token MAC (Window=4)')
    # plt.plot(Arrival_Rate, fail_ene_token_8, marker='2', linestyle='-.', label='Token MAC (Window=8)')
    # plt.plot(Arrival_Rate, fail_ene_token_12, marker='3', linestyle=':', label='Token MAC (Window=12)')
    # plt.plot(Arrival_Rate, fail_ene_token_16, marker='4', linestyle='-', label='Token MAC (Window=16)')
    # plt.plot(Arrival_Rate, fail_ene_token_20, marker='5', linestyle='--', label='Token MAC (Window=20)')
    # plt.plot(Arrival_Rate, fail_ene_token_24, marker='6', linestyle='-.', label='Token MAC (Window=24)')
    # plt.plot(Arrival_Rate, fail_ene_token_28, marker='7', linestyle=':', label='Token MAC (Window=28)')
    # plt.plot(Arrival_Rate, fail_ene_token_32, marker='8', linestyle='dotted', label='Token MAC (Window=32)')

    # Set graph attributes for fail energy
    plt.title('Fail Energy vs Arrival Rate for Different Methods')
    plt.xlabel('Arrival Rate')
    plt.ylabel('Fail Energy')
    plt.grid(True)
    plt.legend()
    plt.show()

    # Succ energy graph
    plt.figure(figsize=(12, 8))

    plt.plot(Arrival_Rate, succ_ene, marker='o', linestyle='-', label='Q-Learning Succ Energy')
    plt.plot(Arrival_Rate, succ_ene_4, marker='x', linestyle='--', label='Hybrid MAC Succ Energy (Window=4)')
    plt.plot(Arrival_Rate, succ_ene_8, marker='s', linestyle='-.', label='Hybrid MAC Succ Energy (Window=8)')
    plt.plot(Arrival_Rate, succ_ene_12, marker='^', linestyle=':', label='Hybrid MAC Succ Energy (Window=12)')
    plt.plot(Arrival_Rate, succ_ene_16, marker='d', linestyle='-', label='Hybrid MAC Succ Energy (Window=16)')
    plt.plot(Arrival_Rate, succ_ene_20, marker='h', linestyle='--', label='Hybrid MAC Succ Energy (Window=20)')
    plt.plot(Arrival_Rate, succ_ene_24, marker='*', linestyle='-.', label='Hybrid MAC Succ Energy (Window=24)')
    plt.plot(Arrival_Rate, succ_ene_28, marker='v', linestyle=':', label='Hybrid MAC Succ Energy (Window=28)')
    plt.plot(Arrival_Rate, succ_ene_32, marker='p', linestyle='dotted', label='Hybrid MAC (Window=32)')

    # plt.plot(Arrival_Rate, succ_ene_token_4, marker='1', linestyle='--', label='Token MAC (Window=4)')
    # plt.plot(Arrival_Rate, succ_ene_token_8, marker='2', linestyle='-.', label='Token MAC (Window=8)')
    # plt.plot(Arrival_Rate, succ_ene_token_12, marker='3', linestyle=':', label='Token MAC (Window=12)')
    # plt.plot(Arrival_Rate, succ_ene_token_16, marker='4', linestyle='-', label='Token MAC (Window=16)')
    # plt.plot(Arrival_Rate, succ_ene_token_20, marker='5', linestyle='--', label='Token MAC (Window=20)')
    # plt.plot(Arrival_Rate, succ_ene_token_24, marker='6', linestyle='-.', label='Token MAC (Window=24)')
    # plt.plot(Arrival_Rate, succ_ene_token_28, marker='7', linestyle=':', label='Token MAC (Window=28)')
    # plt.plot(Arrival_Rate, succ_ene_token_32, marker='8', linestyle='dotted', label='Token MAC (Window=32)')

    # Set graph attributes for succ energy
    plt.title('Succ Energy vs Arrival Rate for Different Methods')
    plt.xlabel('Arrival Rate')
    plt.ylabel('Succ Energy')
    plt.grid(True)
    plt.legend()
    plt.show()

    # Delay graph
    plt.figure(figsize=(12, 8))

    plt.plot(Arrival_Rate, delay, marker='o', linestyle='-', label='Q-Learning Delay')
    plt.plot(Arrival_Rate, delay_4, marker='x', linestyle='--', label='Hybrid MAC Delay (Window=4)')
    plt.plot(Arrival_Rate, delay_8, marker='s', linestyle='-.', label='Hybrid MAC Delay (Window=8)')
    plt.plot(Arrival_Rate, delay_12, marker='^', linestyle=':', label='Hybrid MAC Delay (Window=12)')
    plt.plot(Arrival_Rate, delay_16, marker='d', linestyle='-', label='Hybrid MAC Delay (Window=16)')
    plt.plot(Arrival_Rate, delay_20, marker='h', linestyle='--', label='Hybrid MAC Delay (Window=20)')
    plt.plot(Arrival_Rate, delay_24, marker='*', linestyle='-.', label='Hybrid MAC Delay (Window=24)')
    plt.plot(Arrival_Rate, delay_28, marker='v', linestyle=':', label='Hybrid MAC Delay (Window=28)')
    plt.plot(Arrival_Rate, delay_32, marker='p', linestyle='dotted', label='Hybrid MAC (Window=32)')

    # plt.plot(Arrival_Rate, delay_token_4, marker='1', linestyle='--', label='Token MAC (Window=4)')
    # plt.plot(Arrival_Rate, delay_token_8, marker='2', linestyle='-.', label='Token MAC (Window=8)')
    # plt.plot(Arrival_Rate, delay_token_12, marker='3', linestyle=':', label='Token MAC (Window=12)')
    # plt.plot(Arrival_Rate, delay_token_16, marker='4', linestyle='-', label='Token MAC (Window=16)')
    # plt.plot(Arrival_Rate, delay_token_20, marker='5', linestyle='--', label='Token MAC (Window=20)')
    # plt.plot(Arrival_Rate, delay_token_24, marker='6', linestyle='-.', label='Token MAC (Window=24)')
    # plt.plot(Arrival_Rate, delay_token_28, marker='7', linestyle=':', label='Token MAC (Window=28)')
    # plt.plot(Arrival_Rate, delay_token_32, marker='8', linestyle='dotted', label='Token MAC (Window=32)')

    # Set graph attributes for delay
    plt.title('Delay vs Arrival Rate for Different Methods')
    plt.xlabel('Arrival Rate')
    plt.ylabel('Delay')
    plt.grid(True)
    plt.legend()
    plt.show()