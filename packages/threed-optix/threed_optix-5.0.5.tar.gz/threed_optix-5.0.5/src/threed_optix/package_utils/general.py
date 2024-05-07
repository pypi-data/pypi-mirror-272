import threed_optix.package_utils.vars as v
from skimage.transform import rescale as sk_scale
import pandas as pd

def process_headers(headers_num):

    data_kind_mapping = v.DATA_KINDS_MAPPING
    polarization_mapping = v.POLARIZATION_MAPPING

    analysis_kind = headers_num['analysis kind'][0]
    data_kind = headers_num['data kind'][0]
    polarization_kind = headers_num['polarization kind'][0]
    num_hits = headers_num['num_hits'][0]
    num_wavelengths = headers_num['num_wavelengths'][0]
    resolution_x = headers_num['resolution_x'][0]
    resolution_y = headers_num['resolution_y'][0]
    resolution = (resolution_x, resolution_y)
    data_kind_value = data_kind_mapping.get(data_kind)
    polarization_kind_value = polarization_mapping.get(polarization_kind)

    headers = {
        "analysis_kind": analysis_kind,
        "data_kind": data_kind_value,
        "polarization_kind": polarization_kind_value,
        "num_hits": num_hits,
        "num_wavelengths": num_wavelengths,
        "resolution": resolution
    }

    return headers

def print_completed_failed(completed, failed, message):
    completed_ = completed.copy()
    failed_ = failed.copy()
    print(f"{message} successfully: {len(completed_)}, failed: {len(failed_)}")

def reorganize_analysis_results_dict(results):
    results = list(results).copy()
    polarization_dict = {}
    for result in results:
        polarization_kind = result['metadata']['polarization_kind'].split('_')[0].capitalize()
        modified_res = result.copy()
        del modified_res['metadata']
        polarization_dict[polarization_kind] = modified_res
    polarization_dict = {k: v['data'] for k, v in polarization_dict.items()}
    wl_dict = {}
    for p, data in polarization_dict.items():
        for wl, matrix in data.items():
            if wl not in wl_dict:
                wl_dict[wl] = {}
            wl_dict[wl][p] = matrix
    return wl_dict

def reorganize_analysis_results_dict2(results):
    return {i: results for i, results in enumerate(results)}

def upscale(results, height, width):
    scale_height = height / results.shape[0]
    scale_width = width / results.shape[1]
    sk_upscale_scale = max(scale_height, scale_width)
    if sk_upscale_scale > 1:
        upscaled_results = sk_scale(results, scale = sk_upscale_scale, anti_aliasing=False)
        return upscaled_results
    return results


def process_v2_results(data, maps):
    def translate_spot_target(row):
        if row['spot_target_kind'] == 0:
            return maps['sources'][row['spot_target_index']]
        if row['spot_target_kind'] == 1:
            return maps['groups'][row['spot_target_index']] if maps.get('groups') else row['spot_target_index']
        return None

    if not data:
        return pd.DataFrame(data)

    data = pd.DataFrame(data)
    data['polarization'] = data['polarization_kind'].apply(lambda x: x.split('_')[0].capitalize())
    data['spot_target'] = data.apply(translate_spot_target, axis=1)
    data['spot_target_kind'] = data['spot_target_kind'].apply(lambda x: v.AnalysisFile2.SPOT_TARGET_KINDS.get(x))
    data.drop(columns = ['data_kind', 'analysis_kind', 'num_wavelengths', 'polarization_kind', 'spot_target_index'], inplace = True)
    return data
