"""
Code for loading the results of experiments.
"""
import os
import re
import json
import math
from pathlib import Path
import pandas as pd
import numpy as np


CIRCUIT_CATEGORY_FILE = os.path.join(os.path.dirname(__file__), 'circuit_categories.json')


def _to_complex_vector(state_vector_json):
    """
    Obtain a 2^n x 1 complex vector from the 2^n x 2 data structure.
    """
    return np.apply_along_axis(lambda args: [complex(*args)], 1, state_vector_json)


def _json_is_empty(log_filepath : str):
    """
    Check if the json file corresponding to the log file is empty.
    """
    parts = os.path.normpath(log_filepath).split(os.path.sep)
    json_path = os.path.join(*parts[:-2], 'json', parts[-1].replace('.log','.json'))
    if os.path.isfile(json_path) and os.path.getsize(json_path) == 0:
        return True
    return False


def _get_termination_status(log_filepath : str):
    """
    Get the termination status of benchmark based on log.
    """
    if os.path.getsize(log_filepath) == 0:
        return "TIMEOUT" if _json_is_empty(log_filepath) else "FINISHED"
    with open(log_filepath, 'r', encoding='utf-8') as f:
        text = f.read()
        if 'qsylvan' in log_filepath:
            if "Amplitude table full" in text:
                return 'WEIGHT_TABLE_FULL'
            elif "Unique table full" in text:
                return 'NODE_TABLE_FULL'
            elif "statistics" in text:
                return 'FINISHED'
            elif "timeout" in text:
                return 'TIMEOUT'
            elif "Assertion" in text and "failed" in text:
                return "ERROR"
            elif len(text.splitlines()) == 1 and "WARNING" in text:
                return "TIMEOUT" if _json_is_empty(log_filepath) else "FINISHED"
            else:
                print("    Could not get termination status from file:")
                print("    " + log_filepath)
        elif 'mqt' in log_filepath:
            pass
        elif 'quokkasharp' in log_filepath:
            if 'timeout' in text:
                return 'TIMEOUT'
    return 'UNKNOWN'


def _get_log_info(log_filepath : str, log_filename : str):
    """
    Get info from the log file.
    """
    stats = {}
    if 'qsylvan' in log_filename:
        stats['tool'] = 'q-sylvan'
        parts = re.split('_|.log', log_filename)
        stats['circuit'] = '_'.join(parts[:parts.index('qsylvan')])
        stats['workers'] = int(parts[parts.index('qsylvan')+1])
    elif 'mqt' in log_filename:
        stats['tool'] = 'mqt'
        stats['circuit'] = log_filename.split('_mqt')[0]
        stats['workers'] = 1
    stats['exp_id'] = int(re.findall(r'\d+', log_filename)[-1])
    stats['status'] = _get_termination_status(log_filepath)
    return stats


def _add_missing_fields(row : dict):
    """
    Add missing data fields (i.e. information which was added to later version
    of the code) to allow the plotting code to re-plot older data.
    """
    if 'reorder' not in row.keys():
        row['reorder'] = 2
    if 'wgt_inv_caching' not in row.keys():
        row['wgt_inv_caching'] = 1
    return row


def load_json(exp_dir : str, add_missing = False):
    """
    Load the data (and do some preprocessing).
    """
    rows = []
    json_dir = os.path.join(exp_dir, 'json')
    for filename in sorted(os.listdir(json_dir)):
        filepath = os.path.join(json_dir, filename)
        if filename.endswith('.json') and os.path.getsize(filepath) > 0:
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    row = data['statistics']
                    if 'mqt' in filename:
                        row['tool'] = 'mqt'
                        row['workers'] = 1
                    elif 'qsylvan' in filename:
                        row['tool'] = 'q-sylvan'
                    row['exp_id'] = int(re.findall(r'\d+', filename)[-1])
                    row['status'] = 'FINISHED'
                    if add_missing:
                        row = _add_missing_fields(row)
                    rows.append(row)
            except json.decoder.JSONDecodeError:
                print(f"    Error getting json data from {filepath}, skipping")

    df = pd.DataFrame(rows)
    return df


def load_logs(exp_dir : str):
    """
    Add information from logs to dataframe.
    """
    new_rows = [ {'exp_id' : 0} ]
    log_dir = os.path.join(exp_dir, 'logs')
    for filename in sorted(os.listdir(log_dir)):
        filepath = os.path.join(log_dir, filename)
        if filename.endswith('.log'):
            row = _get_log_info(filepath, filename)
            if row['status'] != 'FINISHED':
                new_rows.append(row)
    return pd.DataFrame(new_rows)


def load_meta(exp_dir : str):
    """
    Load additional meta data.
    """
    meta_data = []
    meta_dir = os.path.join(exp_dir, 'meta')
    for filename in sorted(os.listdir(meta_dir)):
        filepath = os.path.join(meta_dir, filename)
        if filename.endswith('.json'):
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                meta_data.append(data)
    return pd.DataFrame(meta_data)


def ketgpt_sharing_category(row : pd.Series):
    """
    Compute "no/high/some sharing" category for ketgtp results
    """
    row = row.fillna(0)
    nodes = max(row['final_nodes'], row['max_nodes'])
    qubits = row['n_qubits']
    if row['status'] != 'FINISHED':
        return 4*'\u200b' + 'unknown'
    elif nodes <= qubits*math.log(qubits):
        return 3*'\u200b' + 'high sharing'
    elif nodes >= 2.0**(qubits-2):
        return 1*'\u200b' + 'no sharing'
    else:
        return 2*'\u200b' + 'some sharing'


def add_circuit_categories(df : pd.DataFrame):
    """
    Add column to the df in which every circuit labeled with a category.
    """
    cat_info = {}
    with open(CIRCUIT_CATEGORY_FILE, 'r', encoding='utf-8') as f:
        cat_info = json.load(f)
    circuit_types = cat_info['circuit_types']
    use_cat = cat_info['use_category']
    df.insert(loc=1, column='category', value = 'N/A')
    for i, row in df.iterrows():
        circ_type = row['circuit'].split('_')[0]
        if circ_type in circuit_types:
            cat = circuit_types[circ_type][use_cat]
             # zero-width space for ordering the categories in the legends
            df.at[i, 'category'] = '\u200b'*cat_info['order'].index(cat) + cat
        elif circ_type == 'KetGPT':
            df.at[i, 'category'] = ketgpt_sharing_category(df.loc[i])
        else:
            df.at[i, 'category'] = circ_type
    return df


def compute_errors_from_json(df : pd.DataFrame, exp_dir : str, errors_dir : str):
    """
    Compute state-vector errors from json in given dir and write to errors_dir.
    As ground truth, take the runs with the highest precision, and tolerance = 0.
    """
    Path(errors_dir).mkdir(parents=True, exist_ok=False)

    # ids of ground truth runs
    gt_ids = df.loc[(df['precision'] == df['precision'].max()) & 
                    (df['tolerance'] == 0) & 
                    (df['workers'] == 1)].index

    # pair up all files
    ground_truths = {} # circuit -> filename
    benchmarks = {} # filename -> circuit
    exp_ids = {} # filename -> exp_id
    for filename in sorted(os.listdir(exp_dir)):
        filename_info = re.split('_qsylvan_|.json', filename)
        circuit, exp_id = filename_info[0], int(filename_info[1])
        if exp_id in gt_ids:
            ground_truths[circuit] = filename
        else:
            benchmarks[filename] = circuit
        exp_ids[filename] = exp_id
    
    # check vectors for all pairs
    rows = []
    for bench_file in benchmarks.keys():

        # skip if no ground truth for this circuit
        if benchmarks[bench_file] not in ground_truths:
            print(f"    No ground truth for {bench_file}, skipping")
            continue

        # get filepaths
        gt_path    = os.path.join(exp_dir, ground_truths[benchmarks[bench_file]])
        bench_path = os.path.join(exp_dir, bench_file)

        # try to read files
        vec_bench = None
        vec_gt = None
        try:
            with open(bench_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if 'state_vector' in data:
                    vec_bench = _to_complex_vector(data['state_vector'])
                else:
                    print(f"    No state vector in {bench_path}, skipping")
            with open(gt_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if 'state_vector' in data:
                    vec_gt = _to_complex_vector(data['state_vector'])
                else:
                    print(f"    No state vector in {bench_path}, skipping")
            pass
        except:
            print(f"    Could not get json data from {bench_path} or {gt_path}, skipping")
        
        # add max (relative) error to results
        # NOTE: vec_gt is not the actual ground truth (but rather a higher precision calculation).
        # The relative errors when vec_gt[i] is supposed to be 0 but instead is very small
        # are incorrect (supposed to be undefined) and create outliers in the plots.
        # TODO: how to fix?
        row = {}
        abs_errors = np.abs(vec_gt - vec_bench)
        with np.errstate(divide='ignore', invalid='ignore'):
            rel_errors = abs_errors / np.abs(vec_gt)
        row['exp_id'] = exp_ids[bench_file]
        row['max_error_abs'] = np.max(abs_errors)
        row['max_error_rel'] = np.nanmax(rel_errors)
        rows.append(row)
        # write to file to make re-plotting faster
        output_file = os.path.join(errors_dir, bench_file)
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(row, f, indent=2)

    return pd.DataFrame(rows).set_index('exp_id')


def load_errors_from_json(errors_dir : str):
    """
    Load errors from json files in given dir.
    """
    rows = []
    for filename in sorted(os.listdir(errors_dir)):
        filepath = os.path.join(errors_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            rows.append(data)
    return pd.DataFrame(rows).set_index('exp_id')
