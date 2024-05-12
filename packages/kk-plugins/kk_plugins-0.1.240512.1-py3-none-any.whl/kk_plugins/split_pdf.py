import os

from PyPDF2 import PdfReader, PdfWriter


class PdfSplit:
    def __split(self, src: str, dst: str, split_range: list):
        """
        分割PDF文件
        :param src: pdf文件路径
        :param dst: 分割后的pdf文件保存路径，路径到文件名
        :param split_range: 分割范围 [start, end]
        :return:
        """
        self.__init_path(src, dst)

        pdf_reader = PdfReader(src)

        pdf_writer = PdfWriter()
        if split_range[1] == -1 or split_range[1] > len(pdf_reader.pages):
            split_range[1] = len(pdf_reader.pages)

        for i in range(int(split_range[0]), int(split_range[1])):
            pdf_writer.add_page(pdf_reader.pages[i])

        if not dst.endswith(".pdf"):
            dst += ".pdf"

        with open(dst, 'wb') as out:
            pdf_writer.write(out)

    def __init_path(self, src: str, dst: str):
        """
        初始化路径
        :param src: pdf文件路径
        :param dst:
        :return:
        """
        if not os.path.exists(src):
            print("文件不存在")
            return

        dst_folder = os.path.dirname(dst)
        if not os.path.exists(dst_folder) and dst_folder != "":
            os.makedirs(dst_folder)

    def __read_pdf_bookmarks(self, src: str):
        """
        读取PDF文件的书签
        :param src: pdf文件路径
        :return: 返回书签列表，每个元素是一个字典，包含页码和标题，如 {'page': 1, 'title': '第一页'}
        """
        result = []
        with open(src, 'rb') as file:
            reader = PdfReader(file)
            bookmarks = reader.outline
            for bookmark in bookmarks:
                # 获取书签的标题
                title = bookmark['/Title']
                # 获取书签的页码
                page = reader.get_destination_page_number(bookmark) + 1
                result.append({'page': page, 'title': title})
        return result

    def split(self, src: str):
        """
        分割PDF文件
        :param src: pdf文件路径
        :return:
        """
        if not os.path.exists(src):
            print("文件不存在")
            return

        # 获取pdf的文件名,创建同名文件夹
        pdf_name = os.path.basename(src).split('.')[0]
        pdf_dir = os.path.join(os.path.dirname(src), pdf_name)
        if not os.path.exists(pdf_dir):
            os.makedirs(pdf_dir)

        bookmarks = self.__read_pdf_bookmarks(src)
        if len(bookmarks) == 0:
            print("没有找到书签")
            return

        # 对书签按页码排序
        bookmarks = sorted(bookmarks, key=lambda x: x['page'])
        # 分割pdf，每个书签到下一个书签之间的内容为一个pdf
        for i, bookmark in enumerate(bookmarks):
            title = bookmark['title']
            page = bookmark['page']
            if i == 0:
                start = 0
            else:
                start = bookmarks[i]['page'] - 1
            if i == len(bookmarks) - 1:
                end = -1
            else:
                end = bookmarks[i + 1]['page'] - 1
            dst_pdf_path = os.path.join(pdf_dir, f"{title}.pdf")
            # 如果文件已经存在，则文件名后加上序号
            if os.path.exists(dst_pdf_path):
                dst_pdf_path = os.path.join(pdf_dir, f"{title}_{i}.pdf")
            self.__split(src, dst_pdf_path, [start, end])


# sp = PdfSplit()
# sp.split('xxx.pdf')
