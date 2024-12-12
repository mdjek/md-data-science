from pandas import ExcelFile
import pandas as pd

def get_data_frame(file_to_path: str, sheet_name: str, with_strats = False):
    xlsx = ExcelFile(file_to_path)
    df = pd.read_excel(xlsx, sheet_name=sheet_name)
    
    first_row_num = df[df[df.columns[0]] == "Белгородская область"].index[0]
    last_row_num = df[df[df.columns[0]] == "Чукотский автономный округ"].index[0]
    df = df.iloc[first_row_num:last_row_num+1]
    df = df[~df[df.columns[0]].isin(["Архангельская область", "Тюменская область", "в том числе:"])]   

    # Если требуется группировка данных
    df = df if with_strats else df[~df[df.columns[0]].str.contains("федеральный округ")]
    
    df = df[[df.columns[0], df.columns[-1]]]
    df = df.set_axis(["Регион", "Значение в 2022"], axis=1)
    df = df.reset_index(drop=True).dropna()
    df['Значение в 2022'] = df['Значение в 2022'].replace("-", 0)
    df['Значение в 2022'] = df['Значение в 2022'].replace("–", 0)
    df['Значение в 2022'] = df['Значение в 2022'].replace("", 0) 
    # df.to_excel(f"test{sheet_name}.xlsx", index=False)
    
    return df