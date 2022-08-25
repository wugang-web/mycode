import os
import xlwt
import pandas as pd


class csv_xlsx_tool():
    def def_style(self):
        style = xlwt.XFStyle()
        # 这部分设置字体
        font = xlwt.Font()
        # 字体
        font.name = u"宋体"
        # 设为粗体
        # font.bold = 'True '
        # 字号
        # font.size = '11'
        font.height = 20 * 11
        # 字体颜色
        # font.colour_index = 0x40
        style.font = font
        # 这部分设置居中格式
        alignment = xlwt.Alignment()
        # 水平居中
        # alignment.horz = xlwt.Alignment.HORZ_CENTER
        # 垂直居中
        alignment.vert = 0x01
        alignment.wrap = 1
        style.alignment = alignment

        # 设置背景颜色
        # ptn = xlwt.Pattern()
        # 设置背景色
        # ptn.pattern = xlwt.Pattern.SOLID_PATTERN
        # ptn.pattern_fore_colour = 0x40
        # style.pattern = ptn

        # 设置边框
        borders = xlwt.Borders()
        borders.left = 1
        borders.right = 1
        borders.top = 1
        borders.bottom = 1
        style.borders = borders
        return style

    def csv_to_xlsx(self, csvPath):
        """
        利用pandas将csv格式的文件转换成xlsx
        :param csvPath: csv文件的路径
        :return:
        """
        # 设置生成xlsx文件的路径
        toExcelPath = csvPath[:-4] + '.xlsx'

        data = pd.read_csv(csvPath, encoding='utf-8')
        #  index false为不写入索引
        data.to_excel(toExcelPath, index=False, encoding="gbk")

        # 判断csv文件是否存在，存在则删除
        if os.path.exists(csvPath):
            os.remove(csvPath)

    def xlsx_to_csv(self, xlsxPath):
        """
        利用pandas将xlsx格式的文件转换成csv
        :param xlsxPath: xlsx文件的路径
        :return:
        """
        # 设置生成csv文件的路径
        toCSVPath = xlsxPath[:-5] + '.csv'
        # 使用index_col=0，直接将第一列作为索引，不额外添加列。
        data = pd.read_excel(xlsxPath, index_col=0)
        data.to_csv(toCSVPath, encoding="utf-8")

    def list_to_xlsx(self, caselists, fileheader, xmind_file):

        workbook = xlwt.Workbook(encoding='utf-8')  # 设置一个workbook，其编码是utf-8
        worksheet = workbook.add_sheet("测试用例", cell_overwrite_ok=True)  # 新增一个sheet
        # python xlwt 解决报错：ValueError: More than 4094 XFs (styles) https://blog.csdn.net/weixin_35757704/article/details/116296515
        mystyle=self.def_style()
        # 创建表头
        for i in range(len(fileheader)):
            worksheet.write(0, i, label=fileheader[i], style=mystyle)  # 将‘列1’作为标题
            worksheet.set_panes_frozen(True)
            worksheet.set_horz_split_pos(1)  # 冻结首行
            if i < 4:
                worksheet.col(i).width = 256 * 40
            elif i == 5:
                worksheet.col(i).width = 256 * 30
            else:
                worksheet.col(i).width = 256 * 15
        for row in range(len(caselists)):
            for column in range(len(caselists[row])):
                worksheet.write(row + 1, column, label=caselists[row][column], style=mystyle)

        # 设置excel文件的名称和路径
        xlsx_file = xmind_file[:-6] + '(1).xlsx'
        if os.path.exists(xlsx_file):
            os.remove(xlsx_file)
        workbook.save(xlsx_file)
        return xlsx_file




if __name__ == '__main__':
    ...
