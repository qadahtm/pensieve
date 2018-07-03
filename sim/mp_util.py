NUM_AGENTS=8

S_INFO = 6  # bit_rate, buffer_size, next_chunk_size, bandwidth_measurement(throughput and time), chunk_til_video_end
S_LEN = 8  # take how many frames in the past
# A_DIM = 6
VIDEO_BIT_RATE = [300,750,1200,1850,2850,4300]  # Kbps
LTE_PERCS = [0.0,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,\
             0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95,1.0] # LTE percentages

# LTE_MU = 5000
LTE_MU = 0
LAMBDA = [100000,10000,1000,100,10,1]

ACTIONS = []
for i in range(len(VIDEO_BIT_RATE)):
    for j in range(len(LTE_PERCS)):
        a = {}
        a['q'] = i
        a['lte'] = LTE_PERCS[j]
        ACTIONS.append(a)

A_DIM = len(ACTIONS)
Q_DIM = len(VIDEO_BIT_RATE)
LTE_DIM = len(LTE_PERCS)

MP_ENABLED=True

# REBUF_PENALTY = 4.3  # 1 sec rebuffering -> 3 Mbps
REBUF_PENALTY = 1000000  # 1 sec rebuffering -> 3 Mbps

## Environment
MILLISECONDS_IN_SECOND = 1000.0
LTE_BUFFER_THRESH = 60.0 * MILLISECONDS_IN_SECOND  # millisec, max buffer limit
WIFI_LINK_RTT = 80  # millisec
LTE_LINK_RTT = 80  # millisec

def log_debug(msg, log_file):
    # log_file.write("DEBUG: {}\n".format(msg))
    # log_file.flush()
    return False;

def reward_rate(a_i):
    res = 0
    br_i = a_i['q']
    for i in range(len(VIDEO_BIT_RATE)):
        res = res + (LAMBDA[i] * VIDEO_BIT_RATE[i])
        if br_i == i:
            break
    return res

def compute_reward(bit_rate, rebuf, video_chunk_size, log_file):
    rate = reward_rate(ACTIONS[bit_rate])
    rebuf_pen = REBUF_PENALTY * rebuf
    lte_usage = (ACTIONS[bit_rate])['lte']
    lte_pen = (LTE_MU * (video_chunk_size * (lte_usage)))
    reward = rate - rebuf_pen - lte_pen
    log_debug(
        "rate={}, i={}, size={}, lte_usage={}, rebuf_pen={}, lte_pen={}, reward={}".format(rate, bit_rate,
                                                                                           video_chunk_size,
                                                                                           lte_usage, lte_pen,
                                                                                           rebuf_pen, reward),
        log_file)
    return  reward

