import os
import shutil


def move_file(src_dir, dst_dir):
    """
    移动文件
    :param src_dir: 源目录，str
    :param dst_dir: 目标目录，str
    :return:
    """
    fn = os.listdir(src_dir)
    fn = list(
        filter(lambda x: str(x).split(".")[-2][-1] != 'd', fn)
    )

    if not os.path.exists(dst_dir):
        os.mkdir(dst_dir)
    for f in fn:
        shutil.move(os.path.join(src_dir, f), os.path.join(dst_dir, f))

    print(f"move corresponding files from {src_dir} to {dst_dir}")


if __name__ == "__main__":
    move_file(r"D:\codeprograms\mybuilds\vtk9.0install\bin",
              r"D:\codeprograms\mybuilds\vtk9.0install\release_bin")
