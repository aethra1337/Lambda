def is_triangle (line1, line2, line3):
    
    if (line1 + line2 > line3) and (line1 + line3> line2) and (line2 + line3 > line1):
        result = "possible"
    else:
        result = "not possible"
        
    return result

print(is_triangle(12, 5, 13))