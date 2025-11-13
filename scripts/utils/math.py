import math

def round_to_significant_figures(num, sig_figs=2):
    if num == 0:
        return 0
    return round(num, sig_figs - int(math.floor(math.log10(abs(num)))) - 1)

def divide_number(n, parts):
    base = n // parts
    remainder = n % parts

    result = [base] * parts

    for i in range(remainder):
        result[i] += 1

    return result