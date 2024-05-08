from pandas import DataFrame
import cooler
import os


def icing(bin_values, axis_size):
    has_non_zero = False
    for v in bin_values:
        if v != 0:
            has_non_zero = True
            break
    if not has_non_zero:
        return bin_values
    bins = DataFrame(
        data={
            "chrom": ["chr1" for _ in range(axis_size)],
            "start": [i * 10 for i in range(axis_size)],
            "end": [(i + 1) * 10 for i in range(axis_size)],
        }
    )
    pixels = DataFrame(
        data={
            "bin1_id": [i // axis_size for i in range(len(bin_values))],
            "bin2_id": [i % axis_size for i in range(len(bin_values))],
            "count": bin_values,
        }
    )
    print("cooler_interface, axis_size:", axis_size)
    cooler.create_cooler(
        ".tmp.cooler", bins, pixels, symmetric_upper=False, triucheck=False
    )
    clr = cooler.Cooler(".tmp.cooler")
    bias, stats = cooler.balance_cooler(clr)
    ret = []
    for i, v in enumerate(bin_values):
        ret.append(v * bias[i // axis_size] * bias[i % axis_size])
    os.remove(".tmp.cooler")
    return ret
