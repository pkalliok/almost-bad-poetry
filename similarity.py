
def rhythm_distance(target, sample):
    return min(raw_rhythm_dist(target, sample),
            raw_rhythm_dist([(0.0, 0.0)] + target, sample),
            raw_rhythm_dist([(1.0, 0.0), (0.0, 0.0)] + target, sample)) \
        / len(target)

def raw_rhythm_dist(target, sample):
    if len(target) == 0: return len(sample)
    if len(sample) == 0: return len(target)
    tg1_w, tg1_len = target[0]
    s1_w, s1_len = sample[0]
    try: tg2_w, tg2_len = target[1]
    except IndexError: tg2_w, tg2_len = 0.0, 0.0
    try: s2_w, s2_len = sample[1]
    except IndexError: s2_w, s2_len = 0.0, 0.0
    l1_d = len_dist(tg1_len, s1_len)
    l2_d = len_dist(tg1_len, s1_len + s2_len)
    l3_d = len_dist(tg1_len + tg2_len, s1_len)
    if l1_d <= l2_d and l1_d <= l3_d:
        rest_d = l1_d / 2.0 + raw_rhythm_dist(target[1:], sample[1:])
    elif l2_d <= l3_d:
        rest_d = l2_d / 2.0 + weight_dist(0.0, s2_w) \
                + raw_rhythm_dist(target[1:], sample[2:])
    else:
        rest_d = l3_d / 2.0 + weight_dist(0.0, tg2_w) \
                + raw_rhythm_dist(target[2:], sample[1:])
    return weight_dist(tg1_w, s1_w) + rest_d

weight_dist = len_dist = lambda a, b: (a-b)*(a-b)

syl_weights = [0.1, 0.3, 0.9]
part_weights = [0.2, 0.5, 0.3]

def rhyming_dist(target, sample):
    return sum((part1 != part2) * syl_weight * part_weight
            for syl_weight, syl1, syl2 in zip(syl_weights, target, sample)
            for part_weight, part1, part2 in zip(part_weights, syl1, syl2))
