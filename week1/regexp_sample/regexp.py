def calculate(data, findall):
    matches = findall(r"([abc])([+-]?)=([abc])?([+-]?\d+)?") # Если придумать хорошую регулярку, будет просто
    for v1, sign, v2, number in matches:
        right = data.get(v2, 0) + int(number or 0)
        if sign == "-":
            data[v1] -= right
        elif sign == "+":
            data[v1] += right
        else:
            data[v1] = right
        
    return data
