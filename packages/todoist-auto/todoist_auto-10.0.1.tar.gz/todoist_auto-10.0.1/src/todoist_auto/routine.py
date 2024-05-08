"""

    """

import uuid
from functools import partial

import pandas as pd
import requests
from todoist_api.api import TodoistAPI
from todoist_auto.models import ColName
from todoist_auto.models import Notion
from todoist_auto.models import Todoist
from todoist_auto.models import TodoistProject
from todoist_auto.models import TodoistSection
from todoist_auto.models import TodoistTask
from todoist_auto.models import Types
from todoist_auto.util import del_sections
from todoist_auto.util import get_all_sections
from todoist_auto.util import get_all_tasks
from todoist_auto.util import Params
from todoist_auto.util import ret_not_special_items_of_a_class as rnsioac

c = ColName()
ty = Types()
ts = TodoistSection()
tsk = TodoistTask()
tsd = rnsioac(TodoistSection)
tp = TodoistProject()
tpd = rnsioac(TodoistProject)
no = Notion()
to = Todoist()

api = TodoistAPI(to.tok)

pa = Params()

def get_txt_content_fr_notion_name(name) :
    ti = name['title']
    os = ''
    for el in ti :
        os += el['text']['content']
    return os

def get_select_col_val(x) :
    if x['select'] is None :
        return None
    else :
        return x['select']['name']

def get_num_col_val(x) :
    return x['number']

def get_checkbox_col_val(x) :
    return x['checkbox']

def fix_indents(df) :
    df[c.indnt] = df[c.indnt].fillna(1)
    df[c.indnt] = df[c.indnt].astype(int)
    return df

def add_time_to_cont(df) :
    _df = df.copy()

    msk = df[c.th].notna()
    msk |= df[c.tm].notna()

    _df[[c.th , c.tm]] = _df[[c.th , c.tm]].fillna(0)

    msk1 = df[c.tm].lt(10)
    msk1 &= msk

    _df.loc[msk1 , c.tm] = '0' + _df.loc[msk1 , c.tm].astype(int).astype(str)

    msk2 = df[c.tm].ge(10)
    msk2 &= msk
    _df.loc[msk2 , c.tm] = _df.loc[msk2 , c.tm].astype(int).astype(str)

    h = _df.loc[msk , c.th].astype(int).astype(str)
    m = _df.loc[msk , c.tm].astype(str)

    df.loc[msk , c.cnt] = df.loc[msk , c.cnt] + ' - ***' + h + ':' + m + '***'

    df = df.drop(columns = [c.th , c.tm])

    return df

def add_t_type_to_cnt(df) :
    msk = df[c.tty].notna()
    df.loc[msk , c.cnt] = df.loc[msk , c.cnt] + ' @' + df.loc[msk , c.tty]
    df = df.drop(columns = c.tty)
    return df

def fillna_priority(df) :
    msk = df[c.pri].isna()
    df.loc[msk , c.pri] = 4
    return df

def make_labels_list(df) :
    lbl_cols = {
            }

    if not lbl_cols :
        df[c.labels] = df[c.cnt].apply(lambda x : [])
        return df

    _fu = lambda x : [x] if x is not None else []
    df[c.labels] = df[list(lbl_cols.keys())[0]].apply(_fu)
    for col in list(lbl_cols.keys())[1 :] :
        df[c.labels] = df[c.labels] + df[col].apply(_fu)
    return df

def make_sections(df) :
    """ Make sections and get their ids """
    for sec in df[c.sec].unique().tolist() :

        if pd.isna(sec) :
            continue

        ose = api.add_section(sec , pa.routine_proj_id)

        msk = df[c.sec].eq(sec)
        df.loc[msk , c.sec_id] = ose.id

    return df

def make_tasks_with_the_indent(df , indent) :
    msk = df[c.indnt].eq(indent)

    df.loc[msk , c.par_id] = df[c.par_id].ffill()

    _df = df[msk]

    for ind , row in _df.iterrows() :
        sid = row[c.sec_id] if not pd.isna(row[c.sec_id]) else None

        tska = api.add_task(content = row[c.cnt] ,
                            project_id = pa.routine_proj_id ,
                            section_id = sid ,
                            priority = 5 - int(row[c.pri]) ,
                            parent_id = row[c.par_id] ,
                            labels = row[c.labels])

        df.at[ind , c.par_id] = tska.id

    return df

def get_pgs(url , proxies = None) :
    r = requests.get(url , headers = no.hdrs , proxies = proxies)
    return str(r.json())

def find_next_not_sub_task_index(subdf , indent) :
    df = subdf
    df['h'] = df[c.indnt].le(indent)
    return df['h'].idxmax()

def propagate_exculsion_and_drop_final_exculded_tasks(df) :
    # reset index
    df = df.reset_index(drop = True)

    # propagate exculde to sub-tasks
    for indx , row in df.iloc[:-1].iterrows() :
        if not row[c.excl] :
            continue

        nidx = find_next_not_sub_task_index(df[indx + 1 :] , row[c.indnt])

        msk_range = pd.RangeIndex(start = indx , stop = nidx)

        msk = df.index.isin(msk_range)

        df.loc[msk , c.excl] = True

    # drop exculded tasks
    df = df[~ df[c.excl]]

    return df

def filter_tasks_to_take_out_from_sections() :
    # get all tasks
    df = get_all_tasks()

    # keep only tasks in the routine project
    msk = df[tsk.project_id].eq(pa.routine_proj_id)
    df = df[msk]

    # keep those with section_id == those in some section
    msk = df[tsk.section_id].notna()
    df = df[msk]

    # keep only level 1 tasks
    msk = df[tsk.parent_id].isna()
    df = df[msk]

    return df

def move_a_task_under_a_section_out_to_routine_project(task_id) :
    muuid = uuid.uuid4()
    dta = {
            "commands" : r'[ {"type": "item_move", "uuid": ' + f'"{muuid}" ,' + r' "args": { "id": ' + f' "{task_id}", ' + r' "project_id": ' + f' "{pa.routine_proj_id}" ' + r'}}]'
            }
    requests.post('https://api.todoist.com/sync/v9/sync' ,
                  headers = to.hdrs ,
                  data = dta)

def move_all_tasks_out_of_sections() :
    """ move all not done tasks out of sections to routine project body """

    df = filter_tasks_to_take_out_from_sections()
    for ind , ro in df.iterrows() :
        move_a_task_under_a_section_out_to_routine_project(ro[tsk.id])

def rm_all_sections_in_the_routine_proj() :
    df = get_all_sections()

    # keep only sections in the day routine project
    msk = df[ts.project_id].eq(pa.routine_proj_id)
    df = df[msk]

    del_sections(df[ts.id])

def get_routine_from_notion_db() :
    pass

    ##
    proxies = {
            'http'  : '172.31.0.221:8080' ,
            'https' : '172.31.0.221:8080' ,
            }

    if False :
        pass

        ##

        r = requests.post(no.db_url , headers = no.hdrs , proxies = proxies)

    ##
    r = requests.post(no.db_url , headers = no.hdrs)

    ##

    secs = r.json()['results']
    df = pd.DataFrame(secs)

    df = df[['id']]
    df['id'] = df['id'].str.replace('-' , '')
    df[c.url] = no.pg_url + df['id']

    return df

def get_all_pages_in_routine_db_from_notion(df) :
    if False :
        pass

        fu = partial(get_pgs , proxies = proxies)

        df[c.jsn] = df[c.url].apply(lambda x : fu(x))

    df[c.jsn] = df[c.url].apply(lambda x : get_pgs(x))

    df = df[c.jsn].apply(lambda x : pd.Series(eval(x)))
    df = df[['id' , 'properties']]

    df = df['properties'].apply(pd.Series)

    return df

def format_page_properties(df) :
    apply_dct = {
            c.th    : get_num_col_val ,
            c.tm    : get_num_col_val ,
            c.indnt : get_select_col_val ,
            c.srt   : get_num_col_val ,
            c.sec   : get_select_col_val ,
            c.pri   : get_select_col_val ,
            c.tty   : get_select_col_val ,
            c.cnt   : get_txt_content_fr_notion_name ,
            c.excl  : get_checkbox_col_val
            }

    for col , func in apply_dct.items() :
        df[col] = df[col].apply(func)

    return df

def split_section_order_and_section_name(df) :
    new_cols = [c.secn , c.sec]
    df[new_cols] = df[c.sec].str.split('-' , expand = True , n = 1)

    df[c.secn] = df[c.secn].str.strip()
    df[c.sec] = df[c.sec].str.strip()

    return df

def fix_section_order(df) :
    msk = df[c.secn].isna()
    df.loc[msk , c.secn] = 0
    return df

def sort_tasks_based_on_section_and_sort(df) :
    df = df.sort_values([c.secn , c.srt] , ascending = True)
    df = df.drop(columns = [c.secn , c.srt])
    return df

def fix_cols(df) :
    df = fix_indents(df)
    df = add_time_to_cont(df)
    df = fillna_priority(df)
    df = make_labels_list(df)
    df = add_t_type_to_cnt(df)
    return df

def main() :
    pass

    ##
    move_all_tasks_out_of_sections()

    ##
    rm_all_sections_in_the_routine_proj()

    ##
    dfa = get_routine_from_notion_db()

    ##
    df = get_all_pages_in_routine_db_from_notion(dfa)

    ##
    df = format_page_properties(df)

    ##
    df = split_section_order_and_section_name(df)

    ##
    df = fix_section_order(df)

    ##
    df = sort_tasks_based_on_section_and_sort(df)

    ##
    df = fix_cols(df)

    ##
    df = make_sections(df)
    print('All sections created.')

    ##
    df = propagate_exculsion_and_drop_final_exculded_tasks(df)

    ##
    df[c.par_id] = None

    for indnt in sorted(df[c.indnt].unique().tolist()) :
        df = make_tasks_with_the_indent(df , indnt)

##
if __name__ == "__main__" :
    main()
