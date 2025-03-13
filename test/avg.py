ecs_qb_t =  [0.026, 0.508, 0.990, 1.472, 1.953, 2.435, 2.917, 3.398, 3.880, 4.362, 4.844]
ecs_qb_q = [1, 38, 101, 30, 1, 4, 2, 2, 2, 8, 10, 3]

ecs_ar_t =  [ 0.030, 0.543, 1.056, 1.569, 2.083, 2.596, 3.109, 3.622, 4.135, 4.648, 5.161 ]
ecs_ar_q =  [1, 71, 86, 9, 4, 4, 7, 8, 3, 5, 2]

lf_qb_t = [ 0.040, 0.185, 0.329, 0.474, 0.618, 0.763, 0.907, 1.052, 1.196, 1.341, 1.485 ]
lf_qb_q = [ 1, 142, 8, 2, 3, 7, 17, 14, 3, 1, 2 ]

lf_ar_t = [ 0.043, 0.348, 0.653, 0.958, 1.263, 1.568, 1.873, 2.178, 2.483, 2.788, 3.093 ]
lf_ar_q =  [ 1, 149, 0, 0, 0, 0, 0, 0, 0, 18, 32 ]

lc_qb_t=  [ 0.048, 0.156, 0.264, 0.372, 0.480, 0.588, 0.697, 0.805, 0.913, 1.021, 1.129 ]
lc_qb_q =  [ 1, 138, 9, 0, 5, 8, 4, 5, 12, 15, 3 ]

lc_ar_t = [ 0.041, 0.127, 0.212, 0.298, 0.384, 0.469, 0.555, 0.641, 0.727, 0.812, 0.898 ]
lc_ar_q =  [ 1, 140, 8, 0, 10, 9, 13, 0, 1, 9, 9 ]

def avg_time(t, q):
	return sum([t[i] * q[i] for i in range(len(t))]) / sum(q)

print("Average time for ECS query builder: ", avg_time(ecs_qb_t, ecs_qb_q))
print("Average time for ECS active record: ", avg_time(ecs_ar_t, ecs_ar_q))
print("Average time for Lambda a freddo query builder: ", avg_time(lf_qb_t, lf_qb_q))
print("Average time for Lambda a freddo active record: ", avg_time(lf_ar_t, lf_ar_q))
print("Average time for Lambda a caldo query builder: ", avg_time(lc_qb_t, lc_qb_q))
print("Average time for Lambda a caldo active record: ", avg_time(lc_ar_t, lc_ar_q))