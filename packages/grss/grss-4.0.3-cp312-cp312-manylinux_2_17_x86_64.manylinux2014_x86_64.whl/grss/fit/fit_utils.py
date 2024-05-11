"""Utilities for the GRSS orbit determination code"""
import json
import requests
import numpy as np
from numba import jit

from ..utils import grss_path

__all__ = [ 'mjd2et',
            'et2mjd',
            'get_codes_dict',
            'get_observer_info',
            'get_sbdb_info',
            'get_similarity_stats',
]

@jit('float64(float64)', nopython=True, cache=True)
def mjd2et(mjd):
    """
    Converts Modified Julian Date to JPL NAIF SPICE Ephemeris time.

    Parameters
    ----------
    mjd : float
        Modified Julian Date

    Returns
    -------
    et : float
        Ephemeris time (ephemeris seconds beyond epoch J2000)
    """
    return (mjd+2400000.5-2451545.0)*86400

@jit('float64(float64)', nopython=True, cache=True)
def et2mjd(ephem_time):
    """
    Converts JPL NAIF SPICE Ephemeris time to Modified Julian Date.

    Parameters
    ----------
    ephem_time : float
        Ephemeris time (ephemeris seconds beyond epoch J2000)

    Returns
    -------
    mjd : float
        Modified Julian Date
    """
    return ephem_time/86400-2400000.5+2451545.0


@jit('Tuple((float64, float64, float64))(float64, float64, float64)',
        nopython=True, cache=True)
def parallax_to_lat_lon_alt(lon, rho_cos_lat, rho_sin_lat):
    """
    Convert parallax constants to geocentric longitude, latitude, and distance.

    Parameters
    ----------
    lon : float
        degrees, longitude of observer
    rho_cos_lat : float
        rho cos phi', where rho is the distance from the geocenter to the observer
        and phi' is the geocentric latitude of the observer
    rho_sin_lat : float
        rho sin phi', where rho is the distance from the geocenter to the observer
        and phi' is the geocentric latitude of the observer

    Returns
    -------
    lon : float
        radians, longitude of observer
    lat : float
        radians, geocentric latitude of observer
    rho : float
        distance from the geocenter to the observer, m
    """
    # WGS84 ellipsoid parameters
    r_eq = 6378137.0 # m
    lat = np.arctan2(rho_sin_lat, rho_cos_lat)
    rho = np.sqrt(rho_cos_lat**2 + rho_sin_lat**2)*r_eq
    return lon*np.pi/180, lat, rho

def get_mpc_observatory_info():
    """
    Read in the MPC observatory codes and return them as a dictionary.

    Returns
    -------
    codes_dict : dict
        dictionary of observatory codes and their corresponding longitude,
        rho*cos(latitude), and rho*sin(latitude)
    """
    fpath = f'{grss_path}/fit/codes.json'
    with open(fpath, 'r', encoding='utf-8') as f:
        codes = json.load(f)
    mpc_info_dict = {}
    for key, val in codes.items():
        if 'Longitude' in val and 'cos' in val and 'sin' in val:
            mpc_info_dict[key] = val['Longitude'], val['cos'], val['sin']
    return mpc_info_dict

def get_radar_codes_dict():
    # sourcery skip: inline-immediately-returned-variable
    """
    Creates a dictionary of radar codes and their corresponding longitude,
    geocentric latitude, and distance from the geocenter

    Returns
    -------
    radar_codes_dict : dict
        dictionary of radar codes and their corresponding longitude,
        geocentric latitude, and distance from the geocenter
    """
    # from obscodr.dat
    radar_site_loc = {
        '-1' : (5.118130907583567, 0.3181656968486174, 6376485.333881727),
        '-2' : (5.035480840855376, 0.7405706484785946, 6368498.652158532),
        '-5' : (4.404902108756085, 0.5916728612960379, 6373576.72604664),
        '-7' : (5.100642708478584, -0.399524038599547, 6379967.245894235),
        '-9' : (4.889717923045817, 0.6675170779877466, 6370739.0833090255),
        '-12': (4.244544747741349, 0.6129362736340168, 6371991.805482853),
        '-13': (4.244736733959069, 0.6120180410509634, 6372122.4980728),
        '-14': (4.243078671169674, 0.6151300479071157, 6371998.818089744),
        '-15': (4.24311881374247, 0.6150585185761809, 6371969.864633745),
        '-24': (4.2433352345697175, 0.6136333053130102, 6371971.305963156),
        '-25': (4.243324762594206, 0.613591562161615, 6371985.244902656),
        '-26': (4.243366650496253, 0.6135596331039699, 6371988.34181429),
        '-27': (4.245049147895176, 0.6118624490546375, 6372102.910857716),
        '-28': (4.24500900532238, 0.6118630223297832, 6372123.749433432),
        '-30': (2.454981871184476, 0.6243606496656824, 6370885.734886958),
        '-31': (2.41488642227841, 0.6274360123894954, 6372276.380152331),
        '-34': (2.600226426206192, -0.6146518945371586, 6371696.895259182),
        '-35': (2.6002176995599324, -0.6146063109997237, 6371693.310483042),
        '-36': (2.600165339682372, -0.6145926584351252, 6371686.845710653),
        '-37': (0.6623995750216518, 0.9719174569868173, 6363624.565513317),
        '-38': (0.5792206735301062, 0.7853416799255691, 6367485.25229262),
        '-39': (0.6624327362774398, 1.0069184644478415, 6363037.644793144),
        '-43': (2.600214208901428, -0.6147209467847035, 6371696.186663469),
        '-45': (2.6001513770483564, -0.6146513303468355, 6371676.046576824),
        '-47': (2.6101416416867713, -0.5261377306704356, 6372958.625370879),
        '-49': (2.5876862355306125, -0.5728673795561365, 6372243.0334759895),
        '-51': (4.920559636257809, 0.798717284494754, 6367362.434760925),
        '-53': (6.208949472775259, 0.702271825398319, 6370038.345634378),
        '-54': (6.208937255470495, 0.7022465885003641, 6370019.897420738),
        '-55': (6.2089634354092755, 0.702223144300857, 6370011.116026489),
        '-56': (6.208972162055535, 0.7022516910577987, 6370027.803387983),
        '-58': (0.2032774507822284, 0.7736762901596285, 6367689.985118462),
        '-59': (0.19335106519443584, 0.8323411726917304, 6367084.059003408),
        '-62': (0.12445593830121165, 0.8801430084714452, 6365696.804677316),
        '-63': (6.209043720554868, 0.7023436744200388, 6370053.302865111),
        '-65': (6.208996596665064, 0.7022748594030155, 6370015.505758979),
        '-71': (0.12014176364296197, 0.878526528349089, 6365864.205220217),
        '-72': (4.163102448855539, 0.709077390570306, 6370066.157584699),
        '-73': (0.3355547330604022, 1.2123119930334905, 6359465.28889241),
        '-74': (2.3354215814351083, -0.5531874093138018, 6372379.120672884),
        '-75': (2.5732802878846512, -0.7437500522399563, 6368332.037514396),
        '-76': (2.5732802878846512, -0.7437500522399563, 6368332.037514396),
        '-77': (2.3065276556683423, -0.24930848030288796, 6377014.525085852),
        '-78': (2.0131604976883715, -0.5041219522325624, 6373379.289639647),
        '-79': (2.6022806787357897, -0.542750689803241, 6373270.145477656),
        '-80': (3.5699749918455415, 0.34346577655008154, 6379419.660235015),
        '-81': (4.218860482469002, 0.6465820287430366, 6371559.134510055),
        '-82': (4.335181441126667, 0.5547313111571804, 6374103.163770516),
        '-83': (4.3961492825573325, 0.5955447712959684, 6373752.421762615),
        '-84': (4.4288497714226995, 0.6212127637775329, 6372836.487310473),
        '-85': (4.469006306852585, 0.5317428681811908, 6374241.915461778),
        '-86': (4.194317662527457, 0.8367083415513576, 6366576.525540495),
        '-87': (4.684915752629047, 0.7257130595739807, 6368924.758078582),
        '-88': (5.0267821198634355, 0.7459841618649351, 6368570.241645971),
        '-89': (5.155988844388577, 0.3046527239435524, 6376222.04666057),
        '-91': (0.12553455177894413, 0.8942928579278642, 6365319.001972028),
        '-92': (0.4832012101987129, -0.4492288614371409, 6375505.90823571),
        '-93': (0.16135568934687575, 0.685984303210341, 6370122.728403139),
        '-96': (2.923065213935339, 0.1629031860614893, 6377644.65762988),
        '-97': (5.484002533349886, -1.5706763615148356, 6359749.6043233145)
    }
    # # # add this when ingesting radar data from ADES file not JPL API
    # # map to MPC code for radar observatories if it exists (otherwise use JPL code)
    # code_map = {
    #     '-1': '251', # Arecibo (300-m, 1963 to 2020)
    #     '-2': '254', # Haystack (37-m)
    #     '-9': '256', # Green Bank Telescope (100-m, GBT)
    #     '-13': '252', # DSS-13 (34-m BWG, R&D)
    #     '-14': '253', # DSS-14 (70-m)
    #     '-25': '257', # Goldstone DSS 25
    #     '-35': '-35', # DSS-35 (34-m BWG)
    #     '-36': '-36', # DSS-36 (34-m BWG)
    #     '-38': '255', # Evpatoria (70-m)
    #     '-43': '-43', # DSS-43 (70-m)
    #     '-47': '-47', # DSS-47 (ATCA ref. W196)
    #     '-73': '259', # Tromso (32-m, EISCAT)
    # }
    # radar_codes_dict = {
    #     mpc_code: radar_site_loc[jpl_code] for jpl_code, mpc_code in code_map.items()
    # }
    # return radar_codes_dict
    return radar_site_loc

def get_codes_dict():
    """
    Creates a dictionary of MPC codes and their corresponding longitude,
    geocentric latitude, and distance from the geocenter

    Returns
    -------
    codes_dict : dict
        dictionary of MPC codes and their corresponding longitude,
        geocentric latitude, and distance from the geocenter
    """
    codes_dict = {}
    mpc_info_dict = get_mpc_observatory_info()
    for code, info in mpc_info_dict.items():
        lon, lat, rho = parallax_to_lat_lon_alt(info[0], info[1], info[2])
        codes_dict[code] = (lon, lat, rho)
    radar_codes_dict = get_radar_codes_dict()
    for code, info in radar_codes_dict.items():
        codes_dict[code] = info
    return codes_dict

def get_observer_info(obs_df):
    """
    Creates a list of observer information for each observer code for
    passing into a libgrss PropSimulation object

    Parameters
    ----------
    obs_df : pandas DataFrame
        Observation data conatining observer information

    Returns
    -------
    observer_info : list
        Information about each observer (Spice ID for parent body, longitude,
        geocentric latitude, and altitude). Shape of each entry changes on type
        of observation: 4 (optical), 8 (radar), or 9 (doppler).
    """
    stn_codes_dict = get_codes_dict()
    observer_info = []
    gaia = ['258']
    occultation = ['275']
    spacecraft = [ 'S/C', '245', '249', '250', '274', 'C49', 'C50', 'C51',
                    'C52', 'C53', 'C54', 'C55', 'C56', 'C57', 'C59', ]
    roving = ['247', '270']
    conv_to_m = {
        'ICRF_AU': 1.49597870700e11,
        'ICRF_KM': 1.0e3,
    }
    fields = ['stn', 'mode', 'sys', 'pos1', 'pos2', 'pos3', 'trx', 'rcv', 'com', 'frq', 'doppler']
    for obs_info in zip(*[obs_df[field] for field in fields]):
        stn, mode, sys, pos1, pos2, pos3, trx, rcv, com, freq, doppler = obs_info
        info_list = []
        if stn in gaia+occultation+spacecraft:
            c = conv_to_m[sys]
            info_list.extend((500, pos1*c, pos2*c, pos3*c, 0, 0, 0))
        elif mode == 'RAD':
            rx_lon, rx_lat, rx_rho = stn_codes_dict[rcv]
            tx_lon, tx_lat, tx_rho = stn_codes_dict[trx]
            info_list.extend((
                399, rx_lon, rx_lat, rx_rho,
                399, tx_lon, tx_lat, tx_rho,
                com
            ))
            if np.isfinite(doppler):
                info_list.append(freq)
        elif stn in roving:
            lon = pos1*np.pi/180
            if sys == 'WGS84':
                lat = pos2*np.pi/180
                rho = pos3+6378137.0
            elif sys == 'ITRF':
                lat = np.arctan2(pos2, pos3)
                rho = np.sqrt(pos2**2 + pos3**2)*1.0e3
            else:
                raise ValueError(f"Invalid system {sys}")
            info_list.extend((399, lon, lat, rho))
        elif mode.startswith('SIM'):
            lon = pos1*np.pi/180
            lat = np.arctan2(pos2, pos3)
            rho = np.sqrt(pos2**2 + pos3**2)*1.0e3
            if mode in {'SIM_RAD_DEL', 'SIM_RAD_DOP'}:
                info_list.extend((
                    399, lon, lat, rho,
                    399, lon, lat, rho,
                    com
                ))
                if np.isfinite(doppler):
                    info_list.append(freq)
            else:
                if sys == 'WGS84':
                    lat = pos2*np.pi/180
                    rho = pos3+6378137.0
                elif sys == 'ITRF':
                    lat = np.arctan2(pos2, pos3)
                    rho = np.sqrt(pos2**2 + pos3**2)*1.0e3
                else:
                    raise ValueError(f"Invalid system {sys}")
                info_list.extend((399, lon, lat, rho))
        else:
            lon, lat, rho = stn_codes_dict[stn]
            info_list.extend((399, lon, lat, rho))
        observer_info.append(info_list)
    return observer_info

def get_sbdb_raw_data(tdes):
    """
    Get json data from JPL SBDB entry for desired small body

    Parameters
    ----------
    tdes : str
        IMPORTANT: must be the designation of the small body, not the name.

    Returns
    -------
    raw_data : dict
        JSON output of small body information query from SBDB
    """
    url = f"https://ssd-api.jpl.nasa.gov/sbdb.api?sstr={tdes}&cov=mat&phys-par=true&full-prec=true"
    req = requests.request("GET", url, timeout=30)
    return json.loads(req.text)

def get_sbdb_elems(tdes, cov_elems=True):
    """
    Get a set of desired elements for small body from SBDB API

    Parameters
    ----------
    tdes : str
        IMPORTANT: must be the designation of the small body, not the name.
    cov_elems : bool, optional
        Boolean for whether to extract element set corresponding to the covariance
        information (since the nominal set on the webpage might have a different epoch
        than the full covariance info), by default True

    Returns
    -------
    elements : dict
        Dictionary containing desired cometary elements for the small body
    """
    response = requests.get("https://data.minorplanetcenter.net/api/query-identifier",
                            data=tdes, timeout=30)
    if response.ok:
        tdes = response.json()['unpacked_primary_provisional_designation']
    else:
        print("get_radar_obs_array: ERROR. ", response.status_code, response.content)
        raise ValueError("Failed to get JPL orbit data")
    raw_data = get_sbdb_raw_data(tdes)
    if cov_elems:
        # epoch of orbital elements at reference time [JD -> MJD]
        epoch_mjd = float(raw_data['orbit']['covariance']['epoch']) - 2400000.5
        # cometary elements at epoch_mjd
        if epoch_mjd == float(raw_data['orbit']['epoch']) - 2400000.5:
            elem = raw_data['orbit']['elements']
        else:
            elem = raw_data['orbit']['covariance']['elements']
    else:
        # epoch of orbital elements at reference time [JD -> MJD]
        epoch_mjd = float(raw_data['orbit']['epoch']) - 2400000.5
        # cometary elements at epoch_mjd
        elem = raw_data['orbit']['elements']
    hdr = []
    val = []
    for ele in elem:
        hdr.append(ele['name'])
        val.append(float(ele['value']))
    full_elements_dict = dict(zip(hdr, val))
    # cometary elements
    # eccentricity, perihelion distance, time of periapse passage (JD),
    # longitude of the ascending node, argument of perihelion, inclination
    keys = ['e', 'q', 'tp', 'om', 'w', 'i']
    elements = {'t': epoch_mjd}
    # add every element key to elements dictionary
    for key in keys:
        elements[key] = full_elements_dict[key]
        if key == 'tp':
            elements[key] = full_elements_dict[key] - 2400000.5
        if key in {'om', 'w', 'i'}:
            elements[key] = full_elements_dict[key]*np.pi/180
    return elements

def get_sbdb_info(tdes):
    """
    Return small body orbit information from JPL SBDB API

    Parameters
    ----------
    tdes : str
        IMPORTANT: must be the designation of the small body, not the name.

    Returns
    -------
    elements : dict
        Dictionary containing desired cometary elements for the small body
    cov_mat : array
        Covariance matrix corresponding to cometary elements
    nongrav_params : dict
        Dictionary containing information about nongravitational acceleration
        constants for target body
    """
    # get json info from SBDB entry for small body
    raw_data = get_sbdb_raw_data(tdes)
    # cometary elements corresponding to the covariance on JPL SBDB
    elements = get_sbdb_elems(tdes, cov_elems=True)
    # covariance matrix for cometary orbital elements
    cov_keys = raw_data['orbit']['covariance']['labels']
    cov_mat = (np.array(raw_data['orbit']['covariance']['data'])).astype(float)
    # convert covariance matrix angle blocks from degrees to radians
    cov_mat[3:6, :] *= np.pi/180
    cov_mat[:, 3:6] *= np.pi/180
    # nongravitatinoal constants for target body
    nongrav_data = raw_data['orbit']['model_pars']
    hdr = [param['name'] for param in nongrav_data]
    val = [float(param['value']) for param in nongrav_data]
    nongrav_data_dict = dict(zip(hdr, val))
    nongrav_keys = ['A1', 'A2', 'A3', 'ALN', 'NK', 'NM', 'NN', 'R0']
    # from https://ssd.jpl.nasa.gov/horizons/manual.html
    nongrav_default_vals = [0.0, 0.0, 0.0, 0.1112620426, 4.6142, 2.15, 5.093, 2.808]
    nongrav_default_dict = dict(zip(nongrav_keys, nongrav_default_vals))
    nongrav_key_map = { 'A1': 'a1', 'A2': 'a2', 'A3': 'a3', 'ALN': 'alpha',
                        'NK': 'k', 'NM': 'm', 'NN': 'n', 'R0': 'r0_au'}
    nongrav_params = {}
    for key in nongrav_keys:
        try:
            nongrav_params[nongrav_key_map[key]] = nongrav_data_dict[key]
        except KeyError:
            nongrav_params[nongrav_key_map[key]] = nongrav_default_dict[key]
        if key in cov_keys:
            elements[nongrav_key_map[key]] = nongrav_data_dict[key]
    abs_mag = 0
    albedo = 0.125
    for par in raw_data['phys_par']:
        if par['name'] == 'H':
            abs_mag = float(par['value'])
        if par['name'] == 'albedo':
            albedo = float(par['value'])
    body_radius = 1329*10**(-0.2*abs_mag)/(2*albedo**0.5)*1e3
    if abs_mag == 0:
        body_radius = 0
    nongrav_params['radius'] = body_radius
    return [elements, cov_mat, nongrav_params]

def get_similarity_stats(sol_1, cov_1, sol_2, cov_2):
    """
    Get similarity statistics between two solutions. This includes the
    Mahalanobis distance of both solutions from the other, Bhattacharyya
    distance, and Bhattacharyya coefficient.

    Parameters
    ----------
    sol_1 : vector
        Mean solution 1
    cov_1 : array
        Covariance matrix 1
    sol_2 : vector
        Mean solution 2
    cov_2 : _type_
        Covariance matrix 2

    Returns
    -------
    maha_dist_1 : float
        Mahalanobis distance of solution 2 from solution 1
    maha_dist_2 : float
        Mahalanobis distance of solution 1 from solution 2
    bhattacharya : float
        Bhattacharyya distance between solutions
    bhatt_coeff : float
        Bhattacharyya coefficient of solutions
    """
    maha_dist_1 = np.sqrt((sol_1-sol_2) @ np.linalg.inv(cov_1) @ (sol_1-sol_2).T)
    maha_dist_2 = np.sqrt((sol_1-sol_2) @ np.linalg.inv(cov_2) @ (sol_1-sol_2).T)
    big_cov = (cov_1+cov_2)/2
    det_1 = np.linalg.det(cov_1)
    det_2 = np.linalg.det(cov_2)
    det_big = np.linalg.det(big_cov)
    term_1 = 1/8 * (sol_1-sol_2) @ big_cov @ (sol_1-sol_2).T
    # simplify the natural log in term_2 because sometimes the determinant
    # is too small and the product of the two determinants is beyond the lower
    # limit of the float64 type
    # term_2 = 1/2 * np.log(det_big/np.sqrt(det_1*det_2))
    # term_2 = 1/2 * (np.log(det_big) - np.log(np.sqrt(det_1*det_2)))
    # term_2 = 1/2 * (np.log(det_big) - 1/2 * np.log(det_1*det_2))
    term_2 = 1/2 * np.log(det_big) - 1/4 * (np.log(det_1) + np.log(det_2))
    bhattacharya = term_1 + term_2
    bhatt_coeff = np.exp(-bhattacharya)
    return maha_dist_1, maha_dist_2, bhattacharya, bhatt_coeff
