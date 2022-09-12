# 计算矩形的重叠面积


def overlap_area(r1, r2):
    """
    给定两个矩形r1, r2，计算二者的重叠面积。矩形用左上角和右下角的顶点坐标表示。坐标轴原点为左上角。注意：矩形的边与坐标轴平行
    :param r1: 矩形1。表示为[(x1, y1), (x2, y2)]
    :param r2: 矩形1。表示为[(x3, y3), (x4, y4)]
    :return: 重叠面积
    """
    def cal_overlap_len(line1, line2):
        """
        计算两条平行直线line1, line2的重叠长度。直线表示为(x1, x2)。注意：平行于坐标轴的直线
        :param line1: 直线1
        :param line2: 直线2
        :return: 重叠的长度
        """
        a, b = line1
        c, d = line2
        a, b = min(a, b), max(a, b)
        c, d = min(c, d), max(c, d)
        if a > c:
            a, b, c, d = c, d, a, b

        if b <= c:
            return 0

        if b >= d:
            return d - c
        else:
            return b - c

    x_overlap_len = cal_overlap_len([r1[0][0], r1[1][0]], [r2[0][0], r2[1][0]])
    y_overlap_len = cal_overlap_len([r1[0][1], r1[1][1]], [r2[0][1], r2[1][1]])

    return x_overlap_len * y_overlap_len


if __name__ == "__main__":
    r1 = [(1, 1), (2, 2)]
    r2 = [(2, 2), (2.5, 2.5)]

    area = overlap_area(r1, r2)

    print(f"Overlap area of r1({r1}) and r2({r2}) is : {area}")
