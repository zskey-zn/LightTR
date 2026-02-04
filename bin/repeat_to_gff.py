#!/usr/bin/env python3
"""
repeat_to_gff.py - 将TRF .dat文件转换为GFF格式

描述:
    此程序读取TRF .dat文件，并将其转换为GFF3格式。

用法:
    python repeat_to_gff.py input.dat [--prefix STR] [--help]

示例:
    python repeat_to_gff.py rice.frag1M.fa.trf.dat
"""

import sys
import os
import re
import argparse
from typing import List, Tuple

def dat_to_gff3(input_file: str, prefix: str = None) -> None:
    """
    将TRF .dat文件转换为GFF3格式
    
    参数:
        input_file: TRF .dat文件路径
        prefix: 可选前缀，将添加到重复元素ID前
    """
    # 处理前缀
    pre_tag = f"{prefix}_" if prefix else ""
    
    # 输出文件名
    output_file = f"{input_file}.gff"
    
    # 计数器
    mark = 1
    current_chr = ""
    
    # 打开文件
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        # 写入GFF3头部
        outfile.write("##gff-version 3\n")
        
        for line in infile:
            line = line.strip()
            
            # 提取染色体/序列名
            if line.startswith("Sequence:"):
                # 提取序列名，去除"Sequence:"和可能的空格
                match = re.search(r'Sequence:\s*(\S+)', line)
                if match:
                    current_chr = match.group(1)
                continue
            
            # 跳过空行
            if not line:
                continue
            
            # 分割行，跳过可能的表头行
            fields = line.split()
            
            # 检查是否是有15个字段的数据行
            if len(fields) != 15:
                continue
            
            try:
                # 解析所需字段
                start = int(fields[0])
                end = int(fields[1])
                period_size = int(fields[2])
                copy_number = float(fields[3])
                percent_matches = int(fields[5])
                percent_indels = int(fields[6])
                score = float(fields[7])
                consensus = fields[13]
                
                # 生成唯一ID，格式化为6位数字
                element_id = f"{pre_tag}TR{mark:06d}"
                
                # 写入GFF3行
                # 格式: seqname source feature start end score strand frame attributes
                # 注: TRF不提供链信息，默认为"+"
                strand = "+"
                
                # 构建属性字段，只包含指定的6个属性
                attributes = (f"ID={element_id};PeriodSize={period_size};CopyNumber={copy_number};"
                             f"PercentMatches={percent_matches};PercentIndels={percent_indels};"
                             f"Consensus={consensus}")
                
                # 写入输出文件
                gff_line = (f"{current_chr}\tTRF\tTandemRepeat\t{start}\t{end}\t"
                           f"{score}\t{strand}\t.\t{attributes}\n")
                outfile.write(gff_line)
                
                # 增加计数器
                mark += 1
                
            except (ValueError, IndexError) as e:
                # 如果解析失败，跳过这一行
                sys.stderr.write(f"警告: 无法解析行，跳过: {line}\n")
                sys.stderr.write(f"错误信息: {str(e)}\n")
                continue
    
def count_lines(file_path: str) -> int:
    """计算文件行数"""
    try:
        with open(file_path, 'r') as f:
            return sum(1 for _ in f)
    except IOError:
        return 0

def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="将TRF .dat文件转换为GFF3格式",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
    python %(prog)s input.dat
    python %(prog)s input.dat --prefix Custom
        """
    )
    
    parser.add_argument(
        "input_file",
        help="TRF .dat格式的输入文件"
    )
    
    parser.add_argument(
        "--prefix",
        type=str,
        default="",
        help="设置重复元素ID的前缀"
    )
    
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="显示详细运行信息"
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version="repeat_to_gff.py v2.0"
    )
    
    # 解析参数
    args = parser.parse_args()
    
    # 检查输入文件是否存在
    if not os.path.exists(args.input_file):
        print(f"错误: 输入文件 '{args.input_file}' 不存在", file=sys.stderr)
        sys.exit(1)
    
    # 检查文件扩展名
    if not args.input_file.endswith('.dat'):
        print(f"警告: 输入文件 '{args.input_file}' 可能不是TRF .dat格式文件", file=sys.stderr)
        answer = input("是否继续? (y/n): ")
        if answer.lower() != 'y':
            sys.exit(0)
    
    if args.verbose:
        print(f"开始转换文件: {args.input_file}")
        print(f"使用前缀: '{args.prefix}'")
        line_count = count_lines(args.input_file)
        print(f"文件行数: {line_count}")
    
    try:
        # 执行转换
        dat_to_gff3(args.input_file, args.prefix)
        
        if args.verbose:
            print("转换成功!")
            
    except Exception as e:
        print(f"转换过程中出现错误: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
